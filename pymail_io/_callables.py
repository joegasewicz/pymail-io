import smtplib
import ssl
from typing import Dict, Any, Union, List
from datetime import datetime
from email.message import EmailMessage


def format_msg(
        subject: str,
        body: str,
        sender_email: str,
        receiver_email: Union[List[str], str],
) -> EmailMessage:
    """
    :param subject:
    :param body:
    :param sender_email:
    :param receiver_email:
    :return:
    """
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender_email
    if isinstance(receiver_email, list):
        message["To"] = ", ".join(receiver_email)
    else:
        message["To"] = receiver_email
    message.preamble = f"{body}"
    return message


def unit_of_work_callable(
        sender_email: str,
        password: str,
        receiver_email: str,
        host: str,
        port: int,
        subject: str,
        body: str,
) -> Dict[str, Any]:
    """
    :param sender_email:
    :param password:
    :param receiver_email:
    :param host:
    :param port:
    :param subject:
    :param body:
    :return:
    """
    time_sent = None
    _SSL_CONTEXT = ssl.create_default_context()
    message = format_msg(subject, body, sender_email, receiver_email)
    with smtplib.SMTP_SSL(host, port, context=ssl.SSLContext()) as server:
        try:
            server.login(sender_email, password)
            time_sent = datetime.now()
            server.send_message(message)
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