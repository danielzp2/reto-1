#librerias 
import motor.motor_asyncio
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# aqui se leen las variables de .env
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "user_db")

# Crear cliente asíncrono
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)

# Seleccionar la base de datos
db = client[DB_NAME]

# Verificación opcional de conexión
async def check_connection():
    try:
        await client.server_info()
        print(f"conexión exitosa: {DB_NAME}")
    except Exception as e:
        print(f"error de conexión: {e}")
