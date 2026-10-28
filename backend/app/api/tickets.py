"""Endpoints for tickets and their history (contract in KSP-20).

The five endpoints from CORE section 4 and HIST section 5 have been in /openapi.json
since KSP-20. The ones not built yet are stubs that answer 501 until the KSP issue that
builds them replaces the body. Built: POST /tickets (KSP-22, create a ticket),
GET /tickets and GET /tickets/{id} (KSP-23, list and show) and GET /tickets/{id}/history
(KSP-35, read the history). Still a stub: the status change (KSP-24).
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.errors import TICKET_NOT_FOUND
from app.schemas.tickets import ErrorResponse, HistoryEntry, StatusChange, Ticket, TicketCreate
from app.services.tickets import TicketNotFound, TicketService

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
def create_ticket(ticket: TicketCreate, session: Annotated[Session, Depends(get_session)]):
    """Create a ticket with status "new" (CORE-01). Built in KSP-22.

    Validation and trimming are done by TicketCreate before this runs, so a 422 never
    reaches the service and nothing is saved (AC5 in KSP-22).
    """
    row = TicketService(session).create(ticket)
    # The row is a SQLAlchemy object, so it is read through its attributes.
    return Ticket.model_validate(row, from_attributes=True)


@router.get("", response_model=list[Ticket])
def list_tickets(session: Annotated[Session, Depends(get_session)]):
    """List all tickets, newest first (CORE-03). No errors are declared. Built in KSP-23.

    No tickets gives 200 with [], not an error (CORE-15).
    """
    rows = TicketService(session).list()
    return [Ticket.model_validate(row, from_attributes=True) for row in rows]


# ticket_id is an int in the contract (KSP-20 decision 2). That "abc" gives 404
# instead of 422 (CORE-10, B8) is handled in KSP-21.
@router.get("/{ticket_id}", response_model=Ticket, responses=_error(404))
def get_ticket(ticket_id: int, session: Annotated[Session, Depends(get_session)]):
    """Get one ticket (CORE-04). 404 if it does not exist (CORE-10). Built in KSP-23."""
    try:
        row = TicketService(session).get(ticket_id)
    except TicketNotFound:
        # Same message as for an id that is not an integer (B8), so the frontend shows one text.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TICKET_NOT_FOUND)
    return Ticket.model_validate(row, from_attributes=True)


@router.patch("/{ticket_id}/status", response_model=Ticket, responses=_error(404, 409, 422, 503))
def change_status(ticket_id: int, change: StatusChange):
    """Change the status and write a history entry in the same transaction (HIST-02).

    404 unknown ticket (HIST-08), 409 same status as now (HIST-07),
    422 invalid status (HIST-06), 503 the history entry could not be saved (HIST-09).
    """
    _not_implemented()


@router.get("/{ticket_id}/history", response_model=list[HistoryEntry], responses=_error(404))
def get_history(ticket_id: int, session: Annotated[Session, Depends(get_session)]):
    """Get the ticket's history, oldest first (HIST-03). 404 if unknown (HIST-08). Built in KSP-35.

    A ticket without changes still has its "created" entry, so the list is never empty
    for a ticket that exists (HIST-12).
    """
    try:
        rows = TicketService(session).get_history(ticket_id)
    except TicketNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TICKET_NOT_FOUND)
    # Through HistoryEntry, so only the contract's fields are sent (no ticket_id).
    return [HistoryEntry.model_validate(row, from_attributes=True) for row in rows]
