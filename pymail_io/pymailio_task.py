"""
Main Public API for sending emails by adding it to the asyncio task queue
without having to block waiting for a response.
"""
from typing import Dict, Any

from pymail_io.pymail_io import AbstractPyMailIO, PyMailIO


class PyMailIOTask(AbstractPyMailIO, PyMailIO):
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
    #: The entree to asyncio is via `PyTaskIO <https://github.com/joegasewicz/pytask-io>`_ which is
    #: an asynchronous task queue library that runs an event loop in a background thread.
    #: Basic Usage. Example::
    #:
    #:    from pymail_io.pymailio_task import PyMailIOTask
    #:
    #:    p = PyMailIOTask(
    #:        password="wizard",
    #:        receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
    #:        sender_email="your_email@gmail.com",
    #:        host="smtp.gmail.com",
    #:    )
    #:
    #:    # Create your email subject & body
    #:    email_meta = p.send_email(
    #:        subject="The subject...",
    #:        body="The email body...",
    #:    )
    #:
    #:     # Get a response from your sent email:
    #:     res = p.get_email_response(email_meta)
    #:
    #: Set to False by default. If you want to keep the asyncio task queue running in the background thread
    #: then set this to true.
    run_forever: bool

    def __init__(self, *args, **kwargs):
        super(PyMailIOTask, self).__init__(self, *args, **kwargs)

    def send_email(self, *, subject, body) -> Any:
        """
        Example::

            email_meta = p.send_email(
                subject="The subject...",
                body="The email body...",
            )

        :param subject:
        :param body:
        :return:
        """
        self.queue.run()
        metadata = self.add_email_to_queue(subject, body)
        if not self.run_forever:
            self.queue.stop()
        return metadata

    def get_email_response(self, metadata):
        """
        Gets the task result
        :param metadata:
        :return:
        """
        return self.queue.get_task(metadata)
