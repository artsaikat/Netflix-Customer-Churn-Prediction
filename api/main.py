from fastapi import FastAPI
from api.schema import UserInput
from fastapi.responses import JSONResponse
from api.predict import churn_predict
from api.model import model
from api.predicted_output import PredictionResponse



app = FastAPI()

@app.get("/")
def home():
    return{
        "Netflix Customer Churn Prediction app"
    }
    
    
@app.post("/churn_predict",response_model=PredictionResponse)
def predict(data:UserInput):
    try:
        prediction = churn_predict(data.model_dump())
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    