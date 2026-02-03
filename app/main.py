"""FastAPI application entrypoint."""

from __future__ import annotations

import logging

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Session

from .db import get_session, init_db
from .models import Stage
from .schemas import CandidateCreate, CandidateRead, FollowUpCreate, FollowUpRead
from .services import (NotFoundError, create_candidate, create_followup,
                       get_candidate, list_candidates, list_followups)
from .settings import settings

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ATS Follow-up API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    logger.info("Database initialized")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/candidates",
    response_model=CandidateRead,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate_endpoint(
    payload: CandidateCreate,
    session: Session = Depends(get_session),
) -> CandidateRead:
    candidate = create_candidate(session, payload)
    logger.info("Candidate created", extra={"candidate_id": candidate.id})
    return candidate


@app.get("/candidates", response_model=list[CandidateRead])
def list_candidates_endpoint(
    stage: Stage | None = Query(default=None),
    q: str | None = Query(default=None, min_length=1),
    session: Session = Depends(get_session),
) -> list[CandidateRead]:
    return list_candidates(session, stage=stage, query=q)


@app.get("/candidates/{candidate_id}", response_model=CandidateRead)
def get_candidate_endpoint(
    candidate_id: int,
    session: Session = Depends(get_session),
) -> CandidateRead:
    try:
        return get_candidate(session, candidate_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post(
    "/candidates/{candidate_id}/followups",
    response_model=FollowUpRead,
    status_code=status.HTTP_201_CREATED,
)
def create_followup_endpoint(
    candidate_id: int,
    payload: FollowUpCreate,
    session: Session = Depends(get_session),
) -> FollowUpRead:
    try:
        followup = create_followup(session, candidate_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    logger.info(
        "Follow-up created",
        extra={"candidate_id": candidate_id, "followup_id": followup.id},
    )
    return followup


@app.get("/candidates/{candidate_id}/followups", response_model=list[FollowUpRead])
def list_followups_endpoint(
    candidate_id: int,
    session: Session = Depends(get_session),
) -> list[FollowUpRead]:
    try:
        return list_followups(session, candidate_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
