from fastapi import APIRouter
import numpy as np
import pandas as pd
import pickle
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydantic import BaseModel
from pymongo import MongoClient


sheets_data_router = APIRouter()

# === CONEXIÓN GOOGLE SHEETS ===
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("src/routes/credenciales.json", scope)
client = gspread.authorize(creds)

class planilla(BaseModel):
    planilla: str
@sheets_data_router.post('/data')
def agregar(planilla: planilla):
    # Abrir una hoja de cálculo (ejemplo: por nombre)
    spreadsheet = client.open(planilla.planilla)
    worksheet = spreadsheet.sheet1  # o por índice, .get_worksheet(0)
    paciente = worksheet.cell(2, 2).value
    paciente = paciente.replace(" ","_")
    # === CONEXIÓN MONGODB ===
    # Reemplazá la URI por tu conexión real (puede ser local o Atlas)
    mongo_uri = "mongodb+srv://lautimarino17:Moreno18@cluster.umilwzi.mongodb.net/"
    mongo_client = MongoClient(mongo_uri)

    # Selecciona base de datos y colección
    db = mongo_client["llm_resume"]
    collection = db[paciente]

    # === EJEMPLO DE INSERCIÓN DE DATOS A MONGO ===
    # Suponiendo que obtenés valores de una fila en la hoja
    data = worksheet.cell(50, 2).value  # Col 2 = B, fila 50
    documento = {"pliegues":data}

    collection.insert_one(documento)
    
