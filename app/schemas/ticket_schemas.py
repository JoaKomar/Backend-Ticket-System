from pydantic import BaseModel, Field
from enum import Enum

#I use Enum to set types of Status on the tickets
class TicketStatus(str, Enum):
    pending = "pending"
    in_process = "in_process"
    completed = "completed"

#Ticket Schema
class TicketUser(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=15, max_length=1000)

class Ticket(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=15, max_length=1000)
    status: TicketStatus