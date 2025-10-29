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

API_TOKEN = os.getenv("API_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiQW1hcmlsbG8iLCJleHAiOjE3OTMyMzI5Mjd9.eT1sa0E-gRmV_cUeYTPRRQhOUb6yNrAqi6N8MgSGpMI")