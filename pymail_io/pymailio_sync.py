from typing import Dict, Any
import asyncio

from pymail_io.pymail_io import AbstractPyMailIO, PyMailIO


class PyMailSyncIO(AbstractPyMailIO, PyMailIO):

    def __init__(self, *args, **kwargs):
        super(PyMailSyncIO, self).__init__(self, *args, **kwargs)
        self.init()

    def send_email(self, *, subject, body) -> Dict[str, None]:
        """
        The response will always be None
        :param subject: The email title or subject
        :param body: The text body of the email
        :return: The response is a Dict with a `response` key
        """
        res = self.create_and_send_email(subject, body)
        return res


