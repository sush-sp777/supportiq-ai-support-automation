from pydantic import BaseModel
from datetime import datetime
from backend.app.tickets.models import TicketCategory, TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    title: str
    description: str
    category: TicketCategory


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime

    class Config:
        orm_mode = True
