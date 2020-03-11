import pytest


@pytest.fixture
def pytask_io_fixture():
    class MockPyTaskIO:
        def __init__(self, *args, **kwargs):
            pass

        def run(self):
            pass

        def stop(self):
            pass

        def add_task(self, callable_uow, subject, body):
            return {

            }

    return MockPyTaskIO


@pytest.fixture
def mock_server():
    class MockServer:
        def __init__(self, t, y):
            pass

        def login(self, t, y):
            pass

        def send_message(self, t, y, u):
            pass

        def quit(self):
            pass
    return MockServer
