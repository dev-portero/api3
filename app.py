from flask import Flask

# Este nombre debe ser 'app' para que Gunicorn lo encuentre
app = Flask(__name__)

@app.route("/")
def home():
    return "Hola desde Flask en Azure con Git Hub - FUNCIONA !!!"
