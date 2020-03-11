import pytest


@pytest.fixture
def redis_fixture():
    class MockRedis:
        pass
    return MockRedis


@pytest.fixture
def pytask_io_fixture():
    class MockPyTaskIO:
        pass

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
