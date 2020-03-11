from pymail_io.pymailio_task import PyMailIOTask
from tests.fixtures import mock_server, redis_fixture, pytask_io_fixture


class TestPyMailIOTask:

    def test_send_email(self, moneypatch, redis_fixture, pytask_io_fixture):

        moneypatch.setattr()

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
