from flask import Flask, jsonify, render_template
from services.thingspeak_service import fetch_latest_data
from services.db import init_db
from services.db import get_latest_readings
import os

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/sensor-data")
def sensor_data():
    data = fetch_latest_data()
    return jsonify(data)




@app.route("/api/history")
def history():
    rows = get_latest_readings(50)

    history_data = []
    for r in rows:
        history_data.append({
            "name": r[0],
            "co2": r[1],
            "temperature": r[2],
            "humidity": r[3],
            "quality": r[4],
            "score": r[5],
            "latitude": r[6],
            "longitude": r[7],
            "timestamp": r[8]
        })

    return jsonify(history_data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)