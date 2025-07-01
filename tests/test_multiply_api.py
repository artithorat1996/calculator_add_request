import requests
import pytest

BASE_URL = "http://localhost/TestingAPI"
LOGIN_URL = f"{BASE_URL}/api/Login/IsAutehticatedUser"
MULTIPLY_URL = f"{BASE_URL}/api/arithmetic/multiply"

# Fixture to get auth token
@pytest.fixture
def auth_token():
    login_payload = {
        "UserId": "arti",
        "Password": "arti@123"
    }
    headers = {"Content-Type": "application/json"}
    res = requests.post(LOGIN_URL, json=login_payload, headers=headers)
    assert res.status_code == 200
    return res.json().get("Token")

# ✅ Positive test
@pytest.mark.parametrize("first, second, expected", [
    (8, 7, 56),
    (0, 10, 0),
    (-4, 5, -20),
    (-3, -6, 18),
    (999, 888, 887112)
])
def test_multiply_positive(auth_token, first, second, expected):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "First_Value": first,
        "Second_Value": second
    }
    res = requests.post(MULTIPLY_URL, json=payload, headers=headers)
    assert res.status_code == 200
    assert res.json() == expected

#  Negative: Missing parameters
@pytest.mark.parametrize("payload", [
    {"Second_Value": 5},  # Missing First_Value
    {"First_Value": 5},   # Missing Second_Value
    {},                   # Both missing
])
def test_multiply_missing_fields(auth_token, payload):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    res = requests.post(MULTIPLY_URL, json=payload, headers=headers)
    assert res.status_code == 200  # Depending on your API's error codes

#  Negative: Invalid input types

def test_multiply_invalid_input(auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    invalid_payload = {
        "First_Value": "a",
        "Second_Value": 7
    }
    invalid_payload_res = requests.post(MULTIPLY_URL, json=invalid_payload, headers=headers)
    assert invalid_payload_res.status_code in [400, 422]

#  Negative: No token or invalid token
def test_multiply_without_token():
    headers = {
        "Content-Type": "application/json"
    }
    payload = {"First_Value": 8, "Second_Value": 7}
    res = requests.post(MULTIPLY_URL, json=payload, headers=headers)
    assert res.status_code == 401

def test_multiply_with_invalid_token():
    headers = {
        "Authorization": "Bearer invalidtoken123",
        "Content-Type": "application/json"
    }
    payload = {"First_Value": 8, "Second_Value": 7}
    res = requests.post(MULTIPLY_URL, json=payload, headers=headers)
    assert res.status_code == 401
