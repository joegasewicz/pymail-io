import pytask_io

from pymail_io.pymailio_task import PyMailIOTask
from tests.fixtures import mock_server, pytask_io_fixture


class TestPyMailIOTask:

    def test_send_email(self, monkeypatch, pytask_io_fixture):

        monkeypatch.setattr(pytask_io, "PyTaskIO", pytask_io_fixture)

        p = PyMailIOTask(
            password="wizard",
            receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
            sender_email="your_email@gmail.com",
            host="smtp.gmail.com",
        )

        result = p.send_email(
            subject="test subject 1",
            body="test body 1",
        )

        assert result == {}

    def test_get_email_response(self):
        pass