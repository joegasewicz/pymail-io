"""
PyMailIO is a low level class designed to be used be authors of libraries etc.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Awaitable
from pytask_io import PyTaskIO


from pymail_io.email import Email
from pymail_io.callables import unit_of_work_callable, send_email_with_async


class AbstractPyMailIO(ABC):

    @abstractmethod
    def send_email(self, *, subject, body) -> Dict[str, Any]:
        pass


class PyMailIO:
    """
    :kwargs:
    :key password: Your senders email password.
    :key receiver_email: This can be either a string or a list of email addresses.
    :key sender_email: The senders email address.
    :key store_port: Redis store port (defaults to 6379).
    :key store_host: The email server host.
    :key db: The Redis store database name.
    :key workers: The number of workers created to run tasks in the queue.
    :key email_host: The email server host.
    :key email_port: The email server SSL or TLS port.
    """

    #: PyMailIO iss a python library built on CPython's AsyncIO library.
    #: The entree to asyncio is via `PyTaskIO <https://github.com/joegasewicz/pytask-io>`_ which is
    #: an asynchronous task queue library that runs an event loop in a background thread.
    #:
    #: Setting up the library for debugging. Example::
    #:
    #:  export PYTASKIO_DEBUG=1
    #:
    #:
    #: The senders email password.
    password: str

    #: This can be either a string or a list of email addresses.
    receiver_email: str

    #: The senders email address.
    sender_email: str

    #: The email server host.
    email_host: str

    email: Email

    #: Accesses the `PyTaskIO <https://github.com/joegasewicz/pytask-io>`_ task queue library
    queue: PyTaskIO = None

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
        self.email_host = kwargs.get("email_host")
        self.email_port = kwargs.get("email_port") or self._SMPT_SSL_PORT

    def send_email_sync(self, subject: str, body: str):
        """
        :param subject:
        :param body:
        :return:
        """
        return self.email.send_sync_email(unit_of_work_callable, [subject, body])

    async def send_email_async(self, subject: str, body: str) -> Awaitable[Dict[str, Any]]:
        """
        :param subject:
        :param body:
        :return:
        """
        return await self.email.send_async_email(send_email_with_async, [subject, body])

    def add_email_to_queue(self, subject: str, body: str):
        """
        :param subject:
        :param body:
        :return:
        """
        return self.email.add_email_to_task_queue(unit_of_work_callable, [subject, body])
