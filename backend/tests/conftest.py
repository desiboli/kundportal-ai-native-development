import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def database_url(tmp_path):
    """Varje test får en egen SQLite-fil som tas bort efteråt."""
    return f"sqlite:///{tmp_path / 'test.db'}"


@pytest.fixture
def client(database_url):
    # `with` kör appens uppstart och nedstängning (lifespan), precis som uvicorn gör.
    with TestClient(create_app(database_url)) as test_client:
        yield test_client
