
import hashlib
import ipaddress
import platform
import shutil
import subprocess

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    user_id = request.args.get("id", "1")
    return f"<h1>Hello, user #{escape(user_id)}!</h1>"


@app.route("/checksum")
def checksum():
    data = request.args.get("data", "")
    return hashlib.sha256(data.encode()).hexdigest()


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    try:
        ipaddress.ip_address(host)
    except ValueError:
        return "Invalid IP address", 400

    ping_cmd = shutil.which("ping")

    if ping_cmd is None:
        return "ping not found", 500

    count_flag = "-n" if platform.system() == "Windows" else "-c"

    try:
        result = subprocess.run(
            [ping_cmd, count_flag, "1", host],
            capture_output=True,
            check=False,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return "Ping timeout", 504

    return f"<pre>{escape(result.stdout.decode(errors='replace'))}</pre>"


if __name__ == "__main__":
    app.run(debug=False)
