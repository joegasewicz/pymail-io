from typing import Dict, Any
import asyncio

from pymail_io.pymail_io import AbstractPyMailIO, PyMailIO


class PymailIOAsync(AbstractPyMailIO, PyMailIO):

    async def send_email(self) -> Dict[str, Any]:
        """
        :return: Return the PytaskIO metadata dict
        """
        result = await asyncio.sleep(1)
        return result
