"""Reading and writing tickets (KSP-22). Commit is left to the service."""

from sqlalchemy.orm import Session

from app.models.tickets import TicketRow


class TicketRepository:
    """Ticket rows in the database for one session."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, row: TicketRow) -> TicketRow:
        """Add a new ticket. flush() gives it an id, but nothing is saved until commit."""
        self.session.add(row)
        self.session.flush()
        return row
