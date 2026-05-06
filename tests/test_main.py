import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)



def test_auth():
    unique_id = str(uuid.uuid4())[:8]

    client.post("/users/auth/register",json={"username" : f"testbot{unique_id}",
                                                        "email" : f"test{unique_id}@gmail.com",
                                                        "password" : "12345678"})


    response = client.post("/users/auth/login", json={"identifier" : f"testbot{unique_id}",
                                                      "password" : "12345678"})
    

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_duplicated_user():

    unique_id = str(uuid.uuid4())[:8]
    
    username = f"testbot_{unique_id}"
    email = f"bot{unique_id}@gmail.com"

    client.post("/users/auth/register", json={"username" : username,
                                                         "email" : email,
                                                         "password" : "12345678"})
    
    other_user = client.post("/users/auth/register", json={"username" : username,
                                                         "email" : email,
                                                         "password" : "12345678"})

    assert other_user.status_code == 401


def test_create_ticket():

    unique_id = str(uuid.uuid4())[:8]

    username = f"ticket_{unique_id}"
    email = f"ticket{unique_id}@gmail.com"


    register = client.post("/users/auth/register", json={"username" : username,
                                              "email" : email,
                                              "password" : "12345678"})
    
    assert register.status_code == 200

    user = client.post("/users/auth/login", json={"identifier" : username,
                                           "password" : "12345678"})
    
    assert user.status_code == 200

    token = user.json()["access_token"]

    headers = {"Authorization" : f"Bearer {token}"}

    ticket = client.post("/tickets", json={"title" : "Test Ticket",
                                           "description" : "Test for creation of tickets"}, headers=headers)

    assert ticket.status_code == 200




