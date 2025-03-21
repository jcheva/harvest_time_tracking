from flask import Flask, jsonify
import requests
import os
from google.cloud import bigquery
import datetime  # Asegúrate de importar esto

app = Flask(__name__)

# Configuración de Harvest API
HARVEST_ACCOUNT_ID = "1961945"
HARVEST_API_TOKEN = os.getenv("HARVEST_API_TOKEN")

@app.route("/")
def fetch_harvest_data():
    if HARVEST_API_TOKEN is None:
        return jsonify({"error": "API token not configured"}), 500

    # Obtener la fecha de hace 24 horas
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    started_after = yesterday.isoformat() + "Z"

    url = "https://api.harvestapp.com/api/v2/time_entries"
    headers = {
        "Harvest-Account-ID": HARVEST_ACCOUNT_ID,
        "Authorization": f"Bearer {HARVEST_API_TOKEN}",
        "User-Agent": "Harvest API Cloud Run"
    }
    
    params = {
        "started_after": started_after,
        "per_page": 100
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        time_entries = data.get("time_entries", [])
        
        # Enviar los datos a BigQuery
        send_to_bigquery(time_entries)
        
        return jsonify(data)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return jsonify({"error": "No se pudo obtener datos", "details": response.text}), response.status_code

def send_to_bigquery(entries):
    client = bigquery.Client()
    table_id = "harvest-time-tracking-454321.TRACKING.HARVEST_TIME_DATA"  # Modifica esto

    rows_to_insert = []
    for entry in entries:
        rows_to_insert.append({
            "id": entry["id"],
            "hours": entry["hours"],
            "spent_date": entry["spent_date"],
            "notes": entry["notes"],
            "client": entry["client"]["name"],
        })

    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print(f"Errores al insertar filas: {errors}")
    else:
        print("Datos insertados en BigQuery exitosamente!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
