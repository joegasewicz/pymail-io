"""
Email class
"""
from pytask_io import PyTaskIO
from typing import Dict, Any, Callable, Awaitable
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
    email_host: str
    email_port: int

    def init(self, **kwargs):
        self.queue = kwargs.get("queue")
        self.sender_email = kwargs.get("sender_email")
        self.password = kwargs.get("password")
        self.receiver_email = kwargs.get("receiver_email")
        self.email_host = kwargs.get("email_host")
        self.email_port = kwargs.get("email_port")

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
            self.email_host,
            self.email_port,
        )

        subject, body = email_data
        meta_data = self.queue.add_task(callable_uow, subject, body)
        return meta_data

    async def send_async_email(self, unit_of_work: Callable, email_data: Any) -> Awaitable[Dict[str, Any]]:
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
            self.email_host,
            self.email_port,
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
            self.email_host,
            self.email_port,
        )
        subject, body = email_data
        return send_email(subject, body)
