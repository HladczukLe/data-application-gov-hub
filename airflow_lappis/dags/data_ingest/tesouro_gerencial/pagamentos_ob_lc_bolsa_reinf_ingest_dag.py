from typing import Dict, Any, Optional
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import logging
import json
import pandas as pd
import io
from schedule_loader import get_dynamic_schedule
from cliente_email import fetch_and_process_email
from cliente_postgres import ClientPostgresDB
from postgres_helpers import get_postgres_conn

default_args = {
    "owner": "Davi",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

COLUMN_MAPPING = {
    0: "dh_mes_emissao",
    1: "dh_dia_emissao",
    2: "dh_dia_pagamento",
    3: "emitente_ug_codigo",
    4: "emitente_ug_nome",
    5: "ob",
    6: "ob_lista_credores",
    7: "oblc_favorecido_numero",
    8: "oblc_favorecido_nome",
    9: "oblc_banco_codigo",
    10: "oblc_banco_nome",
    11: "oblc_agencia_bancaria_codigo",
    12: "oblc_agencia_bancaria_nome",
    13: "oblc_conta_bancaria",
    14: "oblc_valor",
    15: "oblc_sequencial",
    16: "ob_processo",
    17: "documento_habil",
    18: "doc_observacao",
}

EMAIL_SUBJECT = "Pagamentos _OB_LC_ BOLSA_REINF"
SKIPROWS = 9


with DAG(
    dag_id="email_pagamentos_ob_lc_bolsa_reinf_tesouro_ingest",
    default_args=default_args,
    description=(
        "Processa anexos de pagamentos OB/LC bolsa REINF do Tesouro Gerencial "
        "recebidos por email e insere no banco"
    ),
    schedule_interval=get_dynamic_schedule("pagamentos_ob_lc_bolsa_reinf_ingest_dag"),
    start_date=datetime(2023, 12, 1),
    catchup=False,
    tags=["email", "tesouro", "pagamentos", "bolsa_reinf"],
) as dag:

    def process_email_data(**context: Dict[str, Any]) -> Optional[Any]:
        creds = json.loads(Variable.get("email_credentials"))

        email = creds["email"]
        password = creds["password"]
        imap_server = creds["imap_server"]
        sender_email = creds["sender_email"]

        try:
            logging.info("Iniciando o processamento dos emails...")
            csv_data = fetch_and_process_email(
                imap_server,
                email,
                password,
                sender_email,
                EMAIL_SUBJECT,
                COLUMN_MAPPING,
                skiprows=SKIPROWS,
            )

            if not csv_data:
                logging.warning("Nenhum e-mail encontrado com o assunto esperado.")
                return None

            logging.info(
                "CSV processado com sucesso. Dados encontrados: %s", len(csv_data)
            )
            return csv_data
        except Exception as e:
            logging.error("Erro no processamento dos emails: %s", str(e))
            raise

    def insert_data_to_db(**context: Dict[str, Any]) -> None:
        """Insere os dados processados no banco de dados."""
        try:
            task_instance: Any = context["ti"]
            csv_data: Any = task_instance.xcom_pull(task_ids="process_emails")

            if not csv_data:
                logging.warning("Nenhum dado para inserir no banco.")
                return

            df = pd.read_csv(io.StringIO(csv_data))
            data = df.to_dict(orient="records")

            for record in data:
                record["dt_ingest"] = datetime.now().isoformat()

            postgres_conn_str = get_postgres_conn()
            db = ClientPostgresDB(postgres_conn_str)
            db.insert_data(data, "pagamentos_ob_bolsa", schema="siafi")

            logging.info("Dados inseridos com sucesso no banco de dados.")
        except Exception as e:
            logging.error("Erro ao inserir dados no banco: %s", str(e))
            raise

    def clean_duplicates(**context: Dict[str, Any]) -> None:
        """Remove duplicados da tabela siafi.pagamentos_ob_bolsa."""
        try:
            postgres_conn_str = get_postgres_conn()
            db = ClientPostgresDB(postgres_conn_str)
            db.remove_duplicates(
                "pagamentos_ob_bolsa", COLUMN_MAPPING, schema="siafi"
            )
        except Exception as e:
            logging.error(f"Erro ao executar a limpeza de duplicados: {str(e)}")
            raise

    process_emails_task = PythonOperator(
        task_id="process_emails",
        python_callable=process_email_data,
        provide_context=True,
    )

    insert_to_db_task = PythonOperator(
        task_id="insert_to_db",
        python_callable=insert_data_to_db,
        provide_context=True,
    )

    clean_duplicates_task = PythonOperator(
        task_id="clean_duplicates",
        python_callable=clean_duplicates,
        provide_context=True,
    )

    process_emails_task >> insert_to_db_task >> clean_duplicates_task
