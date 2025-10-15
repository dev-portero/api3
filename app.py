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
TABLE_NAME = 'ib_empleado_imp1'     # tabla con los campos


# # Función de conexión
def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    conn = pyodbc.connect(conn_str)
    return conn
    
    

@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"SELECT TOP 5 * FROM {TABLE_NAME}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # Devolver resultado como texto simple
    return "Holiiiiii"
    
# CREATE
@app.route("/employees", methods=["POST"])
def crear_producto():
    data = request.get_json()
    corporacion = data.get("corporacion")
    identificacion = data.get("identificacion", "")
    nombre = data.get("nombre", "")
    apellidos = data.get("apellidos", "")
    direccion = data.get("direccion", "")
    email = data.get("email", "")
    telefono = data.get("telefono", "")
    rh = data.get("rh", "")
    fecha_nacimiento = data.get("fecha_nacimiento", "")
    dependencia = data.get("dependencia", "")
    eps = data.get("eps", "")
    id_eps = data.get("id_eps", "")    
    cargo = data.get("cargo", "")
    id_cargo = data.get("id_cargo", "")
    genero = data.get("genero", "")
    emp_imp_error = data.get("emp_imp_error", "")
    prs_nombre = data.get("prs_nombre", "")
    soc_nombre = data.get("soc_nombre", "")
    prs_id = data.get("prs_id", "")
    emp_soc_id = data.get("emp_soc_id", "")
    mot_id = data.get("mot_id", "")
    mot_nombre = data.get("mot_nombre", "")
    talla_superior = data.get("talla_superior", "")
    tala_inferior = data.get("tala_inferior", "")
    talla_zapato = data.get("talla_zapato", "")
    conn = get_connection()
    cursor = conn.cursor()
    query = f""" INSERT INTO {TABLE_NAME} (cor_id,         emp_identificacion, emp_nombres,        emp_apellidos,
                                           emp_direccion,  emp_email,          emp_telefono,       emp_rh,
                                           emp_nacimiento, emp_dependencia,    emp_EPS,            ent_id_EPS,
                                           emp_cargo,      car_id,             emp_genero,         prs_nombre,
                                           soc_nombre,     prs_id,             emp_imp_error,      emp_soc_id,
                                           mot_id,         mot_nombre,         emp_talla_superior, emp_talla_inferior,
                                           emp_talla_zapato
                                   values (?,                  ?,              ?,                  ?,   
                                           ?,                  ?,              ?,                  ?,
                                           ?,                  ?,              ?,                  ?,
                                           ?,                  ?,              ?,                  ?, 
                                           ?,                  ?,              ?,                  ?, 
                                           ?,                  ?,              ?,                  ?, 
                                           ?)                                                     
    """
    datVar = (corporacion,      identificacion, nombre,         apellidos,
              direccion,        email,          telefono,       rh,
              fecha_nacimiento, dependencia,    eps,            id_eps,
              cargo,            id_cargo,       genero,         emp_imp_error,
              prs_nombre,       soc_nombre,     prs_id,         emp_soc_id, 
              mot_id,           mot_nombre,     talla_superior, tala_inferior,
              talla_zapato)
    cursor.execute(query,datVar)
    conn.commit()
    # obtener el último ID insertado
    cursor.execute("SELECT SCOPE_IDENTITY()")
    new_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return jsonify({"id": new_id, "nombre": nombre, "apellidos": apellidos}), 201
    
 
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