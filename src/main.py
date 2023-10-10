
# Import necessary libraries
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import uvicorn
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


# Create a FastAPI instance with title and description
app = FastAPI(
    title="Sepsis Prediction APP",
    description="An APP for predicting sepsis status based on a patient's medical record. \
                This API accepts medical record features as input and provides predictions \
                for the likelihood of sepsis. The features include:\n\n"
                "- PRG (Plasma Glucose): Plasma glucose levels.\n"
                "- PL (Blood Work Result-1): Blood work result 1 (mu U/ml).\n"
                "- PR (Blood Pressure): Blood pressure in mm Hg.\n"
                "- SK (Blood Work Result-2): Blood work result 2 (mm).\n"
                "- TS (Blood Work Result-3): Blood work result 3 (mu U/ml).\n"
                "- M11 (Body Mass Index): Body mass index (weight in kg / (height in m)^2).\n"
                "- BD2 (Blood Work Result-4): Blood work result 4 (mu U/ml).\n"
                "- Age: Patient's age in years.\n\n"
                "Use this APP to assess sepsis risk and make informed medical decisions.",
)



# app = FastAPI()

# Define the path to your pickle file
pickle_file_path = "src/asset/ml/sepssis_components.pkl"

# Check if the pickle file exists
if not os.path.exists(pickle_file_path):
    raise Exception(f"Pickle file '{pickle_file_path}' not found. Please check the file path.")

# Load your pre-trained machine learning model and preprocessing components using pickle
with open(pickle_file_path, "rb") as model_file:
    exported_data = pickle.load(model_file)

# Extract the pre-fitted preprocessing components and model from the loaded components
scaler = exported_data['scaler']
numerical_imputer = exported_data['numerical_imputer']
best_model = exported_data['best_model']

class SepsisInput(BaseModel):
    PRG: float
    PL: float
    PR: float
    SK: float
    TS: float
    M11: float
    BD2: float
    Age: int 

# Root endpoint to provide a response at the root URL
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Sepsis Prediction APP!"}    


# Set endpoint to make sepsis predictions
@app.post("/predict_sepsis/", response_model=dict)
async def predict_sepsis(data: SepsisInput):
    try:
        # Extract features from the request
        features = [
            data.PRG,
            data.PL,
            data.PR,
            data.SK,
            data.TS,
            data.M11,
            data.BD2,
            data.Age,
        ]

        # Create a pandas DataFrame to hold the features
        features_df = pd.DataFrame([features], columns=["PRG", "PL", "PR", "SK", "TS", "M11", "BD2", "Age"])

        # Create a numpy array from the features
        features_array = np.array(features).reshape(1, -1)

        # Apply preprocessing steps to the features using the pre-fitted scaler and imputer
        features_scaled = scaler.transform(features_array)
        features_imputed = numerical_imputer.transform(features_scaled)

        # Perform sepsis predictions using your model
        prediction = int(best_model.predict(features_imputed)[0])  

        # Map the prediction to "Positive" or "Negative"
        sepsis_result = "Positive Sepsis Status" if prediction == 1 else "Negative Sepsis Status"

       # Construct the response dictionary
        response_dict = {
            "features": features_df.to_dict(orient="records")[0],
            "sepsis_prediction": sepsis_result
        }

        return response_dict


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
