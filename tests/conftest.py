import pytest
from pathlib import Path


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def config_dir(project_root: Path) -> Path:
    """Return the config directory path."""
    return project_root / "config"


@pytest.fixture
def data_dir(project_root: Path) -> Path:
    """Return the data directory path."""
    return project_root / "data"


@pytest.fixture
def tmp_output(tmp_path: Path) -> Path:
    """Return a temporary output directory for test artifacts."""
    output = tmp_path / "output"
    output.mkdir()
    return output
