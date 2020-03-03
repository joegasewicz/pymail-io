import pytest
import smtplib

from pymail_io.pymail_io import PyMailIO


class MockServer:
    def __init__(self, t, y):
        pass

    def login(self, t, y):
        pass

    def sendmail(self, t, y, u):
        pass

    def quit(self):
        pass


class TestPyMailIO:

    def test_init(self):

        p = PyMailIO(
            sender_email="test_sender",
            receiver_email="receiver_email",
            password="test_password",
        )

        result = p.format_msg("Hello John", "This is a test message.")

        print(result)

        assert "Subject: Hello John" in result
        assert "This is a test message." in result

    def test_add_email_to_task_queue(self, monkeypatch):
        p = PyMailIO(
            sender_email="test_sender",
            receiver_email="receiver_email",
            password="test_password",
        )

        monkeypatch.setattr(smtplib, "SMTP_SSL", lambda t, y: MockServer(t, y))
        result = p.add_email_to_task_queue("Hello John", "This is a test message.")