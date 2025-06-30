import pytest
import requests


add_url = "http://localhost/TestingAPI/api/arithmetic/add?"
auth_url = "http://localhost/TestingAPI/api/Login/IsAutehticatedUser"

@pytest.fixture
def auth_token():
    login_payload = {
        "UserId": "arti",
        "Password": "arti@123"
    }
    header = {"Content-Type":"application/json"}
    res = requests.post(auth_url, json=login_payload, headers=header)
    assert res.status_code == 200
    return res.json().get("Token")

@pytest.mark.parametrize("first, second, expected",[
                (7,4,11),
                (-1,-3,-4),
                (0,4,4),
                 (4,4,8)
])
def test_addition_postive(auth_token,first,second,expected):
    param = {
    "first_value":first,
    "second_value":second
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(add_url, params=param, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected

@pytest.mark.parametrize("first, second",[
    (2.2,4.5),
    ("a",2),
    ("","$#"),
    ("","")
])
def test_addition_negative(auth_token,first,second):
    param = {
        "first_value": first,
        "second_value": second
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(add_url, params=param, headers=headers)
    assert response.status_code == 400

def test_invalid_auth_token():
    param = {
        "first_value": 8,
        "second_value": 4
    }
    headers = {
        "Authorization": "Bearer invalid456tokenggf",
        "Content-Type": "application/json"
    }
    response = requests.get(add_url, params=param, headers=headers)
    assert response.status_code == 401






