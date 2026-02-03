from app.models import Channel, Stage
from app.schemas import CandidateCreate, FollowUpCreate
from app.services import (
    create_candidate,
    create_followup,
    get_candidate,
    list_candidates,
    list_followups,
)


def test_create_candidate(session):
    payload = CandidateCreate(
        name="Ana Lopez",
        email="ana@example.com",
        stage=Stage.sourced,
    )

    candidate = create_candidate(session, payload)

    assert candidate.id is not None
    assert candidate.email == "ana@example.com"


def test_list_candidates_filters(session):
    create_candidate(
        session,
        CandidateCreate(name="Ana Lopez", email="ana@example.com", stage=Stage.sourced),
    )
    create_candidate(
        session,
        CandidateCreate(name="Luis Perez", email="luis@example.com", stage=Stage.hired),
    )

    hired = list_candidates(session, stage=Stage.hired, query=None)
    assert len(hired) == 1
    assert hired[0].stage == Stage.hired

    filtered = list_candidates(session, stage=None, query="ana")
    assert len(filtered) == 1
    assert filtered[0].email == "ana@example.com"


def test_followup_flow(session):
    candidate = create_candidate(
        session,
        CandidateCreate(name="Mia", email="mia@example.com", stage=Stage.interview),
    )

    followup = create_followup(
        session,
        candidate.id,
        FollowUpCreate(message="Sent a reminder", channel=Channel.email),
    )
    followups = list_followups(session, candidate.id)

    assert followup.id is not None
    assert followups[0].message == "Sent a reminder"
    assert get_candidate(session, candidate.id).name == "Mia"
