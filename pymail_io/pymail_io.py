from abc import ABC, abstractmethod
import smtplib
from email.message import EmailMessage


email_msg = EmailMessage()

email_msg["Subject"] = "test here"
email_msg["From"] = "pymailio@gmail.com"
email_msg["To"] = "pymailio@gmail.com"

s = smtplib.SMTP("localhost")
s.send_message(email_msg)
s.quit()


class AbstractConnection(ABC):
    pass



class PyMailIO:

    def __init__(self):
        pass

    def send(self):


