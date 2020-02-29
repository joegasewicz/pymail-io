from abc import ABC, abstractmethod
import smtplib
import ssl, contextlib
from email.message import EmailMessage
from typing import Dict, Any
from pytask_io import PyTaskIO
import asyncio


class AbstractPyMailIO(ABC):

    @abstractmethod
    def send_email(self, *, subject, body) -> Dict[str, Any]:
        pass


class _PyMailIO:

    password: str
    receiver_email: str
    sender_email: str
    store_port: int
    store_host: str
    db: int
    workers: int
    host: str

    _CONTEXT: ssl.SSLContext
    _SMPT_SSL_PORT = 465
    _START_TLS_PORT = 587

    def __init__(self, *args, **kwargs):
        self.password = kwargs.get("password")
        self.receiver_email = kwargs.get("receiver_email")
        self.sender_email = kwargs.get("sender_email")
        self.store_port = kwargs.get("store_port")
        self.store_host = kwargs.get("store_host")
        self.db = kwargs.get("db")
        self.workers = kwargs.get("workers")
        self.host = kwargs.get("host") or "smtp.gmail.com"
        self.init()

    def init(self):
        self._CONTEXT = ssl.create_default_context()

    def send_email_sync(self, email_msg: str):
        with smtplib.SMTP_SSL(self.host, self._SMPT_SSL_PORT, context=self._CONTEXT) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, email_msg)

    @staticmethod
    def _format_msg(subject: str, body: str) -> str:
        formatted_text = f"""\
                Subject: {subject}

                {body}
                """
        return formatted_text

    def create_and_send_email(self, subject: str, body: str) -> Any:
        msg = _PyMailIO._format_msg(subject, body)
        self.send_email_sync(msg)


class PyMailIO(AbstractPyMailIO, _PyMailIO):

    def __init__(self, *args, **kwargs):
        super(PyMailIO, self).__init__(self, *args, **kwargs)

    def send_email(self, *, subject, body) -> Dict[str, None]:
        """
        The response will always be None
        :param subject: The email title or subject
        :param body: The text body of the email
        :return: The response is a Dict with a `response` key
        """
        res = self.create_and_send_email(subject, body)
        return {
            "response": res,
        }


class PymailIOAsync(AbstractPyMailIO, _PyMailIO):

    async def send_email(self) -> Dict[str, Any]:
        """
        :return: Return the PytaskIO metadata dict
        """
        result = await asyncio.sleep(1)
        return {}


class PyMailIOAsTask(AbstractPyMailIO, _PyMailIO):

    def send_email(self) -> Dict[str, Any]:
        pass
