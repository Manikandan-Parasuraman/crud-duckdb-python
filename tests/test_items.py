import pytest
from fastapi.testclient import TestClient

def test_create_item(client: TestClient):
    response = client.post(
        "/api/v1/items/",
        json={"title": "Test Item", "description": "A test description", "price": 10.5}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Item"
    assert "id" in data

def test_read_items(client: TestClient):
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1

def test_read_item(client: TestClient):
    # First, create one
    create_res = client.post(
        "/api/v1/items/",
        json={"title": "Item to Get", "price": 5.0}
    )
    item_id = create_res.json()["id"]
    
    # Then read it
    res = client.get(f"/api/v1/items/{item_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Item to Get"

def test_update_item(client: TestClient):
    create_res = client.post(
        "/api/v1/items/",
        json={"title": "Item to Update", "price": 1.0}
    )
    item_id = create_res.json()["id"]
    
    res = client.put(
        f"/api/v1/items/{item_id}",
        json={"title": "Updated Item Name", "price": 100.0}
    )
    assert res.status_code == 200
    assert res.json()["title"] == "Updated Item Name"
    assert res.json()["price"] == 100.0

def test_delete_item(client: TestClient):
    create_res = client.post(
        "/api/v1/items/",
        json={"title": "Item to Delete", "price": 0.0}
    )
    item_id = create_res.json()["id"]
    
    # Delete
    del_res = client.delete(f"/api/v1/items/{item_id}")
    assert del_res.status_code == 204
    
    # Verify it's gone
    res = client.get(f"/api/v1/items/{item_id}")
    assert res.status_code == 404
