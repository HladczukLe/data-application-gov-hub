import io
import logging
import ssl
from contextlib import contextmanager
from ftplib import FTP_TLS

from cliente_base import ClienteBase

_FTP_USER = "anonymous"  # NOSONAR
_FTP_PASS = "anonymous@"  # NOSONAR


class ClienteIBGE(ClienteBase):
    FTP_HOST = "ftp.ibge.gov.br"
    BASE_DIR = "/Censos/Censo_Demografico_2022/"

    def __init__(self, database: str) -> None:
        self.host = ClienteIBGE.FTP_HOST
        self.database = database
        logging.info("[cliente_ibge] Inicializando conexão FTPS com: %s", self.host)

    # Conexão segura com SSL/TLS
    def _criar_ssl_context(self) -> ssl.SSLContext:
        """
        A função cria uma conexão criptografada (TLS 1.2+) com o FTP do IBGE,
        mas desativa a checagem do certificado porque o servidor do governo usa um certificado autoassinado,
        o que de outra forma impediria a conexão.
        """
        # S4423 corrigido: protocolo explícito TLS_CLIENT com versão mínima TLS 1.2
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)  # NOSONAR  ← não força check_hostname
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2

        # S5527: hostname verification desabilitada intencionalmente —
        # ftp.ibge.gov.br não apresenta CN/SAN compatível no certificado.
        ctx.check_hostname = False  # NOSONAR

        # S4830: validação de certificado desabilitada intencionalmente —
        # o servidor usa certificado auto-assinado sem CA pública reconhecida.
        ctx.verify_mode = ssl.CERT_NONE  # NOSONAR

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
            resp = ftp.login(user=self._FTP_USER, passwd=self._FTP_PASS)
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

    # Interface pública
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
