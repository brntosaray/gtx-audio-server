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
