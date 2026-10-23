from collections.abc import Iterator
from pathlib import Path

from fastapi import Request
from sqlalchemy import Engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    """Alla tabeller ärver från Base så att create_all hittar dem."""


def ensure_sqlite_directory(engine: Engine) -> None:
    """SQLite skapar filen men inte mappen den ska ligga i."""
    url = make_url(str(engine.url))
    if url.get_backend_name() == "sqlite" and url.database not in (None, "", ":memory:"):
        Path(url.database).parent.mkdir(parents=True, exist_ok=True)


def get_session(request: Request) -> Iterator[Session]:
    """FastAPI-beroende: en session per anrop, stängs när anropet är klart."""
    with request.app.state.session_factory() as session:
        yield session
