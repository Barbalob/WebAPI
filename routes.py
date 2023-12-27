from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import schemas
from db.database import get_db
from sqlalchemy.orm import Session
from crud import (create_user, get_users, get_user, update_user, delete_user,create_school, get_schools, get_school, update_school, delete_school)

router_websocket = APIRouter()
router_users = APIRouter(prefix='/user', tags=['user'])
router_schools = APIRouter(prefix='/school', tags=['school'])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"User #{client_id} joined")
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"User #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User #{client_id} left")


@router_users.post("/", response_model=schemas.User)
async def create_user_route(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_data)
    await notify_clients(f"User added: {user.name}")
    return user


@router_users.get("/", response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return users


@router_users.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    return user


@router_users.patch("/{user_id}", response_model=schemas.User)
async def update_user_route(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user_data)
    if updated_user:
        await notify_clients(f"User updated: {updated_user.name}")
        return updated_user
    return {"message": "User not found"}


@router_users.delete("/{user_id}")
async def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user(db, user_id)
    if deleted:
        await notify_clients(f"User deleted: ID {user_id}")
        return {"message": "User deleted"}
    return {"message": "User not found"}


@router_schools.post("/", response_model=schemas.School)
async def create_school_route(schema: schemas.SchoolCreate, db: Session = Depends(get_db)):
    school = create_school(db, schema)
    await notify_clients(f"School added: {school.name}")
    return school


@router_schools.get("/", response_model=List[schemas.School])
async def read_schools(db: Session = Depends(get_db)):
    schools = get_schools(db)
    return schools


@router_schools.get("/{school_id}", response_model=schemas.School)
async def read_school(school_id: int, db: Session = Depends(get_db)):
    school = get_school(db, school_id)
    return school


@router_schools.patch("/{school_id}")
async def update_school_route(school_id: int, schema: schemas.SchoolUpdate, db: Session = Depends(get_db)):
    updated_school = update_school(db, school_id, schema)
    if updated_school:
        await notify_clients(f"School updated: {updated_school.name}")
        return updated_school
    return {"message": "School not found"}


@router_schools.delete("/{school_id}")
async def delete_school_route(school_id: int, db: Session = Depends(get_db)):
    deleted = delete_school(db, school_id)
    if deleted:
        await notify_clients(f"School deleted: ID {school_id}")
        return {"message": "School deleted"}
    return {"message": "School not found"}
