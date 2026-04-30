import logging
import io
from ftplib import FTP
from cliente_base import ClienteBase


class ClienteIBGE(ClienteBase):
    FTP_HOST = "ftp.ibge.gov.br"
    BASE_DIR = "/Censos/Censo_Demografico_2022/"

    def __init__(self, database) -> None:
        self.host = ClienteIBGE.FTP_HOST
        self.database = database
        logging.info(f"[cliente_ibge.py] Inicializando conexão FTP com: {self.host}")

    def _conectar(self):
        """Método privado para abrir conexão."""
        ftp = FTP(self.host)
        ftp.login()  # IBGE aceita login anônimo

        # Garantindo que o caminho não tenha erro de barras
        full_path = f"{self.BASE_DIR.rstrip('/')}/{self.database.lstrip('/')}"
        ftp.cwd(full_path)
        return ftp

    def listar_arquivos_alvo(self) -> list:
        """
        Lista todos os arquivos de um diretório específico do Censo 2022.
        """
        try:
            ftp = self._conectar()
            arquivos = ftp.nlst()
            ftp.quit()

            # Filtramos apenas arquivos de dados (Excel ou CSV)
            arquivos_filtrados = [
                f for f in arquivos if f.endswith((".xlsx", ".xls", ".csv"))
            ]

            logging.info(
                f"[cliente_ibge.py] {len(arquivos_filtrados)} arquivos encontrados no FTP."
            )
            return arquivos_filtrados
        except Exception as e:
            logging.error(f"[cliente_ibge.py] Erro ao listar arquivos: {e}")
            return []

    def obter_conteudo_arquivo(self, nome_arquivo: str) -> io.BytesIO | None:
        """
        Faz o download do arquivo do FTP diretamente para a memória.
        """
        buffer = io.BytesIO()
        try:
            ftp = self._conectar()
            logging.info(f"[cliente_ibge.py] Baixando arquivo: {nome_arquivo}")

            # Comando RETR baixa o arquivo binário
            ftp.retrbinary(f"RETR {nome_arquivo}", buffer.write)
            ftp.quit()

            buffer.seek(0)
            return buffer
        except Exception as e:
            logging.error(f"[cliente_ibge.py] Erro ao baixar {nome_arquivo}: {e}")
            return None
