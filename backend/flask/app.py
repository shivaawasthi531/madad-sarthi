from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__, static_folder=None)

# ===== BASE PATHS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = BASE_DIR  # assume app.py is at project root
CPP_DIR = os.path.join(PROJECT_ROOT, "backend", "cpp")
DATA_DIR = os.path.join(PROJECT_ROOT, "backend", "data")
FRONTEND_DIR = PROJECT_ROOT

# ===== C++ BINARIES =====
BUS_ENGINE   = os.path.join(CPP_DIR, "bus_engine")
METRO_ENGINE = os.path.join(CPP_DIR, "metro_engine")

# ===== CSV FILES =====
BUS_STOPS      = os.path.join(DATA_DIR, "dtc_bus_stops.csv")
BUS_INFO       = os.path.join(DATA_DIR, "dtc_buses.csv")
METRO_STATIONS = os.path.join(DATA_DIR, "dtc_metro_stations.csv")
METRO_LINES    = os.path.join(DATA_DIR, "dtc_metro_lines.csv")

# ===== FRONTEND =====
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

# ===== BUS ROUTE =====
@app.route("/bus-route", methods=["POST"])
def bus_route():
    data = request.get_json(force=True)
    start = data.get("start", "")
    end   = data.get("end", "")

    # run bus_engine with start & end
    result = subprocess.run(
        [BUS_ENGINE, start, end],
        cwd=CPP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0 or not result.stdout.strip():
        return jsonify({"error": "No bus found"})

    return jsonify({"type": "bus", "result": result.stdout})

# ===== METRO ROUTE =====
@app.route("/metro-route", methods=["POST"])
def metro_route():
    data = request.get_json(force=True)
    start = data.get("start", "")
    end   = data.get("end", "")

    result = subprocess.run(
        [METRO_ENGINE, start, end, METRO_STATIONS, METRO_LINES],
        cwd=CPP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0 or not result.stdout.strip():
        return jsonify({"error": "No metro found"})

    return jsonify({
        "type": "metro",
        "result": result.stdout,
        "lines": result.stdout.splitlines()
    })

# ===== ENTRYPOINT =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
