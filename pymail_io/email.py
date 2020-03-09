"""
Email class
"""
import smtplib
import ssl
from pytask_io import PyTaskIO
from typing import Dict, Tuple, Any, List, Callable
from functools import partial
from datetime import datetime


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
        sender_email: str,
        password: str,
        receiver_email: str,
        subject: str,
        body: str,
        host: str,
        port: int,
) -> Dict[str, Any]:
    """
    The unit of work must be outside any context
    :param sender_email:
    :param password:
    :param receiver_email:
    :param subject:
    :param body:
    :return:
    """
    time_sent = None
    _SSL_CONTEXT = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=ssl.SSLContext()) as server:
        try:
            server.login(sender_email, password)
            time_sent = datetime.now()
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
            "time_sent": time_sent,
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
    host: str
    port: int

    def __init__(
            self,
            queue,
            sender_email: str,
            password: str,
            receiver_email: str,
            host: str,
            port: int,
    ):
        self.queue = queue
        self.sender_email = sender_email
        self.password = password
        self.receiver_email = receiver_email
        self.host = host
        self.port = port

    def add_email_to_task_queue(
            self,
            email_data: List[str, str],
            unit_of_work: Callable,
    ) -> Dict[str, Any]:
        """
        :param email_data:
        :param unit_of_work:
        :return:
        """
        callable_uow = partial(
            unit_of_work,
            self.sender_email,
            self.password,
            self.receiver_email,
            self.host,
            self.port,
        )

        subject, body = email_data
        meta_data = self.queue.add_task(callable_uow, subject, body)
        return meta_data
