from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
print(HARVEST_API_TOKEN) 
# Configuración de Harvest API
HARVEST_ACCOUNT_ID = "1961945"  # Reemplázalo con el tuyo
HARVEST_API_TOKEN = os.getenv("HARVEST_API_TOKEN")  # Lo leeremos desde una variable de entorno

@app.route("/")
def fetch_harvest_data():
    url = "https://api.harvestapp.com/api/v2/time_entries"
    headers = {
        "Harvest-Account-ID": HARVEST_ACCOUNT_ID,
        "Authorization": f"Bearer {HARVEST_API_TOKEN}",
        "User-Agent": "Harvest API Cloud Run"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
    return jsonify(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")  # Imprimir el mensaje de error
    return jsonify({"error": "No se pudo obtener los datos"}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
