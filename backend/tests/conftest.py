from unittest.mock import MagicMock, patch
import pytest

from ai_assistant.core.embedders import MockEmbedder


@pytest.fixture(autouse=True)
def mock_db_connection_for_api_tests():
    """
    Test Infrastructure Fixture:
    Mocks PostgreSQL connection during test suite execution so API and lifespan tests
    run deterministically without requiring a live PostgreSQL instance.
    Production code in main.py remains 100% fail-fast and explicit.
    """
    with patch("ai_assistant.core.vector_stores.postgresql_vector_store.register_vector"), \
        patch("ai_assistant.core.vector_stores.postgresql_vector_store.psycopg.connect") as mock_connect:
        mock_conn = MagicMock()
        cursor = mock_conn.cursor.return_value.__enter__.return_value
        cursor.fetchall.return_value = []
        mock_connect.return_value = mock_conn
        yield mock_connect
