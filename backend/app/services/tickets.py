"""TicketService: the rules for tickets and where each transaction starts and ends (KSP-22).

Creating a ticket sets status "new" (CORE-01) and the creation time in UTC. The history
entry "created" (HIST-01) is added here in the same transaction in KSP-34.
"""

from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.tickets import TicketRow
from app.repositories.tickets import TicketRepository
from app.schemas.tickets import Status, TicketCreate

# API conventions section 3: UTC, always with microseconds, e.g. 2026-10-25T09:00:00.000000Z.
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def utc_now() -> datetime:
    """The real clock. Tests can pass another one (architecture: replaceable clock)."""
    return datetime.now(UTC)


class TicketService:
    """Creates tickets. One service per request, with that request's session."""

    def __init__(self, session: Session, clock: Callable[[], datetime] = utc_now):
        self.session = session
        self.tickets = TicketRepository(session)
        self.clock = clock

    def create(self, data: TicketCreate) -> TicketRow:
        """Save a new ticket with status "new". The input is already validated and trimmed."""
        row = TicketRow(
            title=data.title,
            description=data.description,
            category=data.category,
            priority=data.priority,
            # CORE-01: the server always sets the first status, the client cannot (CORE-09).
            status=Status.NEW,
            created_at=self.clock().strftime(TIMESTAMP_FORMAT),
        )
        self.tickets.add(row)
        # One commit for the whole operation. KSP-34 adds the history entry before it.
        self.session.commit()
        return row
