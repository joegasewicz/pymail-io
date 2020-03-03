from typing import Dict

from pymail_io.pymail_io import AbstractPyMailIO, PyMailIO, PyTaskIO
import time


class PyMailIOAsTask(AbstractPyMailIO, PyMailIO):

    def __init__(self, *args, **kwargs):
        super(PyMailIOAsTask, self).__init__(self, *args, **kwargs)
        self.pytask = PyTaskIO(
            store_port=6379,
            store_host="localhost",
            db=0,
            workers=3,
        )
        self.init()

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


