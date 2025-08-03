from fastapi import APIRouter
from src.model.models import LRModel
import numpy as np
import pandas as pd
import pickle

def load_model():
    with open("src/routes/models/lr_model.pkl","rb") as f:
        model = pickle.load(f)
    return model 

model_router = APIRouter()

@model_router.post('/predict')
def predict(data: LRModel):
    features = pd.DataFrame([[data.edad, data.peso, data.altura]], columns=["edad", "peso", "altura"])
    model = load_model()
    prediction = model.predict(features)
    return {'predicted_value': int(prediction)}