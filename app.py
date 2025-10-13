from flask import Flask, request, jsonify
import pyodbc


# Este nombre debe ser 'app' para que Gunicorn lo encuentre
app = Flask(__name__)

# # === CONFIGURACIÓN BASE DE DATOS ===
# SERVER ='dataportero.database.windows.net'
# DATABASE = 'datacc' 
# USERNAME = 'validacion_documentos'
# PASSWORD = 'RRt852*amxb'
# DRIVER = '{ODBC Driver 18 for SQL Server}'
# TABLE_NAME = "ib_empleado_imp1"     # tabla con los campos


# # # Función de conexión
# def get_connection():
    # conn = pyodbc.connect(
        # 'DRIVER={ODBC Driver 18 for SQL Server};'
        # 'SERVER={SERVER};'          
        # 'DATABASE={DATABASE};'
        # 'UID={USERNAME};'
        # 'PWD={PASSWORD}';'
        # 'TrustServerCertificate=yes;'        # evita problemas SSL si es remoto      
    # )
    # return conn

@app.route("/")
def home():
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("SELECT top 5 * FROM {TABLE_NAME}")
    # rows = cursor.fetchall()
    # cursor.close()
    # conn.close()
    # # Devolver resultado como texto simple
    # return "<br>".join(str(row) for row in rows)
    return "HOLAAAAAAAA!"
