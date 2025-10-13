from flask import Flask, request, jsonify
import pyodbc
import traceback
import logging
import sys


# Este nombre debe ser 'app' para que Gunicorn lo encuentre
app = Flask(__name__)

# --- Configuración de logs (para ver errores en consola y en Azure) ---
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

# === CONFIGURACIÓN BASE DE DATOS ===
SERVER ='dataportero.database.windows.net'
DATABASE = 'datacc' 
USERNAME = 'validacion_documentos'
PASSWORD = 'RRt852*amxb'
DRIVER = '{ODBC Driver 18 for SQL Server}'
TABLE_NAME = 'ib_validacion_documentos'     # tabla con los campos


# # Función de conexión
def get_connection():
    conn = pyodbc.connect(
        'DRIVER={DRIVER};'
        'SERVER={SERVER};'          
        'DATABASE={DATABASE};'
        'UID={USERNAME};'
        'PWD={PASSWORD};'
        'TrustServerCertificate=yes;'        # evita problemas SSL si es remoto      
    )
    return conn
    
    

@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT top 5 * FROM {TABLE_NAME}")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # Devolver resultado como texto simple
    return "<br>".join(str(row) for row in rows)
    
 
@app.route("/test-error")
def test_error():
    # Genera un error a propósito para probar el manejo de excepciones
    1 / 0  # Esto causará un ZeroDivisionError
    return "Nunca se mostrará esto."


# --- Manejador global de errores (muestra el error completo en el navegador) ---
@app.errorhandler(Exception)
def handle_exception(e):
    tb = traceback.format_exc()
    app.logger.error("❌ Ocurrió un error en la aplicación:\n" + tb)
    # Devuelve el error completo al navegador
    return f" Ocurrió un error en el servidor:</h2><pre>{tb}</pre>", 500