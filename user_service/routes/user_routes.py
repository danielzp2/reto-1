#librerias 
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime
import bcrypt
from config.database import db
from schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from models.user import user_entity

router = APIRouter(prefix="/users", tags=["Users"])

# Crear usuario
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    users_collection = db["users"]

    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password.decode("utf-8"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await users_collection.insert_one(new_user)
    created_user = await users_collection.find_one({"_id": result.inserted_id})

    return {
        "message": "Usuario creado",
        "user": user_entity(created_user)
    }

# Obtener usuario por ID
@router.get("/{id}", response_model=UserResponse)
async def get_user(id: str):
    users_collection = db["users"]

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    user = await users_collection.find_one({"_id": ObjectId(id)})

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user_entity(user)

# Actualizar usuario
@router.put("/{id}")
async def update_user(id: str, user_data: UserUpdate):
    users_collection = db["users"]

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    existing_user = await users_collection.find_one({"_id": ObjectId(id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_fields = user_data.dict(exclude_unset=True)

    if "password" in update_fields:
        update_fields["password"] = bcrypt.hashpw(
            update_fields["password"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    update_fields["updated_at"] = datetime.utcnow()

    await users_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": update_fields}
    )

    updated_user = await users_collection.find_one({"_id": ObjectId(id)})

    return {
        "message": "Usuario actualizado",
        "user": user_entity(updated_user)
    }

# Eliminar usuario
@router.delete("/{id}")
async def delete_user(id: str):
    users_collection = db["users"]

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await users_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario eliminado"}
