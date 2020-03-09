from abc import ABC, abstractmethod
import smtplib
import ssl

from typing import Dict, Any
from pytask_io import PyTaskIO
import asyncio
import time
import threading

from pymail_io._email import Email
from pymail_io._callables import unit_of_work_callable


class AbstractPyMailIO(ABC):

    @abstractmethod
    def send_email(self, *, subject, body) -> Dict[str, Any]:
        pass


class PyMailIO:

    password: str
    receiver_email: str
    sender_email: str
    store_port: int
    store_host: str
    db: int
    workers: int
    host: str
    pytask: PyTaskIO = None
    background_thread: threading.Thread
    foreground_thread: threading.Thread
    queue: PyTaskIO
    email: Email

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
        self.port = kwargs.get("port") or self._SMPT_SSL_PORT
        self.pytask = PyTaskIO(
            store_port=6379,
            store_host="localhost",
            db=0,
            workers=3,
        )
        self.email = Email(
            queue=self.pytask,
            sender_email=self.sender_email,
            password=self.password,
            receiver_email=self.receiver_email,
            host=self.host,
            port=self.port,
        )

    def send_email_sync(self, email_msg: str):
        def inner():
            server = smtplib.SMTP_SSL(self.host, self._SMPT_SSL_PORT)
            try:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, email_msg)
            except smtplib.SMTPAuthenticationError as err:
                Warning(
                    "PyMailIO Error: Couldn't authenticate email senders credentials"
                )

            server.quit()
        return inner

    def format_msg(self, subject: str, body: str) -> str:
        formatted_text = f"""\
                Subject: {subject}

                {body}
                """
        return formatted_text

    def create_and_send_email(self, subject: str, body: str) -> Any:
        msg = self.format_msg(subject, body)
        self.send_email_sync(msg)

    def send_email_on_queue(self, subject: str, body: str):
        self.email.add_email_to_task_queue(unit_of_work_callable, [subject, body])


class PyMailSyncIO(AbstractPyMailIO, PyMailIO):

    def __init__(self, *args, **kwargs):
        super(PyMailSyncIO, self).__init__(self, *args, **kwargs)
        self.init()

    def send_email(self, *, subject, body) -> Dict[str, None]:
        """
        The response will always be None
        :param subject: The email title or subject
        :param body: The text body of the email
        :return: The response is a Dict with a `response` key
        """
        res = self.create_and_send_email(subject, body)
        return res


class PymailIOAsync(AbstractPyMailIO, PyMailIO):

    async def send_email(self) -> Dict[str, Any]:
        """
        :return: Return the PytaskIO metadata dict
        """
        result = await asyncio.sleep(1)
        return result
