"""Pydantic schemas for request/response payloads."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .models import Channel, Stage


class CandidateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    stage: Stage = Stage.sourced


class CandidateRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    stage: Stage
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FollowUpCreate(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    channel: Channel = Channel.email


class FollowUpRead(BaseModel):
    id: int
    candidate_id: int
    message: str
    channel: Channel
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
