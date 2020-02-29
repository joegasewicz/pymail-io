from abc import ABC, abstractmethod
import smtplib
import ssl
from email.message import EmailMessage
from typing import Dict, Any
from pytask_io import PyTaskIO
import asyncio

# TODO This gets removed when the library is ready to be used
from env import PASSWORD, SENDER_EMAIL, RECEIVER_EMAIL

#
# email_msg = EmailMessage()
#
# email_msg["Subject"] = "test here"
# email_msg["From"] = "pymailio@gmail.com"
# email_msg["To"] = "pymailio@gmail.com"
#
# s = smtplib.SMTP("localhost")
# s.send_message(email_msg)
# s.quit()

SMPT_SSL_PORT = 465
START_TLS_PORT = 587

SMTP_SERVER = "smtp.gmail.com"

message = """\
Subject: Hi Joe!!!

Test message #1 ...
"""

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", SMPT_SSL_PORT, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)


class AbstractPyMailIO(ABC):

    @abstractmethod
    def send_email(self) -> Dict[str, Any]:
        pass


class _PyMailIO:

    password: str
    receiver_email: str
    sender_email: str

    def __init__(self, *args, **kwargs):
        self.password = kwargs.get("password")
        self.receiver_email = kwargs.get("receiver_email")
        self.sender_email = kwargs.get("sender_email")


class PyMailIO(AbstractPyMailIO, _PyMailIO):

    def __init__(self, *args, **kwargs):
        super(PyMailIO, self).__init__(self, *args, **kwargs)

    def send_email(self) -> Dict[str, Any]:
        pass


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


if __name__ == "__main__":

    pymail_io = PyMailIO(
        password=PASSWORD,
        sender_email=SENDER_EMAIL,
        receiver_email=RECEIVER_EMAIL,
    )
    pymail_io.send_email()