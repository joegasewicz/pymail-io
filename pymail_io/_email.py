"""
Email class
"""
import smtplib
from pytask_io import PyTaskIO
from typing import Dict, Any, Callable
from functools import partial


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

    def add_email_to_task_queue(self, unit_of_work: Callable, email_data: Any, ) -> Dict[str, Any]:
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

    async def send_async_email(self, unit_of_work: Callable, email_data: Any) -> Dict[str, Any]:
        """
        :param unit_of_work:
        :param email_data:
        :return:
        """
        send_email = partial(
            unit_of_work,
            self.sender_email,
            self.password,
            self.receiver_email,
            self.host,
            self.port,
        )
        subject, body = email_data
        return await send_email(subject, body)

    def send_sync_email(self, unit_of_work: Callable, email_data: Any) -> Dict[str, Any]:
        """
        :param unit_of_work:
        :param email_data:
        :return:
        """
        send_email = partial(
            unit_of_work,
            self.sender_email,
            self.password,
            self.receiver_email,
            self.host,
            self.port,
        )
        subject, body = email_data
        return send_email(subject, body)
