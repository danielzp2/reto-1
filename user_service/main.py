# Librerías
from fastapi import FastAPI
from config.database import check_connection
from routes.user_routes import router as user_router  # Importamos el router de usuarios
from middlewares.logging_middleware import LoggingMiddleware # Importar el middleware de logging    


# Crear instancia de la aplicación FastAPI
app = FastAPI(
    title="User Service API",
    description="API para gestión de usuarios con FastAPI y MongoDB",
    version="1.0.0"
)

app.add_middleware(LoggingMiddleware)

# Evento que se ejecuta al iniciar la app
@app.on_event("startup")
async def startup_event():
    print("Iniciando aplicación")
    await check_connection()

# Registrar rutas de usuario
app.include_router(user_router)

# Endpoint simple para probar la API
@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "FastAPI funcionando correctamente"}

# Punto de entrada para ejecutar la app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
