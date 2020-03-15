"""
Main Public API for sending emails by adding it to the asyncio task queue
without having to block waiting for a response.
"""
from typing import Dict, Any, Union, List
from pytask_io import PyTaskIO
from datetime import datetime

from pymail_io.pymail_io import AbstractPyMailIO, PyMailIO
from pymail_io.email import Email


class Task(AbstractPyMailIO, PyMailIO):
    """
    PyMailIO is a python library built on CPython's AsyncIO library.
    The entree to asyncio is via `PyTaskIO <https://github.com/joegasewicz/pytask-io>`_ which is
    an asynchronous task queue library that runs an event loop in a background thread.
    First, download and install & run the Redis image. Example::

       docker run Redis

    Now, we are ready to use PyMailIO. Basic Usage. Example::

       from pymail_io.pymailio_task import Task

       p = Task(
           password="wizard",
           sender_email="your_email@gmail.com",
           email_host="smtp.gmail.com",
       )

       # Create your email subject & body
       email_meta = p.send_email(
           subject="The subject...",
           body="The email body...",
           receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
       )

        # Get a response from your sent email:
        res = p.get_email_response(email_meta)

    To update the task queue & store settings, you can pass in extra values as kwargs to
    the `Task` class. For example::

       p = Task(
           password="wizard",
           sender_email="your_email@gmail.com",
           email_host="smtp.gmail.com",

           # extra settings:
            store_port=6379,
            store_host="localhost",
            db=0,
            workers=1,
       )

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


    #: Set to False by default. If you want to keep the asyncio task queue running in the background thread
    #: then set this to true. Setting `run_forever` to True, will give much faster performances & is ideal
    #: when you can run the event loop thread against a long running process, such as the life time process
    #: of a web framework or rest API library.
    run_forever: bool = False

    #: Accesses the `PyTaskIO <https://github.com/joegasewicz/pytask-io>`_ task queue library
    queue: PyTaskIO = None

    #: The Redis port (this will default to 6379).
    store_port: int

    #: store_host: The email server host.
    store_host: str

    #: The Redis store database name.
    db: int

    #: The number of workers created to run tasks in the queue.
    workers: int

    _email_results: Dict[str, Dict[str, Any]]

    def __init__(
            self,
            queue: PyTaskIO = PyTaskIO(),
            email: Email = Email(),
            *args,
            **kwargs
    ):
        super(Task, self).__init__(self, *args, **kwargs)
        self.queue = queue
        self.email = email
        self.run_forever = kwargs.get("run_forever") or False
        self.store_port = kwargs.get("store_port") or 6379
        self.store_host = kwargs.get("store_host") or "localhost"
        self.workers = kwargs.get("workers") or 3

        self.queue.init(
            store_port=self.store_port,
            store_host=self.store_host,
            db=self.db,
            workers=self.workers,
        )
        self.email.init(
            queue=self.queue,
            sender_email=self.sender_email,
            password=self.password,
            receiver_email=self.receiver_email,
            email_host=self.email_host,
            email_port=self.email_port,
        )

    def send_email(self, *, subject: str, body: str, receiver_email: Union[str, List[str]]) -> Any:
        """
        Example::

            email_meta = p.send_email(
                subject="The subject...",
                body="The email body...",
            )

        :param subject:
        :param body:
        :param receiver_email: Example: "joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
        :return:
        """
        timestamp_now = datetime.now()
        self.queue.run()
        metadata = self.add_email_to_queue(subject, body, receiver_email)
        if not self.run_forever:
            self.queue.stop()

        data = {
            "metadata": metadata,
            "email": {
                "subject": subject,
                "body": body,
                "receiver_email": receiver_email,
                "email_init": timestamp_now,
            }
        }

        self._email_results = data
        return data

    def get_email_response(self, email_res: Dict[str, Dict[str, Any]]) -> Any:
        """
        To get the results of the email from the store, pass the metadata
        to `get_email_response`.
        For example::

            r = p.send_email(
                subject="The subject...",
                body="The email body...",
            )

            email_meta = p.get_email_response(r)

        :param email_res:
        :return:
        """
        if "metadata" not in email_res:
            raise ValueError(
                "PyTaskIO Error: Could not reference metadata key in email_res arg "
                "Please visit: https://pymail-io.readthedocs.io/en/latest/pymailio_task.html "
                "for more info."
            )
        return self.queue.get_task(email_res["metadata"])

    def datetime_exec(self) -> str:
        """
        There are 2 datetime values that reference when PyMailIO executed the `send_email`
        method & also when the email was actually sent from the background queue:
        The `datetime_exec` method will give you the datetime value that PyMailIO executed
        the `send_email` method.
        For example::

            r = p.send_email(
                subject="The subject...",
                body="The email body...",
            )

            self.datetime_exec()

        :return:
        """
        return self._email_results["email"]["email_init"]

    def exec_time(self, data: Dict[str, Dict[str, Any]]) -> str:
        """
        :param data: The response Dict from the `send_email` method.
        There are 2 datetime values that reference when PyMailIO executed the `send_email`
        method & also when the email was actually sent from the background queue:
        The `exec_time` method will give you the datetime value that PyMailIO's **queue** executed
        the `send_email` method.
        For example::

            r = p.send_email(
                subject="The subject...",
                body="The email body...",
            )

            # Some time in the future...
            r = get_email_response(r)
            time_email_sent = self.exec_time(r)

        :return:
        """
        return data["metadata"]["result_exec_date"]
