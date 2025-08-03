import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
# Cargar datos desde el archivo JSON
with open("data.json", "r") as f:
    data = json.load(f)

# Convertir a DataFrame
df = pd.DataFrame(data)

# Variables independientes (X) y variable objetivo (y)
X = df[["edad", "peso", "altura"]]
y = df["porcentaje_grasa"]

# Separar en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Crear y entrenar modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Evaluar el modelo
y_pred = modelo.predict(X_test)
print("MSE:", mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))
print("acc:", modelo.score(X_test,y_test))
#print("Coeficientes:", modelo.coef_)
#print("Intercepto:", modelo.intercept_)

# Guardar modelo entrenado
with open("src/routes/models/lr_model.pkl", "wb") as f:
    pickle.dump(modelo, f)
print("Modelo guardado como .pkl")
