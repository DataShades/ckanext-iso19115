

from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def examples():
    return Path(__file__).parent / "examples"
