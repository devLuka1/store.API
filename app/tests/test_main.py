from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_product():
    response = client.post("/products/", json={"name": "Laptop", "description": "Gaming Laptop", "price": 1200.0})
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"
    assert response.json()["description"] == "Gaming Laptop"
    assert response.json()["price"] == 1200.0

def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"

def test_update_product():
    response = client.put("/products/1", json={"name": "Updated Laptop", "description": "Updated Gaming Laptop", "price": 1500.0})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Laptop"

def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Laptop"
