from flask import Flask, jsonify, abort
from flask_cors import CORS
from mandelbrot_zoom import generarImagenSector
import os

app = Flask(__name__)
CORS(app)

os.makedirs("img", exist_ok=True)

@app.route('/tile/<int:n>/<int:x>/<int:y>')
def get_tile(n, x, y):
    try:
        generarImagenSector(x, y, n)
        return jsonify({"ok": True})
    except Exception as e:
        abort(500, description=str(e))

@app.route('/check/<int:n>/<int:x>/<int:y>')
def check_tile(n, x, y):
    ruta = f"img/mbz_{n}_{x}_{y}.png"
    return jsonify({"exists": os.path.isfile(ruta)})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
