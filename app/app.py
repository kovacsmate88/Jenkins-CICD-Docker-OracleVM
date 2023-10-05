from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import platform
import os

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def main():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    os_info = f"{platform.system()} {platform.release()}"
    host_name = platform.node()
    socketio.emit("system_info", {"host": host_name, "os": os_info})


def get_system_usage():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = f"{memory_info.used / (1024 ** 3):.2f} GB / {memory_info.total / (1024 ** 3):.2f} GB"
        socketio.emit("system_usage", {"cpu": cpu_usage, "memory": memory_usage})


if __name__ == "__main__":
    socketio.start_background_task(target=get_system_usage)
    port = int(os.environ.get("PORT", 5000))
    debug_mode = bool(os.environ.get("DEBUG_MODE", True))
    socketio.run(app, debug=debug_mode, host="0.0.0.0", port=port)
