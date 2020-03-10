"""
PyMailIO is a low level class designed to be used be authors of libraries etc.
"""
from abc import ABC, abstractmethod
import smtplib
import ssl

from typing import Dict, Any
from pytask_io import PyTaskIO
import asyncio
import time
import threading

from pymail_io._email import Email
from pymail_io._callables import unit_of_work_callable


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
    :key host: The email server host.
    :key port: The email server SSL or TLS port.
    """

    #: PyMailIO is a python library built on CPython's AsyncIO library.
    #: The entree to asyncio is via `PyTaskIO https://github.com/joegasewicz/pytask-io` which is
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

    store_port: int

    store_host: str

    db: int

    workers: int

    host: str

    pytask: PyTaskIO = None

    queue: PyTaskIO

    email: Email

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
        self.host = kwargs.get("host")
        self.port = kwargs.get("port") or self._SMPT_SSL_PORT
        self.pytask = PyTaskIO(
            store_port=6379,
            store_host="localhost",
            db=0,
            workers=3,
        )
        self.email = Email(
            queue=self.pytask,
            sender_email=self.sender_email,
            password=self.password,
            receiver_email=self.receiver_email,
            host=self.host,
            port=self.port,
        )

    def send_email_sync(self, email_msg: str):
        """
        :param email_msg:
        :return:
        """
        def inner():
            server = smtplib.SMTP_SSL(self.host, self._SMPT_SSL_PORT)
            try:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, email_msg)
            except smtplib.SMTPAuthenticationError as err:
                Warning(
                    "PyMailIO Error: Couldn't authenticate email senders credentials"
                )

            server.quit()
        return inner

    def create_and_send_email(self, subject: str, body: str) -> Any:
        """
        :param subject:
        :param body:
        :return:
        """
        msg = self.format_msg(subject, body)
        self.send_email_sync(msg)

    def send_email_on_queue(self, subject: str, body: str):
        """
        :param subject:
        :param body:
        :return:
        """
        self.email.add_email_to_task_queue(unit_of_work_callable, [subject, body])
