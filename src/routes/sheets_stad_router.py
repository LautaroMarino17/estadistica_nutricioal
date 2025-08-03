from fastapi import APIRouter
import numpy as np
import pandas as pd
import pickle
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydantic import BaseModel


sheets_router = APIRouter()
# Define el scope para Sheets y Drive
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Autenticarse
creds = ServiceAccountCredentials.from_json_keyfile_name("src/routes/credenciales.json", scope)
client = gspread.authorize(creds)

class ListaRequest(BaseModel):
    lista: list

@sheets_router.post('/stats')
def parsear(lista: ListaRequest):
    for i in range(len(lista.lista)):
    # Abre la hoja "prueba" y lee celda B50
        sheet_origen = client.open(lista.lista[i]).sheet1
        nombre = sheet_origen.cell(2, 2).value  # Col 2 = B, fila 50
        edad = sheet_origen.cell(3, 9).value 
        peso = sheet_origen.cell(6, 2).value 
        talla = sheet_origen.cell(7, 2).value 
        seis_pliegues = sheet_origen.cell(50, 2).value  # Col 2 = B, fila 50


        # Abre hoja destino "ids"
        sheet_destino = client.open("ids").sheet1

        # Buscar la primera fila vacía en la columna A
        col_a = sheet_destino.col_values(1)  # Columna A completa
        ultima_fila_vacia = len(col_a) + 1

        # Escribir el dato en la columna A de la siguiente fila vacía
        sheet_destino.update_cell(ultima_fila_vacia, 1, nombre)
        sheet_destino.update_cell(ultima_fila_vacia, 2, edad)
        sheet_destino.update_cell(ultima_fila_vacia, 3, peso)
        sheet_destino.update_cell(ultima_fila_vacia, 4, talla)
        sheet_destino.update_cell(ultima_fila_vacia, 5, seis_pliegues)
    return 0
        #print(f"Dato '{data}' copiado a fila {ultima_fila_vacia} en hoja 'ids'")

