from typing import Dict

from pymail_io.pymail_io import AbstractPyMailIO, PyMailIO, PyTaskIO
import time
import threading


class PyMailIOAsTask(AbstractPyMailIO, PyMailIO):

    def __init__(self, *args, **kwargs):
        super(PyMailIOAsTask, self).__init__(self, *args, **kwargs)

    def send_email(self, *, subject, body) -> Dict[str, Dict]:
        """
        :param subject:
        :param body:
        :return:
        """
        metadata = self.add_email_to_task_queue(subject, body)

        return metadata

    def get_task(self, metadata):
        return self.pytask.get_task(metadata)
