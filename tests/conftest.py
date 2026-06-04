"""Pytest configuration and fixtures for FastAPI tests"""

import pytest
from starlette.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for the FastAPI app.
    Each test gets a fresh client with the app's current state.
    """
    return TestClient(app)
