import pytest

# ---------------------------------------------------------------------------
# Casos positivos: comportamiento esperado del CRUD
# ---------------------------------------------------------------------------


def test_create_item_returns_201_and_body(api_client):
    payload = {"name": "teclado mecanico", "price": 49.99}

    response = api_client.post("/items", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["price"] == payload["price"]
    assert body["in_stock"] is True  # valor por defecto
    assert isinstance(body["id"], int)


def test_get_item_by_id_returns_created_item(api_client):
    created = api_client.post("/items", json={"name": "raton", "price": 15.5}).json()

    response = api_client.get(f"/items/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_list_items_includes_created_item(api_client):
    created = api_client.post("/items", json={"name": "monitor", "price": 199.0}).json()

    response = api_client.get("/items")

    assert response.status_code == 200
    ids_in_list = [item["id"] for item in response.json()]
    assert created["id"] in ids_in_list


def test_update_item_overwrites_fields(api_client):
    created = api_client.post("/items", json={"name": "webcam", "price": 30.0}).json()

    response = api_client.put(
        f"/items/{created['id']}",
        json={"name": "webcam HD", "price": 45.0, "in_stock": False},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "webcam HD"
    assert body["price"] == 45.0
    assert body["in_stock"] is False
    assert body["id"] == created["id"]  # el id no cambia


def test_delete_item_removes_it(api_client):
    created = api_client.post(
        "/items", json={"name": "auriculares", "price": 20.0}
    ).json()

    delete_response = api_client.delete(f"/items/{created['id']}")
    get_response = api_client.get(f"/items/{created['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


# ---------------------------------------------------------------------------
# Casos negativos: validacion y errores
# ---------------------------------------------------------------------------


def test_get_nonexistent_item_returns_404(api_client):
    response = api_client.get("/items/999999")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_update_nonexistent_item_returns_404(api_client):
    response = api_client.put("/items/999999", json={"name": "x", "price": 1.0})

    assert response.status_code == 404


def test_delete_nonexistent_item_returns_404(api_client):
    response = api_client.delete("/items/999999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"price": 10.0},  # falta name
        {"name": "sin precio"},  # falta price
        {"name": "", "price": 10.0},  # name vacio
        {"name": "precio cero", "price": 0},  # price no > 0
        {"name": "precio negativo", "price": -5},  # price negativo
    ],
)
def test_create_item_with_invalid_payload_returns_422(api_client, payload):
    response = api_client.post("/items", json=payload)

    assert response.status_code == 422
