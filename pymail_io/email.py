"""
Email class
"""
import smtplib
import ssl
from pytask_io import PyTaskIO
from typing import Dict, Tuple, Any, List, Callable
from functools import partial


def format_msg(subject: str, body: str) -> str:
    """
    :param subject:
    :param body:
    :return:
    """
    formatted_text = f"""\
            Subject: {subject}

            {body}
            """
    return formatted_text


def unit_of_work_callable(
        subject: str,
        body: str,
        sender_email: str,
        password: str,
        receiver_email: str,
) -> Dict[str, Any]:
    """
    The unit of work must be outside any context
    :param subject:
    :param body:
    :param sender_email:
    :param password:
    :param receiver_email:
    :return:
    """
    _SSL_CONTEXT = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.SSLContext()) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, format_msg(subject, body))
        except smtplib.SMTPAuthenticationError as err:
            Warning(
                "PyMailIO Error: Couldn't authenticate email senders credentials"
            )
        finally:
            server.quit()
    return {
        "sent_email": {
            "subject": subject,
            "body": body,
        }
    }


class Queue(PyTaskIO):
    """
        DI here
    """
    pass


class Email:

    queue: PyTaskIO
    sender_email: str
    password: str
    receiver_email: str

    def __init__(self, queue, sender_email: str, password: str, receiver_email: str):
        self.queue = queue
        self.sender_email = sender_email
        self.password = password
        self.receiver_email = receiver_email

    def add_email_to_task_queue(
            self,
            inner: Callable,
            email_data: List[str, str],
            host: int,
            SMPT_SSL_PORT: int,
            unit_of_work: Callable,
    ) -> Dict[str, Any]:
        """
        :param inner:
        :param email_data:
        :param host:
        :param SMPT_SSL_PORT:
        :param unit_of_work:
        :return:
        """
        subject, body = email_data
        meta_data = self.queue.add_task(unit_of_work, subject, body)
        return meta_data
