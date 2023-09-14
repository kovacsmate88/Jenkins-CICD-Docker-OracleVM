from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    try:
        return "<p>Hello World!</p>"
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
