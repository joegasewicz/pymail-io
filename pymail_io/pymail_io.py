from abc import ABC, abstractmethod
import smtplib
import ssl
from email.message import EmailMessage
from typing import Dict, Any
from pytask_io import PyTaskIO

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
password = PASSWORD
sender_email = SENDER_EMAIL
receiver_email = RECEIVER_EMAIL
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
    def send(self) -> Dict[str, Any]:
        pass


class _PyMailIO:
    pass


class PyMailIO(AbstractPyMailIO, _PyMailIO):

    def __init__(self):
        pass

    def send(self) -> Dict[str, Any]:
        pass


class PymailIOAsync(AbstractPyMailIO, _PyMailIO):

    def send(self) -> Dict[str, Any]:
        pass


class PyMailIOAsTask(AbstractPyMailIO, _PyMailIO):

    def send(self) -> Dict[str, Any]:
        pass
