import pytask_io
import datetime

from pymail_io.pymailio_task import Task
from tests.fixtures import mock_server, pytask_io_fixture
from tests.mock_data import payload_one


class TestTask:

    def test_send_email(self, monkeypatch, pytask_io_fixture):

        p = Task(
            pytask_io_fixture,
            password="wizard",
            sender_email="your_email@gmail.com",
            host="smtp.gmail.com",

        )

        subject = "test subject 1"
        body = "test body 1"

        r = p.send_email(
            subject="test subject 1",
            body="test body 1",
            receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
        )

        assert r["email"]["subject"] == subject
        assert r["email"]["body"] == body
        assert isinstance(r["email"]["email_init"], datetime.datetime)
        assert r["metadata"] == payload_one

    def test_get_email_response(self, monkeypatch, pytask_io_fixture):

        p = Task(
            pytask_io_fixture,
            password="wizard",
            sender_email="your_email@gmail.com",
            host="smtp.gmail.com",

        )

        r = p.send_email(
            subject="test subject 1",
            body="test body 1",
            receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
        )

        r = p.get_email_response(r)

        assert "metadata" in r

    def test_datetime_exec(self, monkeypatch, pytask_io_fixture):

        p = Task(
            pytask_io_fixture,
            password="wizard",
            sender_email="your_email@gmail.com",
            host="smtp.gmail.com",

        )

        r = p.send_email(
            subject="test subject 1",
            body="test body 1",
            receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
        )

        timestamp = p.datetime_exec()

        assert isinstance(timestamp, datetime.datetime)

    def test_exec_time(self, monkeypatch, pytask_io_fixture):

        p = Task(
            pytask_io_fixture,
            password="wizard",
            sender_email="your_email@gmail.com",
            host="smtp.gmail.com",

        )

        r = p.send_email(
            subject="test subject 1",
            body="test body 1",
            receiver_email="joe@blogs.com",  # Or a list of emails receiver_email=["joe@blogs.com", ...],
        )

        r = p.get_email_response(r)

        timestamp = p.exec_time(r)

        assert isinstance(timestamp, datetime.datetime)

