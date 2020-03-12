import pytest

from tests.mock_data import payload_one

@pytest.fixture
def pytask_io_fixture():
    class MockPyTaskIO:
        def __init__(self, *args, **kwargs):
            pass

        def init(self, *args, **kwargs):
            pass

        def run(self):
            pass

        def stop(self):
            pass

        def add_task(self, callable_uow, subject, body):
            return payload_one

    return MockPyTaskIO()


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
