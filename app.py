from flask import Flask, request, jsonify
import pyodbc,base64,requests
import traceback
import logging
import sys
from functools import wraps
from config import DB_CONFIG,TOKENS


# Este nombre debe ser 'app' para que Gunicorn lo encuentre
app = Flask(__name__)

# --- Configuración de logs (para ver errores en consola y en Azure) ---
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

# === CONSTANTES ===
TABLE_NAME = 'ib_empleado_api'     # tabla con los campos
VIEW_NAME_7 = 'api7empleados'      #Vista con los campos
VIEW_NAME_8 = 'api8empleados'      #Vista con los campos


# Función de conexión
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

#funcion para convertir a base64
def url_to_base64(url):
    response = requests.get(url)
    response.raise_for_status()  # para errores HTTP

    # Obtiene los bytes de la imagen
    img_bytes = response.content

    # Convierte a base64
    encoded = base64.b64encode(img_bytes).decode("utf-8")

    return encoded
    
#decorador para el token
def token_required(expected_token):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Token requerido"}), 401

            try:
                token_type, token_value = auth_header.split()
            except ValueError:
                return jsonify({"error": "Formato del token inválido"}), 400

            if token_type.lower() != "bearer":
                return jsonify({"error": "Tipo de token inválido"}), 401

            if token_value != expected_token:
                return jsonify({"error": "Token inválido o expirado"}), 403

            return f(*args, **kwargs)
        return decorated
    return decorator



@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error": "Método no permitido",
        "message": f"El método {request.method} no está permitido para esta URL.",
    }), 405
    
@app.route("/")
def home():
    return "Hola, api carga y consulta empleados"
    
# CREATE
@app.route("/api7empleado", methods=["POST"])
@token_required(TOKENS['AMARILLO'])
def crear7_empleado():
    try: 
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Solicitud incorrecta, Faltan los campos requeridos"}), 400

        if 'identificacion' not in data:
            return jsonify({"error": "Campo 'identificacion' es requerido"}), 400
        
        if 'nombres' not in data:
            return jsonify({"error": "Campo 'nombres' es requerido"}), 400
        
        if 'apellidos' not in data:
            return jsonify({"error": "Campo 'apellidos' es requerido"}), 400
            
        if 'accion' not in data:
            return jsonify({"error": "Campo 'accion' es requerido"}), 400
        
        identificacion = data.get("identificacion", "")
        nombres = data.get("nombres", "")
        apellidos = data.get("apellidos", "")
        fecha_nacimiento = data.get("nacimiento", "")
        genero = data.get("sexo", "")
        direccion = data.get("direccion", "")
        telefono = data.get("telefono", "")
        email = data.get("email", "")
        cargo = data.get("cargo", "")
        fecha_ingreso = data.get("fecha_ingreso", "")
        fecha_final_prev = data.get("fecha_final_prev_contrato", "")
        fecha_retiro = data.get("fecha_retiro", "")
        eps = data.get("eps", "") 
        arl = data.get("arl_riesgo", "")
        talla_superior = data.get("talla_superior", "")
        talla_inferior = data.get("talla_inferior", "")
        talla_zapato = data.get("talla_zapato", "")
        dependencia = data.get("dependencia", "")
        rh = data.get("rh", "")
        nom_cont1 = data.get("nombre_contacto1", "")               
        par_cont1 = data.get("parentesco_contacto1", "")
        tel_cont1 = data.get("telefono_contacto1", "")
        afp = data.get("afp", "")
        nivel_educativo = data.get("niveleducativo", "")
        tipo_vivienda = data.get("tipovivienda", "")
        tipo_hogar = data.get("tipohogar", "")
        nucleo_familiar = data.get("personasnucleofamiliar", "")
        grupo_social = data.get("gruposocial", "")
        discapacidad = data.get("tipodiscapacidad", "")
        poblacion_especial = data.get("poblacionespecial", "")
        enfermedad = data.get("enfermedad", "")
        tipo_transporte = data.get("tipotransporte", "")
        tiempo_trabajo = data.get("tiempollegartrabajo", "")
        grado_escolaridad = data.get("gradoescolaridad", "")
        estcivil = data.get("estadoCivil", "")
        nacionalidad = data.get("nacionalidad", "")
        num_hijos_str = data.get("numhijos")
        
        try:
            num_hijos = int(num_hijos_str) if num_hijos_str is not None else None
        except ValueError:
            return jsonify({"error": "El campo 'numeroHijos' debe ser un número entero"}), 400
        
        accion = data.get("accion", "")
        
        if accion not in ('Insertar', 'Actualizar', 'Estado'):
            return jsonify({"error": "El valor del campo 'accion' no es valido solo se admiten valores 'Insertar', 'Actualizar', 'Estado'"}), 400  

        if accion == "Estado" and 'estado' not in data:
            return jsonify({"error": "Campo 'estado' es requerido"}), 400            
        
        estado = data.get("estado", "")
        
        conn = get_connection()
        cursor = conn.cursor()
        

        
        query = f"""              
        INSERT INTO {TABLE_NAME} (cor_id,                    emp_tipo_registro,              emp_estado,             emp_identificacion,
                                  emp_nombres,               emp_apellidos,                  emp_nacimiento,         emp_genero,
                                  emp_direccion,             emp_telefono,                   emp_email,              emp_cargo,
                                  emp_ingreso,               emp_final_prev_contrato,        emp_retiro,             emp_EPS,
                                  emp_ARL_riesgo,            emp_talla_superior,             emp_talla_inferior,     emp_talla_zapato,
                                  emp_dependencia,           emp_rh,                         emp_nom_cont1,          emp_par_cont1,
                                  emp_tel_cont1,             emp_AFP,                        emp_add_niveleducativo, emp_add_tipovivienda,
                                  emp_add_tipohogar,         emp_add_personasnucleofamiliar, emp_add_gruposocial,    emp_add_tipodiscapacidad,
                                  emp_add_poblacionespecial, emp_add_enfermedad,             emp_add_tipotransporte, emp_add_tiempollegartrabajo,
                                  emp_add_gradoescolaridad,  emp_estcivil,                   emp_nacionalidad,       emp_numhijos) 
                           values (?,                        ?,                              ?,                       ?,   
                                   ?,                        ?,                              ?,                       ?,
                                   ?,                        ?,                              ?,                       ?,
                                   ?,                        ?,                              ?,                       ?, 
                                   ?,                        ?,                              ?,                       ?,
                                   ?,                        ?,                              ?,                       ?,
                                   ?,                        ?,                              ?,                       ?,
                                   ?,                        ?,                              ?,                       ?, 
                                   ?,                        ?,                              ?,                       ?,
                                   ?,                        ?,                              ?,                       ?)
        """
        datVar = (7,                       accion,                         estado,                  identificacion, 
                  nombres,                 apellidos,                      fecha_nacimiento,        genero, 
                  direccion,               telefono,                       email,                   cargo,       
                  fecha_ingreso,           fecha_final_prev,               fecha_retiro,            eps, 
                  arl,                     talla_superior,                 talla_inferior,          talla_zapato,
                  dependencia,             rh,                             nom_cont1,               par_cont1,
                  tel_cont1,               afp,                            nivel_educativo,         tipo_vivienda,
                  tipo_hogar,              nucleo_familiar,                grupo_social,            discapacidad,
                  poblacion_especial,      enfermedad,                     tipo_transporte,         tiempo_trabajo,
                  grado_escolaridad,       estcivil,                       nacionalidad,            num_hijos)                           
        cursor.execute(query,datVar)
        conn.commit()
        
        cursor.execute(f"SELECT emp_imp_error FROM {TABLE_NAME} WHERE emp_identificacion = ? and emp_estado_registro = ?", (identificacion,0))
        error_list = cursor.fetchone()[0]
        conn.commit()
        
        if error_list =="":
            if accion == "Insertar":
                return jsonify({"message": "Empleado creado exitosamente"}), 201
            else:
                return jsonify({"message": "Empleado actualizado"}), 200
        else:
            return jsonify({"error(es)": error_list}), 400 
        
        
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
            
@app.route('/api7empleados', methods=['GET'])
@token_required(TOKENS['AMARILLO'])
def obtener7_empleados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Consulta la vista
        cursor.execute(f"SELECT * FROM {VIEW_NAME_7}")

        # Obtener nombres de columnas (cabeceras)
        columns = [column[0] for column in cursor.description]

        # Convertir resultados en una lista de diccionarios
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return jsonify(rows), 200  #respuesta HTTP 200 OK

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api8empleados', methods=['GET'])
@token_required(TOKENS['JARAMILLO'])
def obtener_empleados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Consulta la vista
        cursor.execute(f"SELECT * FROM {VIEW_NAME_8}")

        # Obtener nombres de columnas (cabeceras)
        columns = [column[0] for column in cursor.description]

        # Convertir resultados en una lista de diccionarios
        #rows = [dict(zip(columns, row)) for row in cursor.fetchall()] # con el ultimo campo
        rows = []
        for row in cursor.fetchall():
            # Crear dict sin el último campo
            item = dict(zip(columns, row))
            item.pop(columns[-1], None)  # <-- ESTA LÍNEA EXCLUYE EL ÚLTIMO CAMPO

            rows.append(item)

        return jsonify(rows), 200  #respuesta HTTP 200 OK

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500

    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api8empleados/<string:identificacion>/foto', methods=['GET'])
@token_required(TOKENS['JARAMILLO'])
def obtener_foto_empleado(identificacion):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Obtener solo la URL del empleado
        cursor.execute(
            f"SELECT {VIEW_NAME_8}.* FROM {VIEW_NAME_8} WHERE identificacion = %s",
            (identificacion,)
        )

        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Empleado no encontrado"}), 404

        columns = [col[0] for col in cursor.description]
        url = row[-1]  # el último campo es la URL

        base64_image = url_to_base64(url)

        return jsonify({
            "identificacion": identificacion,
            "foto_base64": base64_image
        }), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detalle": str(e)}), 500
    
    finally:
        if 'conn' in locals():
            conn.close()
