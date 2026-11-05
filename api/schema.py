from pydantic import BaseModel , Field
from typing import Annotated,Literal

class UserInput(BaseModel):
    age : Annotated[int , Field(...,gt=0, lt=110 , description="Age of the user ")]
    gender : Annotated[Literal["Male","Female","Other"],Field(...,description="Gender of the user")]
    country : Annotated[Literal['India' ,'USA', 'Canada' ,'Brazil' ,'France', 'Australia' ,'UK' ,'Japan','Germany', 'Spain'] , Field(..., description="country of the user ")]
    account_age_months : Annotated[int , Field(..., description="account age months of the user ")]
    subscription_type : Annotated[Literal['Standard', 'Basic', 'Premium'] , Field(...,description="subscription_type of the user ")]
    monthly_fee : Annotated[float , Field(..., description="monthly fee of the user ")]
    payment_method : Annotated[Literal['PayPal' ,'Credit Card', 'UPI', 'Debit Card'] , Field(..., description="payment_method of the user ")]
    primary_device : Annotated[Literal['Laptop', 'Tablet' ,'Smart TV', 'Mobile'] , Field(..., description="primary device of the user ")]
    devices_used : Annotated[int , Field(...,gt=0 , description="How many devices user used ")]
    favorite_genre : Annotated[Literal['Sci-Fi','Documentary','Comedy' ,'Action' ,'Horror' ,'Romance' ,'Thriller','Drama'] , Field(..., description="Favorite genre of the user ")]
    avg_watch_time_minutes : Annotated[int , Field(...,gt=0 , description="avg_watch_time_minutes of the user ")]
    watch_sessions_per_week : Annotated[int , Field(...,gt=0 , description="watch_sessions_per_week of the user ")]
    binge_watch_sessions : Annotated[int , Field(...,gt=0,description="binge_watch_sessions of the user")]
    completion_rate : Annotated[int , Field(...,gt=0 , description="completion_rate of the user ")]
    rating_given : Annotated[float , Field(...,gt=0 , description="rating_given of the user ")]
    content_interactions : Annotated[int , Field(...,gt=0, description="content_interactions of the user ")]
    recommendation_click_rate : Annotated[int , Field(...,gt=0, description="recommendation_click_rate of the user ")]
    days_since_last_login : Annotated[int , Field(...,gt=0, description="days_since_last_login of the user ")]
    
    
    
    