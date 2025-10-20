from flask import Flask, request, jsonify
import pyodbc
import traceback
import logging
import sys
from config import DB_CONFIG


# Este nombre debe ser 'app' para que Gunicorn lo encuentre
app = Flask(__name__)

# --- Configuración de logs (para ver errores en consola y en Azure) ---
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

# === CONSTANTES ===
TABLE_NAME = 'ib_empleado_api'     # tabla con los campos


# # Función de conexión
def get_connection():
    conn_str = (
        f"DRIVER={DB_CONFIG['DRIVER']};"
        f"SERVER={DB_CONFIG['SERVER']};"
        f"DATABASE={DB_CONFIG['DATABASE']};"
        f"UID={DB_CONFIG['UID']};"
        f"PWD={DB_CONFIG['PWD']};"
        f"TrustServerCertificate={DB_CONFIG['TrustServerCertificate']};"
    )
    conn = pyodbc.connect(conn_str)
    return conn
    
    
@app.route("/")
def home():
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"SELECT * FROM {TABLE_NAME}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    # Devolver resultado como texto simple
    return "<br>".join(str(row) for row in rows)
    
# CREATE
@app.route("/employees7", methods=["POST"])
def crear7_empleado():
    try: 
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Solicitud incorrecta, Faltan los campos requeridos"}), 400

        if 'identificacion' not in data:
            return jsonify({"error": "Campo 'identificacion' es requerido"}), 400
        
        if 'nombre' not in data:
            return jsonify({"error": "Campo 'nombre' es requerido"}), 400
        
        if 'apellidos' not in data:
            return jsonify({"error": "Campo 'apellidos' es requerido"}), 400
            
        if 'accion' not in data:
            return jsonify({"error": "Campo 'accion' es requerido"}), 400
        
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
        cargo = data.get("cargo", "")
        genero = data.get("genero", "")
        prs_nombre = data.get("prs_nombre", "")
        soc_nombre = data.get("soc_nombre", "")
        mot_nombre = data.get("mot_nombre", "")
        talla_superior = data.get("talla_superior", "")
        tala_inferior = data.get("tala_inferior", "")
        talla_zapato = data.get("talla_zapato", "")
        accion = data.get("accion", "")
        
        if accion not in ('Insertar', 'Actualizar', 'Estado'):
            return jsonify({"error": "El valor del campo 'accion' no es valido solo se admiten valores 'Insertar', 'Actualizar', 'Estado'"}), 400  

        if accion == "Estado" and 'estado' not in data:
            return jsonify({"error": "Campo 'estado' es requerido"}), 400            
        
        estado = data.get("estado", "")
        
        conn = get_connection()
        cursor = conn.cursor()
        

        
        query = f""" INSERT INTO {TABLE_NAME} (cor_id,             emp_identificacion, emp_nombres,        emp_apellidos,
                                               emp_direccion,      emp_email,          emp_telefono,       emp_rh,
                                               emp_nacimiento,     emp_dependencia,    emp_EPS,            emp_cargo,            
                                               emp_genero,         prs_nombre,         soc_nombre,         mot_nombre, 
                                               emp_talla_superior, emp_talla_inferior, emp_talla_zapato,   emp_tipo_registro,
                                               emp_estado) 
                                       OUTPUT INSERTED.emp_id                                                                                     
                                       values (?,                  ?,                  ?,                  ?,   
                                               ?,                  ?,                  ?,                  ?,
                                               ?,                  ?,                  ?,                  ?,
                                               ?,                  ?,                  ?,                  ?, 
                                               ?,                  ?,                  ?,                  ?,
                                               ?);
        """
        datVar = (7,                identificacion, nombre,         apellidos,
                  direccion,        email,          telefono,       rh,
                  fecha_nacimiento, dependencia,    eps,            cargo,
                  genero,           prs_nombre,     soc_nombre,     mot_nombre,     
                  talla_superior,   tala_inferior,  talla_zapato,   accion,
                  estado)
        cursor.execute(query,datVar)
        new_id = cursor.fetchone()[0]
        conn.commit()
        
        cursor.execute("SELECT emp_imp_error FROM {TABLE_NAME} where emp_id = ?", (new_id,))
        error_list = cursor.fetchone()[0]
        conn.commit()
        
        if error_list =="":
            if accion == "Insertar":
                return jsonify({"message": "Empleado creado exitosamente"}), 201
            else:
                return jsonify({"message": "Empleado actualizado"}), 200
        else:
            return jsonify({"error": error_list}), 400 
        
        
    except pyodbc.IntegrityError as e:
        # Error típico de constraint (por ejemplo NOT NULL o UNIQUE)
        conn.rollback()
        return jsonify({"error": "Error de integridad en la base de datos", "detalle": str(e)}), 400

    except pyodbc.ProgrammingError as e:
        # Error de sintaxis SQL u otro problema de estructura
        conn.rollback()
        return jsonify({"error": "Error en la sintaxis SQL o campos inválidos", "detalle": str(e)}), 400

    except Exception as e:
        # Cualquier otro error inesperado
        conn.rollback()
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

    finally:
        # Asegura que se cierren recursos si existen
        try:
            cursor.close()
            conn.close()
        except:
            pass
    
 
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