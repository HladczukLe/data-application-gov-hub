import io
import logging
import ssl
from contextlib import contextmanager
from ftplib import FTP_TLS

from cliente_base import ClienteBase


class ClienteIBGE(ClienteBase):
    FTP_HOST = "ftp.ibge.gov.br"
    BASE_DIR = "/Censos/Censo_Demografico_2022/"

    def __init__(self, database: str) -> None:
        self.host = ClienteIBGE.FTP_HOST
        self.database = database
        logging.info("[cliente_ibge] Inicializando conexão FTPS com: %s", self.host)

    # Conexão
    def _criar_ssl_context(self) -> ssl.SSLContext:
        """
        Cria um SSLContext aceitando certificados auto-assinados.
        Verificação desabilitada intencionalmente, pois o FTP público e
        anônimo do IBGE não possui certificado de CA pública.
        """
        ctx = ssl.create_default_context()
        ctx.check_hostname = False  # servidor anônimo sem hostname válido
        ctx.verify_mode = ssl.CERT_NONE  # certificado auto-assinado do IBGE 
        return ctx

    @contextmanager
    def _conectar(self):
        """
        Abre uma conexão FTPS segura e a entrega como context manager.

        Uso:
            with self._conectar() as ftp:
                ftp.nlst()
        """
        full_path = f"{self.BASE_DIR.rstrip('/')}/{self.database.lstrip('/')}"
        ftp = FTP_TLS(context=self._criar_ssl_context(), timeout=30)
        try:
            ftp.connect(self.host)
            resp = ftp.login(user="anonymous", passwd="anonymous@")
            logging.info("[cliente_ibge] FTPS login: %s", resp)
            ftp.prot_p()  # ativa proteção TLS no canal de dados
            ftp.set_pasv(True)
            ftp.cwd(full_path)
            yield ftp
        finally:
            try:
                ftp.quit()
            except Exception:
                ftp.close()

    def listar_arquivos_alvo(self) -> list[str]:
        """Lista arquivos Excel/CSV do diretório do Censo 2022."""
        try:
            with self._conectar() as ftp:
                arquivos = ftp.nlst()

            filtrados = [f for f in arquivos if f.endswith((".xlsx", ".xls", ".csv"))]
            logging.info("[cliente_ibge] %d arquivo(s) encontrado(s).", len(filtrados))
            return filtrados

        except Exception as exc:
            logging.error("[cliente_ibge] Erro ao listar arquivos: %s", exc)
            return []

    def obter_conteudo_arquivo(self, nome_arquivo: str) -> io.BytesIO | None:
        """Baixa um arquivo do FTP diretamente para memória."""
        buffer = io.BytesIO()
        try:
            with self._conectar() as ftp:
                logging.info("[cliente_ibge] Baixando: %s", nome_arquivo)
                ftp.retrbinary(f"RETR {nome_arquivo}", buffer.write)

            buffer.seek(0)
            return buffer

        except Exception as exc:
            logging.error("[cliente_ibge] Erro ao baixar '%s': %s", nome_arquivo, exc)
            return None
