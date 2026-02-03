"""SQLModel models for candidates and follow-ups."""

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class Stage(StrEnum):
    sourced = "sourced"
    interview = "interview"
    offered = "offered"
    hired = "hired"
    rejected = "rejected"


class Channel(StrEnum):
    email = "email"
    whatsapp = "whatsapp"
    call = "call"
    other = "other"


class Candidate(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    stage: Stage = Field(default=Stage.sourced, index=True)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)

    followups: list["FollowUp"] = Relationship(back_populates="candidate")


class FollowUp(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="candidate.id", index=True)
    message: str = Field(min_length=1, max_length=1000)
    channel: Channel = Field(default=Channel.email)
    created_at: datetime = Field(default_factory=utc_now, nullable=False)

    candidate: Candidate | None = Relationship(back_populates="followups")
