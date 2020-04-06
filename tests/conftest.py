from flaskr.app import create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    test_app = app.test_client()
    return test_app
