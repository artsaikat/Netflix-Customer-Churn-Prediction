import streamlit as st
from api.model import model,label_encoders,scalers
import pandas as pd
import shap
import matplotlib.pyplot as plt
import io



st.header("🎬 Netflix Customer Churn Intelligence 📊🤖")

with st.sidebar:
    st.title("netflix input")
    
    age = st.number_input("Customer's age",0,110)
    gender = st.selectbox("Gender of customer",["Male","Female","Other"])
    country = st.selectbox("country",['India' ,'USA', 'Canada' ,'Brazil' ,'France', 'Australia' ,'UK' ,'Japan','Germany', 'Spain'])
    account_age_months = st.number_input("account age months",min_value=0)
    subscription_type = st.selectbox("Subscription Type of customer",['Standard', 'Basic', 'Premium'])
    monthly_fee = st.number_input("Monthly fee of customer",min_value=0.0)
    payment_method = st.selectbox("Payment Method of customer",['PayPal' ,'Credit Card', 'UPI', 'Debit Card'])
    primary_device = st.selectbox("Primary device of customer",['Laptop', 'Tablet' ,'Smart TV', 'Mobile'])
    devices_used = st.number_input("How many devices customer use",min_value=0)
    favorite_genre = st.selectbox("Favourite genre of customer",['Sci-Fi','Documentary','Comedy' ,'Action' ,'Horror' ,'Romance' ,'Thriller','Drama'])
    avg_watch_time_minutes = st.number_input("Avg watch time in minutes",min_value=0)
    watch_sessions_per_week = st.number_input("watch sessions per week",min_value=0)
    binge_watch_sessions = st.number_input("binge watch sessions",min_value=0)
    completion_rate = st.number_input("completion rate of customer",min_value=0)
    rating_given = st.number_input("rating given",min_value=0.0)
    content_interactions = st.number_input("content interactions",min_value=0)
    recommendation_click_rate = st.number_input("recommendation click rate",min_value=0)
    days_since_last_login = st.number_input("days since last login",min_value=0)
    
    data = {
        "age" : age,
        "gender" : gender,
        "country":country,
        "account_age_months":account_age_months,
        "subscription_type":subscription_type,
        "monthly_fee":monthly_fee,
        "payment_method":payment_method,
        "primary_device":primary_device,
        "devices_used":devices_used,
        "favorite_genre":favorite_genre,
        "avg_watch_time_minutes":avg_watch_time_minutes,
        "watch_sessions_per_week":watch_sessions_per_week,
        "binge_watch_sessions":binge_watch_sessions,
        "completion_rate":completion_rate,
        "rating_given":rating_given,
        "content_interactions":content_interactions,
        "recommendation_click_rate":recommendation_click_rate,
        "days_since_last_login":days_since_last_login
    }
    
    input_df = pd.DataFrame([data])
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

# --------------------------------
# Prediction
# --------------------------------

predicted_class = model.predict(input_df)[0]

probabilities = model.predict_proba(input_df)[0]

churn_probability = probabilities[list(model.classes_).index(1)]

def pred_class_label(pred_class):
    if pred_class == 0:
        return "No Churn"
    else:
        return "Churn"


# --------------------------------
# Submit Button
# --------------------------------

if st.button("Submit"):

    final_output = pred_class_label(predicted_class)

    st.subheader("Customer Churn Prediction")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Prediction",
            final_output
        )

    with col2:
        st.metric(
            "Churn Probability",
            f"{churn_probability:.2%}"
        )

    if predicted_class == 1:
        st.error("This customer is likely to churn!")
    else:
        st.success("This customer is unlikely to churn!")

    st.balloons()

    # --------------------------------
    # SHAP Waterfall Explanation
    # --------------------------------

    st.divider()

    st.subheader("SHAP Waterfall Explanation")

    st.write(
        "Understand which customer features influence "
        "this individual churn prediction."
    )

    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)

    # Calculate SHAP values for this customer
    shap_values = explainer.shap_values(input_df)

    # Find the positive class (churn = 1)
    class_index = list(model.classes_).index(1)

    # Handle different SHAP output formats
    if isinstance(shap_values, list):

        customer_shap = shap_values[class_index][0]
        base_value = explainer.expected_value[class_index]

    elif len(shap_values.shape) == 3:

        customer_shap = shap_values[0, :, class_index]
        base_value = explainer.expected_value[class_index]

    else:

        customer_shap = shap_values[0]
        base_value = explainer.expected_value

    # Create SHAP Explanation
    explanation = shap.Explanation(
        values=customer_shap,
        base_values=base_value,
        data=input_df.iloc[0].values,
        feature_names=input_df.columns.tolist()
    )

    # Draw Waterfall plot
    shap.plots.waterfall(
        explanation,
        max_display=15,
        show=False
    )

    fig = plt.gcf()

    st.pyplot(fig)

    plt.close(fig)
    
    
   

    # Prepare customer prediction report
    report = input_df.copy()

    report["Predicted_Churn"] = final_output
    report["Churn_Probability"] = churn_probability

    # Convert dataframe into CSV
    csv_data = report.to_csv(index=False).encode("utf-8")

    # Download button
    st.download_button(
        label="📥 Download Customer Report",
        data=csv_data,
        file_name="netflix_customer_churn_report.csv",
        mime="text/csv"
    )
    
    