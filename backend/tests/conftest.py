import os
from pathlib import Path
import pytest

# NOTE: we set DATABASE_URL per-test (tmp file) inside the `client` fixture so the
# application's SQLAlchemy engine picks it up on import. This gives each test a
# hermetic SQLite DB and much faster, deterministic runs.

from app.db.base import Base

from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def clean_db(client, tmp_path):
    """Create / destroy DB for the currently configured app engine.

    Depends on `client` to ensure the application's DB engine has been
    initialized using the per-test DATABASE_URL.
    """
    # engine is created when the app (and app.db.session) is imported by the
    # `client` fixture, so import it here to get the same engine instance.
    from app.db.session import engine

    # ensure file-based sqlite DB path (client fixture set the env var)
    db_file = tmp_path / 'test.db'
    if db_file.exists():
        db_file.unlink()

    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)
        if db_file.exists():
            db_file.unlink()


@pytest.fixture()
def client(tmp_path):
    """Create a TestClient with a unique sqlite DB for the test.

    Sets `DATABASE_URL` before importing the application so the app's
    SQLAlchemy engine will use the per-test DB file.
    """
    db_file = tmp_path / 'test.db'
    os.environ['DATABASE_URL'] = f"sqlite:///{db_file}"

    # import the app after DATABASE_URL is set
    from app.main import app
    return TestClient(app)
