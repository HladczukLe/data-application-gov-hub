import logging
import yaml
import pandas as pd
import re
import psycopg2
import unicodedata
from airflow.decorators import dag, task
from airflow.models import Variable
from datetime import datetime, timedelta
from schedule_loader import get_dynamic_schedule
from postgres_helpers import get_postgres_conn
from cliente_ibge import ClienteIBGE
from cliente_postgres import ClientPostgresDB


@dag(
    schedule_interval=get_dynamic_schedule("mulheres_censo_dag"),
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={
        "owner": "Rafael, Letícia",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["mulheres", "censo_demografico", "ibge"],
)
def mulheres_censo_demografico_dag() -> None:
    """DAG para extrair, despivotar e armazenar dados do Censo 2022."""

    # Task 1: Listar os arquivos disponíveis no FTP
    @task
    def listar_arquivos_ftp() -> list:
        logging.info("[Task 1] Conectando ao FTP para listar arquivos...")
        config_str = Variable.get(
            "ibge_censo_config", default_var='{"database": "Mulheres"}'
        )
        config = yaml.safe_load(config_str)
        tema_ibge = config.get("database", "Mulheres")

        api_ftp = ClienteIBGE(database=tema_ibge)
        arquivos = api_ftp.listar_arquivos_alvo()

        if not arquivos:
            logging.warning("Nenhum arquivo encontrado no FTP.")

        return arquivos

    # Task 2: Processar cada arquivo
    @task
    def processar_arquivo_ibge(arquivo: str) -> None:
        logging.info(f"[Task 2] Processando arquivo: {arquivo}")

        config_str = Variable.get(
            "ibge_censo_config", default_var='{"database": "Mulheres"}'
        )
        config = yaml.safe_load(config_str)
        tema_ibge = config.get("database", "Mulheres")
        schema_destino = "censo_demografico"

        api_ftp = ClienteIBGE(database=tema_ibge)
        postgres_conn_str = get_postgres_conn()
        db = ClientPostgresDB(postgres_conn_str)

        buffer = api_ftp.obter_conteudo_arquivo(arquivo)
        if not buffer:
            raise ValueError(f"Falha ao baixar o arquivo {arquivo}")

        excel_file = pd.ExcelFile(buffer)

        todas_abas = excel_file.sheet_names

        abas_validas = [
            aba
            for aba in todas_abas
            if "gráfico" not in aba.lower() and "grafico" not in aba.lower()
        ]

        aba_alvo = abas_validas[-1] if abas_validas else todas_abas[0]

        for sheet_name in [aba_alvo]:
            logging.info(f"Avaliando a aba: {sheet_name}")

            df_aba = excel_file.parse(sheet_name, header=None)

            cols_vazias = [
                i for i, col in enumerate(df_aba.columns) if df_aba[col].isnull().all()
            ]
            pontos_corte_h = [-1] + cols_vazias + [len(df_aba.columns)]
            chunks_horizontais = []

            for i in range(len(pontos_corte_h) - 1):
                col_inicio = pontos_corte_h[i] + 1
                col_fim = pontos_corte_h[i + 1]

                df_chunk = df_aba.iloc[:, col_inicio:col_fim].copy()
                df_chunk = df_chunk.dropna(axis=1, how="all").dropna(axis=0, how="all")

                if not df_chunk.empty and len(df_chunk.columns) > 1:
                    chunks_horizontais.append(df_chunk.reset_index(drop=True))

            for idx, df_raw in enumerate(chunks_horizontais):
                sufixo = f"_parte_{idx + 1}" if len(chunks_horizontais) > 1 else ""
                mascara_num = df_raw.apply(
                    lambda r: pd.to_numeric(r, errors="coerce").notna().sum() > 1, axis=1
                )

                if not mascara_num.any():
                    continue

                idx_dados = mascara_num.idxmax()
                linhas_cabecalho = df_raw.iloc[:idx_dados].copy().ffill(axis=1)
                nomes_colunas = []

                for col_idx in range(len(df_raw.columns)):
                    pedacos = []
                    for row_idx in range(len(linhas_cabecalho)):
                        val = str(linhas_cabecalho.iloc[row_idx, col_idx]).strip()
                        unicos = linhas_cabecalho.iloc[row_idx].dropna().unique()
                        if len(unicos) > 1 and val.lower() != "nan":
                            pedacos.append(val.split(" - ")[-1].strip())

                    nome = "_".join(pedacos) if pedacos else f"coluna_{col_idx}"
                    nomes_colunas.append(nome)

                df = df_raw.iloc[idx_dados:].copy()
                df.columns = nomes_colunas

                col_dimensao_original = df.columns[0]
                df = df.dropna(subset=[col_dimensao_original])
                df = df[
                    ~df[col_dimensao_original]
                    .astype(str)
                    .str.contains("Fonte:|Nota:", case=False, na=False)
                ]

                colunas_limpas = []
                for c in df.columns:
                    c_sem_acento = "".join(
                        char
                        for char in unicodedata.normalize("NFD", str(c))
                        if unicodedata.category(char) != "Mn"
                    )
                    c_limpa = re.sub(
                        r"[^\w_]",
                        "",
                        c_sem_acento.lower().replace(" ", "_").replace("-", "_"),
                    )
                    colunas_limpas.append(c_limpa)

                df.columns = colunas_limpas

                col_id_final = df.columns[0]
                cols_fato = [c for c in df.columns if c != col_id_final]

                # Despivotamento / Flattening
                df_flat = df.melt(
                    id_vars=[col_id_final],
                    value_vars=cols_fato,
                    var_name="indicador",
                    value_name="valor",
                )

                df_flat["dt_ingest"] = datetime.now().isoformat()
                df_flat["nome_fonte"] = arquivo

                clean_file = arquivo.split(".")[0].lower()
                match_tab = re.search(r"(tabela_\d+)", clean_file)
                short_file = match_tab.group(1) if match_tab else clean_file[:15]

                sheet_sem_acento = "".join(
                    c
                    for c in unicodedata.normalize("NFD", sheet_name)
                    if unicodedata.category(c) != "Mn"
                )
                clean_sheet = re.sub(
                    r"[^\w_]",
                    "",
                    sheet_sem_acento.lower().replace(" ", "_").replace("-", "_"),
                )

                prefixo_banco = tema_ibge.lower().replace(" ", "_")
                table_name = f"{prefixo_banco}_{short_file}_{clean_sheet}{sufixo}"

                dados = df_flat.to_dict(orient="records")

                # Rewrite da tabela para evitar duplicação de dados antigos
                try:
                    query_drop = f"DROP TABLE IF EXISTS {schema_destino}.{table_name};"
                    with psycopg2.connect(postgres_conn_str) as conn:
                        with conn.cursor() as cursor:
                            cursor.execute(query_drop)
                        conn.commit()
                except Exception as e:
                    logging.error(f"Falha ao eliminar a tabela {table_name}: {e}")

                db.insert_data(data=dados, table_name=table_name, schema=schema_destino)

    lista_de_arquivos = listar_arquivos_ftp()
    processamentos = processar_arquivo_ibge.expand(arquivo=lista_de_arquivos)


dag_instance = mulheres_censo_demografico_dag()
