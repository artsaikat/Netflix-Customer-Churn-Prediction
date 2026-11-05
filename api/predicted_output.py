from pydantic import BaseModel , Field
from typing import Dict,Literal

class PredictionResponse(BaseModel):
    churn : str = Field(...,description="Predicted customer churn status",examples=["No","Yes"])
    confidence : float = Field(...,description='Models confidence score for the predicted class (range: 0 to 1)',examples=[0.8432])
    class_probabilities : Dict[str,float] = Field(...,description='Probability distribution across all possible classes',examples=[{"No": 0.01, "Yes": 0.15}])
    