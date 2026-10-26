"""Endpoints for tickets and their history (KSP-20).

The five endpoints from CORE section 4 and HIST section 5 exist here so that the
contract is complete in /openapi.json before any logic is built. Each one is a stub
that answers 501 until the KSP issue that builds it replaces the body:
POST and GET /tickets in KSP-22 to KSP-24, status change and history in KSP-33 to KSP-35.
"""

from fastapi import APIRouter, HTTPException, status

from app.schemas.tickets import ErrorResponse, HistoryEntry, StatusChange, Ticket, TicketCreate

# Shown if the frontend calls an endpoint that is not built yet (KSP-20 decision 4).
NOT_IMPLEMENTED = "Funktionen är inte klar än."

# All paths below start with /tickets and are grouped as "tickets" in /docs.
router = APIRouter(prefix="/tickets", tags=["tickets"])


def _error(*codes: int) -> dict:
    """Declare error codes with the {"detail": "..."} body for the schema.

    Declaring 422 here also replaces FastAPI's default 422, which is an English list
    of objects and breaks the error format (CORE-16, HIST-14).
    """
    return {code: {"model": ErrorResponse} for code in codes}


def _not_implemented():
    """Answer 501 with a Swedish message, in the same format as every other error."""
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=NOT_IMPLEMENTED)


# response_model sets the success body in the schema, and status_code its HTTP code.
@router.post("", status_code=status.HTTP_201_CREATED, response_model=Ticket, responses=_error(422))
def create_ticket(ticket: TicketCreate):
    """Create a ticket with status "new" (CORE-01). Built in KSP-22."""
    _not_implemented()


@router.get("", response_model=list[Ticket])
def list_tickets():
    """List all tickets, newest first (CORE-03). No errors are declared."""
    _not_implemented()


# ticket_id is an int in the contract (KSP-20 decision 2). That "abc" gives 404
# instead of 422 (CORE-10, B8) is handled in KSP-21.
@router.get("/{ticket_id}", response_model=Ticket, responses=_error(404))
def get_ticket(ticket_id: int):
    """Get one ticket (CORE-04). 404 if it does not exist (CORE-10)."""
    _not_implemented()


@router.patch("/{ticket_id}/status", response_model=Ticket, responses=_error(404, 409, 422, 503))
def change_status(ticket_id: int, change: StatusChange):
    """Change the status and write a history entry in the same transaction (HIST-02).

    404 unknown ticket (HIST-08), 409 same status as now (HIST-07),
    422 invalid status (HIST-06), 503 the history entry could not be saved (HIST-09).
    """
    _not_implemented()


@router.get("/{ticket_id}/history", response_model=list[HistoryEntry], responses=_error(404))
def get_history(ticket_id: int):
    """Get the ticket's history, oldest first (HIST-03). 404 if unknown (HIST-08)."""
    _not_implemented()
