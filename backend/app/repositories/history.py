"""Writing history entries (KSP-33). Commit is left to the service.

There is deliberately no update or delete: history entries are never changed (AGENTS.md).
Reading the history for the API comes in KSP-35 (GET /tickets/{id}/history).
"""

from sqlalchemy.orm import Session

from app.models.history import HistoryRow


class HistoryRepository:
    """History rows in the database for one session."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, row: HistoryRow) -> HistoryRow:
        """Add an entry. Nothing is saved until the service commits."""
        self.session.add(row)
        self.session.flush()
        return row
