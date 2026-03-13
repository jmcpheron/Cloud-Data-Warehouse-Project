from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def mock_cursor():
    return MagicMock()


@pytest.fixture()
def mock_conn():
    return MagicMock()
