def test_health_check(api_client):
    response = api_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
