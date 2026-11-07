import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Use a separate in-memory database for testing
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Reset database before each test
@pytest.fixture
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# Helper function to register a customer
def create_test_customer(client):
    response = client.post(
        "/customers",
        json={
            "full_name": "Rahul Sharma",
            "email": "rahul@example.com",
            "phone": "9876543210"
        }
    )
    return response


# Test 1: Home route
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Running"


# Test 2: Customer registration
def test_create_customer(client):
    response = create_test_customer(client)

    assert response.status_code == 201
    assert response.json()["full_name"] == "Rahul Sharma"


# Test 3: Prevent duplicate customers
def test_duplicate_customer(client):
    create_test_customer(client)
    response = create_test_customer(client)

    assert response.status_code == 409


# Test 4: Loan application
def test_create_loan(client):
    customer = create_test_customer(client).json()

    response = client.post(
        "/loans",
        json={
            "customer_id": customer["id"],
            "property_value": 5000000,
            "requested_amount": 3500000,
            "annual_interest_rate": 8.5,
            "tenure_months": 240,
            "purpose": "HOME_PURCHASE"
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "PENDING"


# Test 5: Reject loan amount greater than property value
def test_loan_amount_exceeds_property_value(client):
    customer = create_test_customer(client).json()

    response = client.post(
        "/loans",
        json={
            "customer_id": customer["id"],
            "property_value": 2000000,
            "requested_amount": 3000000,
            "annual_interest_rate": 8.5,
            "tenure_months": 240,
            "purpose": "HOME_PURCHASE"
        }
    )

    assert response.status_code == 400


# Test 6: Update loan status
def test_update_loan_status(client):
    customer = create_test_customer(client).json()

    loan = client.post(
        "/loans",
        json={
            "customer_id": customer["id"],
            "property_value": 5000000,
            "requested_amount": 3500000,
            "annual_interest_rate": 8.5,
            "tenure_months": 240,
            "purpose": "HOME_PURCHASE"
        }
    ).json()

    response = client.patch(
        f"/loans/{loan['id']}/status",
        json={"status": "UNDER_REVIEW"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "UNDER_REVIEW"


# Test 7: EMI calculation
def test_calculate_emi(client):
    response = client.get(
        "/calculate-emi",
        params={
            "principal": 3500000,
            "annual_rate": 8.5,
            "tenure_months": 240
        }
    )

    assert response.status_code == 200
    assert response.json()["monthly_emi"] > 0


# Test 8: Invalid EMI input
def test_invalid_emi(client):
    response = client.get(
        "/calculate-emi",
        params={
            "principal": -1000,
            "annual_rate": 8.5,
            "tenure_months": 240
        }
    )

    assert response.status_code == 400