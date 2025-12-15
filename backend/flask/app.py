from flask import Flask, request, jsonify
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CPP_DIR = os.path.abspath(os.path.join(BASE_DIR, "../cpp"))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

BUS_ENGINE_PATH = os.path.join(CPP_DIR, "bus_engine")
METRO_ENGINE_PATH = os.path.join(CPP_DIR, "metro_engine")

STATION_CSV = os.path.join(CPP_DIR, "metro_stations.csv")
LINE_CSV    = os.path.join(CPP_DIR, "metro_lines.csv")


# ================= HOME =================
@app.route("/")
def home():
    return app.send_static_file("index.html")


# ================= BUS ROUTE =================
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


# ================= METRO ROUTE =================
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


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
