from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CPP_DIR = os.path.abspath(os.path.join(BASE_DIR, "../cpp"))

BUS_ENGINE_PATH = os.path.join(CPP_DIR, "bus_engine")
METRO_ENGINE_PATH = os.path.join(CPP_DIR, "metro_engine")
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))


STATION_CSV = os.path.join(CPP_DIR, "metro_stations.csv")
LINE_CSV    = os.path.join(CPP_DIR, "metro_lines.csv")

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

@app.route("/bus-route", methods=["POST"])
def bus_route():
    data = request.json
    start = data.get("start")
    end = data.get("end")

    try:
        result = subprocess.run(
            [BUS_ENGINE_PATH, start, end],
            cwd=CPP_DIR,
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if not output:
            return jsonify({"error": "No bus found"})

        return jsonify({"bus": "DTC", "raw": output})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/metro-route", methods=["POST"])
def metro_route():
    data = request.json
    start = data.get("start")
    end = data.get("end")

    try:
        result = subprocess.run(
            [METRO_ENGINE_PATH, start, end, STATION_CSV, LINE_CSV],
            cwd=CPP_DIR,
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if not output:
            return jsonify({"error": "No metro found"})

        return jsonify({
            "metro": "Delhi Metro",
            "raw": output,
            "lines": output.splitlines()
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

