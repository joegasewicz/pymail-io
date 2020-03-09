import smtplib
import ssl
from typing import Dict, Any
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
        host: str,
        port: int,
        subject: str,
        body: str,
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