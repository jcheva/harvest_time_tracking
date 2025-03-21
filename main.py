import datetime
from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Configuración de Harvest API
HARVEST_ACCOUNT_ID = "1961945"  # Reemplázalo con el tuyo
HARVEST_API_TOKEN = os.getenv("HARVEST_API_TOKEN")

@app.route("/")
def fetch_harvest_data():
    if HARVEST_API_TOKEN is None:
        return jsonify({"error": "API token not configured"}), 500

    # Obtener la fecha de hace 24 horas
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    started_after = yesterday.isoformat() + "Z"  # Formato ISO con zona horaria

    url = "https://api.harvestapp.com/api/v2/time_entries"
    headers = {
        "Harvest-Account-ID": HARVEST_ACCOUNT_ID,
        "Authorization": f"Bearer {HARVEST_API_TOKEN}",
        "User-Agent": "Harvest API Cloud Run"
    }
    
    # Agregar parámetros para la solicitud
    params = {
        "started_after": started_after,
        "per_page": 100  # Puedes ajustar esto según tus necesidades
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        
        # Aquí podrías agregar el código para enviar a BigQuery
        # send_to_bigquery(data["time_entries"])
        
        return jsonify(data)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return jsonify({"error": "No se pudo obtener datos", "details": response.text}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
