import os
import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.database import SessionLocal, engine
from api import models

# Use a test token for authentication (replace with real JWT in production)
TEST_TOKEN = "test-token"

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create tables before tests and drop after.
    """
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Provide a transactional scope for each test.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="module")
def client():
    """
    FastAPI test client.
    """
    return TestClient(app)

def auth_headers():
    """
    Return headers with test token for authentication.
    """
    return {"Authorization": f"Bearer {TEST_TOKEN}"}

def test_health_check(client):
    """
    Test health endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_product(client, db_session):
    """
    Test product creation.
    """
    payload = {
        "name": "Test Product",
        "description": "A product for testing."
    }
    response = client.post("/products/", json=payload, headers=auth_headers())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert "id" in data

def test_create_duplicate_product(client, db_session):
    """
    Test duplicate product creation fails.
    """
    payload = {
        "name": "Duplicate Product",
        "description": "First instance."
    }
    # First creation should succeed
    response1 = client.post("/products/", json=payload, headers=auth_headers())
    assert response1.status_code == 201

    # Second creation should fail
    response2 = client.post("/products/", json=payload, headers=auth_headers())
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"]

def test_list_products(client, db_session):
    """
    Test listing products.
    """
    # Create two products
    client.post("/products/", json={"name": "Product1", "description": "Desc1"}, headers=auth_headers())
    client.post("/products/", json={"name": "Product2", "description": "Desc2"}, headers=auth_headers())

    response = client.get("/products/", headers=auth_headers())
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) >= 2

def test_get_product_by_id(client, db_session):
    """
    Test retrieving a product by ID.
    """
    # Create a product
    response = client.post("/products/", json={"name": "GetById", "description": "Desc"}, headers=auth_headers())
    product_id = response.json()["id"]

    # Retrieve by ID
    get_response = client.get(f"/products/{product_id}", headers=auth_headers())
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == product_id
    assert data["name"] == "GetById"

def test_get_product_not_found(client, db_session):
    """
    Test retrieving a non-existent product.
    """
    response = client.get("/products/999999", headers=auth_headers())
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_product(client, db_session):
    """
    Test updating a product.
    """
    # Create a product
    response = client.post("/products/", json={"name": "UpdateMe", "description": "Old"}, headers=auth_headers())
    product_id = response.json()["id"]

    # Update product
    update_payload = {"name": "UpdatedName", "description": "New description"}
    update_response = client.put(f"/products/{product_id}", json=update_payload, headers=auth_headers())
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["name"] == "UpdatedName"
    assert updated["description"] == "New description"

def test_update_product_not_found(client, db_session):
    """
    Test updating a non-existent product.
    """
    update_payload = {"name": "NoProduct", "description": "NoDesc"}
    response = client.put("/products/999999", json=update_payload, headers=auth_headers())
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_delete_product(client, db_session):
    """
    Test deleting a product.
    """
    # Create a product
    response = client.post("/products/", json={"name": "DeleteMe", "description": "To be deleted"}, headers=auth_headers())
    product_id = response.json()["id"]

    # Delete product
    delete_response = client.delete(f"/products/{product_id}", headers=auth_headers())
    assert delete_response.status_code == 200
    assert "deleted successfully" in delete_response.json()["detail"]

    # Ensure product is gone
    get_response = client.get(f"/products/{product_id}", headers=auth_headers())
    assert get_response.status_code == 404

def test_delete_product_not_found(client, db_session):
    """
    Test deleting a non-existent product.
    """
    response = client.delete("/products/999999", headers=auth_headers())
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_auth_required(client):
    """
    Test endpoints require authentication.
    """
    payload = {"name": "NoAuth", "description": "Should fail"}
    response = client.post("/products/", json=payload)
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]