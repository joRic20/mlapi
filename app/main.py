from fastapi import FastAPI, Header, HTTPException  # Web framework and header-based auth  
from pydantic import BaseModel  # Data validation  
import os  # Environment variable access  
from dotenv import load_dotenv  # Load .env file  
import joblib  # Model loading  
import pandas as pd  # Data handling  

load_dotenv()  # Read .env and populate os.environ  
API_TOKEN = os.getenv("API_TOKEN")  # Retrieve the expected API token  

# Initialize FastAPI app with metadata for Swagger UI
app = FastAPI(
    title="Iris Species Prediction API",  # Shown in docs
    description="Predict iris flower species using a pre-trained model.",  # Shown in docs
    version="1.2.0"  # API version
)

# Pydantic model for the /predict payload
class IrisFeatures(BaseModel):
    sepal_length: float  # Sepal length in cm
    sepal_width: float   # Sepal width in cm
    petal_length: float  # Petal length in cm
    petal_width: float   # Petal width in cm

# Pydantic model for the /hello payload
class NameIn(BaseModel):
    name: str  # Any string (required)

# Load the trained ML model once at startup
model = joblib.load("iris.mdl")  # Path to your .mdl file

@app.post("/predict")
async def predict(
    features: IrisFeatures,            # Parsed and validated JSON body
    x_api_token: str = Header(...),    # Required X-API-Token header
):
    """
    Predict the species of an iris flower given its measurements.
    """
    # Enforce token authentication
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Convert the validated input to a pandas DataFrame
    input_df = pd.DataFrame([features.dict()])  # Single-row DataFrame

    # Perform prediction using the pre-loaded model
    prediction = model.predict(input_df)  # Returns an array of labels

    # Return the first (and only) prediction
    return {"species": prediction[0]}

@app.post("/hello")
async def hello(payload: NameIn):
    """
    Simple greeting endpoint for health checks.
    """
    # Return a greeting message
    return {"message": f"Hello {payload.name}"}
