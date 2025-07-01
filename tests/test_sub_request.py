import pytest
import requests



@pytest.fixture
def auth_token():
    payload = {
           "UserId": "arti",
            "Password": "arti@123"
    }
    header = {"Content-Type":"application/json"}
    auth_url = "http://localhost/TestingAPI/api/Login/IsAutehticatedUser"
    resp = requests.post(auth_url, headers=header,json=payload)
    assert resp.status_code == 200
    return resp.json().get("Token")

url = "http://localhost/TestingAPI/api/arithmetic/subtract?"
@pytest.mark.parametrize("first, second, expected",[
                (7,4,3),
                (-1,-3,2),
                (0,4,-4),
                 (4,4,0)
])
def test_substract_api(auth_token,first,second,expected):
    param = {
    "first_value":first,
    "second_value":second
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, params=param, headers=headers)
    assert response.status_code == 200
    assert response.json() == expected

@pytest.mark.parametrize("first, second",[
    (2.2,4.5),
    ("a",2),
    ("","$#"),
    ("","")
])
def test_substract_float(auth_token,first,second):
    param = {
        "first_value": first,
        "second_value": second
    }
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, params=param, headers=headers)
    assert response.status_code == 400

def test_sub_invalid_token():
    header = {
        "Authorization": "Bearer invalid123token",
        "content_type": "Application/json"
    }
    payload = {"first_value":5, "second_value":4}
    response = requests.get(url,json=payload,headers=header)
    assert response.status_code == 200