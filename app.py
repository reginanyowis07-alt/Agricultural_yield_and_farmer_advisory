from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # fine for local dev; restrict later if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="Agriculture Yield & Farmer Advisory API")


class FarmInput(BaseModel):
    area: float
    year: int
    rainfall: float
    pesticide_use: float
    average_temperature: float
    crop: str


@app.get("/")
def home():
    return {
        "message": "Agriculture Yield & Farmer Advisory API is running"
    }


@app.post("/predict")
def predict(data: FarmInput):

    # Demo prediction
    # Replace this section with your trained model prediction
    if data.rainfall > 1000:
        prediction = "High"
    elif data.rainfall > 500:
        prediction = "Medium"
    else:
        prediction = "Low"

    return {
        "predicted_yield_band": prediction,
        "crop": data.crop,
        "year": data.year
    }