from flask import Flask
app = Flask(__name__)

from core import controller

if __name__ == "__main__":
    app.run(debug=True)

