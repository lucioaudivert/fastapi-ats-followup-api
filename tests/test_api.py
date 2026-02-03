def test_create_candidate(client):
    payload = {
        "name": "Ana Lopez",
        "email": "ana@example.com",
        "stage": "sourced",
    }

    response = client.post("/candidates", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["email"] == "ana@example.com"


def test_list_candidates_with_filters(client):
    client.post(
        "/candidates",
        json={
            "name": "Ana Lopez",
            "email": "ana@example.com",
            "stage": "sourced",
        },
    )
    client.post(
        "/candidates",
        json={
            "name": "Luis Perez",
            "email": "luis@example.com",
            "stage": "hired",
        },
    )

    response = client.get("/candidates", params={"stage": "hired"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["stage"] == "hired"

    response = client.get("/candidates", params={"q": "ana"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "ana@example.com"


def test_followup_flow(client):
    candidate = client.post(
        "/candidates",
        json={
            "name": "Camila Rios",
            "email": "camila@example.com",
            "stage": "interview",
        },
    ).json()

    response = client.post(
        f"/candidates/{candidate['id']}/followups",
        json={"message": "Left a voicemail", "channel": "call"},
    )
    assert response.status_code == 201

    response = client.get(f"/candidates/{candidate['id']}/followups")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["channel"] == "call"


def test_invalid_payload_returns_422(client):
    response = client.post("/candidates", json={"email": "not-an-email"})
    assert response.status_code == 422


def test_missing_candidate_returns_404(client):
    response = client.get("/candidates/9999")
    assert response.status_code == 404
