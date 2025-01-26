import requests
import pytest

@pytest.fixture
def credentials_empty():
    return {}

@pytest.fixture
def credentials_wrong_user():
    return {
        "username": "noSuchUser",
        "password": "noSuchUser"
    }

@pytest.fixture
def credentials_experied():
    return {
        "username": "user_expired",
        "password": "password_expired"
    }

@pytest.fixture
def credentials_valid():
    return {
        "username": "user123",
        "password": "password123"
    }

@pytest.fixture
def data_right():
    return {
        'GRE_Score': 200,
        'TOEFL_Score': 100,
        'University_Rating': 4,
        'SOP': 3,
        'LOR': 2,
        'CGPA': 5,
        'Research': 1,
    }

@pytest.fixture
def data_wrong():
    return {
        'GRE_Score': 200,
        'TOEFL_Score': 100,
        'University_Rating': 4,
        'SOP': 3,
        'LOR': 2,
        'CGPA': 5,
    }

def test_no_credential(credentials_empty, data_right):
    token, status_code, detail = function_to_test(credentials_empty, data_right)
    assert not token and status_code == 401 and detail == "Invalid token"

def test_wrong_credential(credentials_wrong_user, data_right):
    token, status_code, detail = function_to_test(credentials_wrong_user, data_right)
    assert not token and status_code == 401 and detail == "Invalid token"

def test_expired_credential(credentials_experied, data_right):
    token, status_code, detail = function_to_test(credentials_experied, data_right)
    assert token and status_code == 401 and detail == "Token has expired"

def test_valid_credential_wrong_data(credentials_valid, data_wrong):
    token, status_code, detail = function_to_test(credentials_valid, data_wrong)
    assert token and status_code == 422 and detail == "invalid data"

def test_valid_credential_right_data(credentials_valid, data_right):
    token, status_code, detail = function_to_test(credentials_valid, data_right)
    assert token and status_code == 200 and detail == "0.9676999999999991"
 


def function_to_test(credentials, data):
    # The URL of the login and prediction endpoints
    login_url = "http://127.0.0.1:3000/login"
    predict_url = "http://127.0.0.1:3000/v1/models/rf_regressor/predict"

    # Send a POST request to the login endpoint
    login_response = requests.post(
        login_url,
        headers={"Content-Type": "application/json"},
        json=credentials
    )
    

    # Check if the login was successful
    if login_response.status_code == 200:
        token = login_response.json().get("token")
        print("Token JWT obtenu:", token)

        # Send a POST request to the prediction
        response = requests.post(
            predict_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=data
        )

        # return token, JSONResponse(status_code=response.status_code, content={"detail": response.text})
        if response.status_code == 200:
            return token, response.status_code, str(response.json()['prediction'][0])
        else:
            return token, response.status_code, response.json()['detail']
    else:
        return token, login_response.status_code, login_response.json()['detail']
