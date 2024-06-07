import pytest
from fastapi.testclient import TestClient

from main import create_app


@pytest.fixture(scope="session")
def rate_limit_value() -> int:
    return 50


@pytest.fixture(scope="session")
def _rate_limit_str(rate_limit_value: int) -> str:
    return f"{rate_limit_value}/minute"


@pytest.fixture
def testing_app(_rate_limit_str: str) -> TestClient:
    app = create_app(_rate_limit_str)
    testing_app = TestClient(app)
    return testing_app
