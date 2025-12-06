import os

# Configuración de conexión a SQL Server
DB_CONFIG = {
    "DRIVER": "{ODBC Driver 18 for SQL Server}",
    "SERVER": os.getenv("DB_SERVER", "dataportero.database.windows.net"),
    "DATABASE": os.getenv("DB_NAME", "datacc"),
    "UID": os.getenv("DB_USER", "validacion_documentos"),
    "PWD": os.getenv("DB_PASSWORD", "RRt852*amxb"),
    "TrustServerCertificate": "yes"
}

TOKENS = {
    "AMARILLO": os.getenv("TOKEN_AMARILLO", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiQW1hcmlsbG8iLCJleHAiOjE3OTMyMzI5Mjd9.eT1sa0E-gRmV_cUeYTPRRQhOUb6yNrAqi6N8MgSGpMI"),
    "JARAMILLO": os.getenv("TOKEN_JARAMILLO", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiSmFyYW1pbGxvIiwiZXhwIjoxNzk2NTYyNTEyfQ.OfACYzyeQUw4WC-6RpiUnAzlJejbJdIw1lsNjMthLys")
}

