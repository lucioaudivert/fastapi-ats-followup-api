"""Business logic for candidate and follow-up workflows."""

from sqlalchemy import func, or_
from sqlmodel import Session, select

from .models import Candidate, FollowUp, Stage
from .schemas import CandidateCreate, FollowUpCreate


class NotFoundError(Exception):
    """Raised when a requested entity cannot be found."""


def create_candidate(session: Session, payload: CandidateCreate) -> Candidate:
    candidate = Candidate(**payload.model_dump())
    session.add(candidate)
    session.commit()
    session.refresh(candidate)
    return candidate


def list_candidates(
    session: Session,
    stage: Stage | None = None,
    query: str | None = None,
) -> list[Candidate]:
    statement = select(Candidate)

    if stage is not None:
        statement = statement.where(Candidate.stage == stage)

    if query:
        normalized = query.strip().lower()
        if normalized:
            like_value = f"%{normalized}%"
            statement = statement.where(
                or_(
                    func.lower(Candidate.name).like(like_value),
                    func.lower(Candidate.email).like(like_value),
                )
            )

    statement = statement.order_by(Candidate.created_at.desc())
    return list(session.exec(statement))


def get_candidate(session: Session, candidate_id: int) -> Candidate:
    candidate = session.get(Candidate, candidate_id)
    if candidate is None:
        raise NotFoundError("Candidate not found")
    return candidate


def create_followup(
    session: Session,
    candidate_id: int,
    payload: FollowUpCreate,
) -> FollowUp:
    get_candidate(session, candidate_id)
    followup = FollowUp(candidate_id=candidate_id, **payload.model_dump())
    session.add(followup)
    session.commit()
    session.refresh(followup)
    return followup


def list_followups(session: Session, candidate_id: int) -> list[FollowUp]:
    get_candidate(session, candidate_id)
    statement = (
        select(FollowUp)
        .where(FollowUp.candidate_id == candidate_id)
        .order_by(FollowUp.created_at.desc())
    )
    return list(session.exec(statement))
