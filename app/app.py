from flask import Flask, request, render_template
import logging
import os

app = Flask(__name__)


# Initialize logging
logging.basicConfig(level=logging.INFO)


def get_host():
    return request.host


def generate_message(host):
    return f"<p>Hello World!</p><p>You are connected to {host}</p>"


@app.route("/")
def hello_world():
    try:
        host = get_host()
        message = generate_message(host)
        logging.info(f"Generated message: {message}")
        return render_template("index.html", message=message)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = bool(os.environ.get("DEBUG_MODE", True))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
