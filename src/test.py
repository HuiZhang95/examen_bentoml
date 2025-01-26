import requests

# The URL of the login and prediction endpoints
login_url = "http://127.0.0.1:3000/login"
predict_url = "http://127.0.0.1:3000/v1/models/rf_regressor/predict"

# Données de connexion
credentials = {
    "username": "user123",
    "password": "password123"
}

# credentials = {
#     "username": "user_expired",
#     "password": "password_expired"
# }


# credentials = {
#     "username": "uwser123",
#     "password": "password123"
# }

# credentials = {}

# Send a POST request to the login endpoint
login_response = requests.post(
    login_url,
    headers={"Content-Type": "application/json"},
    json=credentials
)
print(login_response.status_code)

# Check if the login was successful
if login_response.status_code == 200:
    token = login_response.json().get("token")
    print("Token JWT obtenu:", token)

    # Data to be sent to the prediction endpoint
    data = {
        'GRE_Score': 200,
        'TOEFL_Score': 100,
        'University_Rating': 4,
        'SOP': 3,
        'LOR': 2,
        'CGPA': 5,
        'Research': 1,
    }

    # Send a POST request to the prediction
    response = requests.post(
        predict_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        json=data
    )

    print(f"Response status code: {response.status_code}. Réponse de l'API de prédiction:{response.text}")

else:
    print(f"Response status code: {login_response.status_code}. Erreur lors de la connexion:", login_response.text)