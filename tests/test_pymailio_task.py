import pytask_io
import datetime

from pymail_io.pymailio_task import PyMailIOTask
from tests.fixtures import mock_server, pytask_io_fixture
from tests.mock_data import payload_one


class TestPyMailIOTask:

    def test_send_email(self, monkeypatch, pytask_io_fixture):

        p = PyMailIOTask(
            pytask_io_fixture,
            password="wizard",
            receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
            sender_email="your_email@gmail.com",
            host="smtp.gmail.com",

        )

        subject = "test subject 1"
        body = "test body 1"

        r = p.send_email(
            subject="test subject 1",
            body="test body 1",
        )

        assert r["email"]["subject"] == subject
        assert r["email"]["body"] == body
        assert isinstance(r["email"]["email_init"], datetime.datetime)
        assert r["metadata"] == payload_one

    def test_get_email_response(self, monkeypatch, pytask_io_fixture):

        p = PyMailIOTask(
            pytask_io_fixture,
            password="wizard",
            receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
            sender_email="your_email@gmail.com",
            host="smtp.gmail.com",

        )

        r = p.send_email(
            subject="test subject 1",
            body="test body 1",
        )

        r = p.get_email_response(r)

        assert r == {}
