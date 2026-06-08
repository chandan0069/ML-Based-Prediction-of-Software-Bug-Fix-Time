from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

FASTAPI_URL = "http://127.0.0.1:8000"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    try:
        res = requests.post(f"{FASTAPI_URL}/predict", json=data, timeout=10)
        return jsonify(res.json()), res.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"detail": "Cannot connect to prediction API. Is FastAPI running?"}), 503
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/health")
def health():
    try:
        res = requests.get(f"{FASTAPI_URL}/health", timeout=5)
        return jsonify(res.json())
    except:
        return jsonify({"status": "error", "model_loaded": False})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
