from datetime import datetime
from bson import ObjectId

# Modelo base para representar cómo se guarda el usuario en MongoDB
def user_entity(user) -> dict:
    # Convierte un documento de MongoDB a un diccionario serializable por FastAPI.
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }

