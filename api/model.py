import pickle

with open("../model/random_forest_model.pkl","rb") as f:
    model = pickle.load(f)
    

    
with open("../model/label_encoders.pkl","rb") as f:
    label_encoders = pickle.load(f)
    
with open("../model/standard_scalers.pkl","rb") as f:
    scalers = pickle.load(f)
    
