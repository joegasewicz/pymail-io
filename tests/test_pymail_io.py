# import pytest
# import smtplib
#
# from pymail_io.pymail_io import PyMailIO
# from pymail_io.pymailio_async import PymailIOAsync
# from tests.fixtures import mock_server, pytask_io_fixture
#
#
# class TestPyMailIO:
#
#     def test_init(self):
#
#         p = PyMailIO(
#             sender_email="test_sender",
#             receiver_email="receiver_email",
#             password="test_password",
#         )
#
#         result = p.format_msg("Hello John", "This is a test message.")
#
#         print(result)
#
#         assert "Subject: Hello John" in result
#         assert "This is a test message." in result
#
#     def test_add_email_to_task_queue(self, monkeypatch):
#         p = PymailIOAsync(
#             sender_email="test_sender",
#             receiver_email="receiver_email",
#             password="test_password",
#         )
#
#         monkeypatch.setattr(smtplib, "SMTP_SSL", lambda t, y: MockServer(t, y))
#         result = p.add_email_to_task_queue("Hello John", "This is a test message.")
