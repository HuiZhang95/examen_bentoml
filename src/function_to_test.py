import requests

def function_to_test(credentials, data)
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

        return JSONResponse(status_code=response.status_code, content={"detail": response.text})
    else:
        return JSONResponse(status_code=response.status_code, content={"detail": login_response.text})