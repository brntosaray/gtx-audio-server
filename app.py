from flask import Flask, jsonify, send_file, request, Response
import os
import json

app = Flask(__name__)

AUDIO_DIR = "./audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def auth_payload(req):
    package = req.args.get("package", "")
    sn = req.args.get("sn", "")
    mac = req.args.get("mac", "")
    ver = req.args.get("ver", "")
    return {
        "result": 1,
        "msg": "success",
        "data": {
            "status": 1,
            "expire": "2099-12-31",
            "package": package,
            "sn": sn,
            "mac": mac,
            "ver": ver
        }
    }

def json_ok(req):
    return Response(json.dumps(auth_payload(req)), mimetype="application/json", status=200)

@app.route("/")
def index():
    return jsonify({"status": "GTX Audio Server Running", "version": "1.0"})

@app.route("/index.php/api/app/auth", methods=["GET", "POST"])
@app.route("/api/app/auth", methods=["GET", "POST"])
@app.route("/api/auth", methods=["GET", "POST"])
@app.route("/api/v1/auth", methods=["GET", "POST"])
@app.route("/api/v1/activation", methods=["GET", "POST"])
@app.route("/activate", methods=["GET", "POST"])
@app.route("/audio/activate", methods=["GET", "POST"])
@app.route("/auth", methods=["GET", "POST"])
def auth():
    return json_ok(request)

@app.route("/audio/list")
def list_audio():
    files = []
    if os.path.exists(AUDIO_DIR):
        files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(('.mp3', '.aac', '.m3u8'))]
    return jsonify({"files": files, "count": len(files)})

@app.route("/audio/<filename>")
def serve_audio(filename):
    filepath = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    return jsonify({"error": "File not found"}), 404

@app.route("/epg")
def epg():
    return jsonify({"epg": [], "message": "EPG endpoint ready"})

@app.errorhandler(405)
def handle_405(e):
    return json_ok(request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
