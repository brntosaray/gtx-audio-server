from flask import Flask, jsonify, send_file, request
import os

app = Flask(__name__)

AUDIO_DIR = "./audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/")
def index():
    return jsonify({"status": "GTX Audio Server Running", "version": "1.0"})

@app.route("/index.php/api/app/auth")
def auth():
    package = request.args.get("package", "")
    sn = request.args.get("sn", "")
    mac = request.args.get("mac", "")
    ver = request.args.get("ver", "")
    return jsonify({
        "result": 1,
        "msg": "success",
        "data": {
            "status": 1,
            "expire": "2099-12-31",
            "package": package,
            "sn": sn
        }
    })

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
