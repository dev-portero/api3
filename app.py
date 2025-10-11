from flask import Flask

# Este nombre debe ser 'app' para que Gunicorn lo encuentre
app = Flask(__name__)

@app.route("/")
def home():
    prueba = " Prueba angee"
    return "Hola desde Flask en Azure con Git Hub - FUNCIONA !!! - 2025-10-10 18:31:00" + prueba
