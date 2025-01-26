import numpy as np
import bentoml
from bentoml.io import NumpyNdarray, JSON
from pydantic import BaseModel, Field, ValidationError
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "your_jwt_secret_key_here"
JWT_ALGORITHM = "HS256"

# User credentials for authentication
USERS = {
    "user123": "password123",
    "user456": "password456",
    "user_expired": "password_expired"
}

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/v1/models/rf_regressor/predict":
            # validate JWT token
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            request.state.user = payload.get("sub")

            # valide inputmodel consistency
            if request.method == "POST":
                try:
                    # Read and parse the request body
                    body = await request.json()
                    # Validate the data using InputModel
                    InputModel(**body)
                except ValidationError as ve:
                    # Return a detailed error response if validation fails
                    return JSONResponse(status_code=422,content={"detail": "invalid data"})#ve.errors()})
                except Exception as e:
                    # Handle unexpected issues in reading or processing the request
                    return JSONResponse(status_code=500,content={"detail": f"Failed to parse request: {str(e)}"},)


        response = await call_next(request)
        return response
        


# Pydantic model to validate input data
class InputModel(BaseModel):
    GRE_Score: int
    TOEFL_Score: int
    University_Rating: int
    SOP: float
    LOR: float
    CGPA: float
    Research: int

# Get the model from the Model Store
exam_rf_runner = bentoml.sklearn.get("exam_rf:latest").to_runner()

# Create a service API
rf_service = bentoml.Service("rf_exam_service", runners=[exam_rf_runner])

# Add the JWTAuthMiddleware to the service
rf_service.add_asgi_middleware(JWTAuthMiddleware)

# Create an API endpoint for the service
@rf_service.api(input=JSON(), output=JSON())
def login(credentials: dict) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in USERS and USERS[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        return {"token": None}
        # return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})


# Create an API endpoint for the service
@rf_service.api(
    input=JSON(pydantic_model=InputModel),
    output=JSON(),
    route='v1/models/rf_regressor/predict'
)
async def classify(input_data: InputModel, ctx: bentoml.Context) -> dict:
    
    request = ctx.request
    user = request.state.user if hasattr(request.state, 'user') else None

    # Convert the input data to a numpy array
    input_series = np.array([input_data.GRE_Score, input_data.TOEFL_Score, input_data.University_Rating,
    input_data.SOP, input_data.LOR, input_data.CGPA, input_data.Research])

    result = await exam_rf_runner.predict.async_run(input_series.reshape(1, -1))

    return {
        "prediction": result.tolist(),
        "user": user
    }

# Function to create a JWT token
def create_jwt_token(user_id: str):
    # expiration = datetime.utcnow() + timedelta(hours=1)
    if user_id == 'user_expired':
        expiration = datetime.utcnow() + timedelta(seconds=-1)
    else:
        expiration = datetime.utcnow() + timedelta(hours=1)
            
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token
