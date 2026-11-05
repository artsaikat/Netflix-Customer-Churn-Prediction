
from api.model import model, label_encoders, scalers
import pandas as pd

class_labels = model.classes_.tolist()


def churn_predict(user_input: dict):

    input_df = pd.DataFrame([user_input])

    # Apply Label Encoding
    for col, encoder in label_encoders.items():

        if col in input_df.columns:

            input_df[col] = encoder.transform(
                input_df[col].astype(str)
            )

    # Apply Standard Scaling
    for col, scaler in scalers.items():

        if col in input_df.columns:

            input_df[col] = scaler.transform(
                input_df[[col]]
            ).ravel()

    # Maintain training feature order
    if hasattr(model, "feature_names_in_"):

        input_df = input_df[list(model.feature_names_in_)]

    # Prediction
    predicted_class = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]

    confidence = max(probabilities)

    # Convert class labels into strings
    class_probs = {
        str(label): round(float(prob), 4)
        for label, prob in zip(class_labels, probabilities)
    }
    
    churn_labels = {
    "0": "No Churn",
    "1": "Churn"
    }

    return {
        "churn": churn_labels[str(predicted_class)],
        "confidence": round(float(confidence), 4),
        "class_probabilities": {
            churn_labels[str(label)]: round(float(prob), 4)
            for label, prob in zip(class_labels, probabilities)
        }
    }

