from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_status(client: TestClient) -> None:
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "content_tool"
    assert data["status"] == "running"
