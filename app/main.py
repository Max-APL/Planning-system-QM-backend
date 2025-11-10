# app/main.py

import asyncio
import logging
import traceback
from typing import List

from fastapi import FastAPI, Request, WebSocket, Depends, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    auth,
    users,
    projects,
    tools,
    materials,
    flow_tools,
    flow_materials,
    stores,
    surplus_project,
    material_allocation,
    tool_allocation,
    used_material,
    purchases_material,
    purchase_material_details,
    purchase_tools,
    purchase_tool_details,
    providers,
    financial,
    inventory,
    management,
)
from app.db.connection import get_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

app = FastAPI()

# Exception handler for request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_trace = traceback.format_exc()
    try:
        body = await request.json()
    except Exception as e:
        body = {"error": f"Unable to parse body: {e}"}

    logging.error(f"Validation error:\n{exc}\nRequest body: {body}\nTraceback:\n{error_trace}")

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": body,
        },
    )

# General exception handler
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://127.0.0.1:8080",  
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router, prefix="/users")
app.include_router(projects.router, prefix="/projects")
app.include_router(tools.router, prefix="/tools")
app.include_router(materials.router, prefix="/materials")
app.include_router(flow_tools.router, prefix="/flow-tools")
app.include_router(flow_materials.router, prefix="/flow-materials")
app.include_router(surplus_project.router, prefix="/surpluses")
app.include_router(material_allocation.router, prefix="/material-allocations")
app.include_router(tool_allocation.router, prefix="/tool-allocations")
app.include_router(used_material.router, prefix="/used-materials")
app.include_router(purchases_material.router, prefix="/purchases-materials")
app.include_router(purchase_material_details.router, prefix="/purchase-material-details")
app.include_router(purchase_tools.router, prefix="/purchase-tools")
app.include_router(purchase_tool_details.router, prefix="/purchase-tool-details")
app.include_router(providers.router, prefix="/providers")
app.include_router(stores.router, prefix="/stores")

app.include_router(inventory.router, prefix="/inventory")
app.include_router(financial.router, prefix="/financial")
app.include_router(management.router, prefix="/management")
    
# WebSocket management
connected_clients: List[WebSocket] = []
# Lista global para manejar clientes conectados
connected_clients_tools = []

@app.websocket("/ws/material")
async def websocket_material(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    logging.info(f"Client connected: {websocket.client}")

    try:
        while True:
            async with get_connection() as conn:
                async with conn.cursor() as cursor:
                    query = """
                        SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO_UNITARIO, CANTIDAD_MINIMA 
                        FROM MATERIAL
                    """
                    await cursor.execute(query)
                    records = await cursor.fetchall()

                    # Formatear los datos
                    data = [
                        {
                            "ID": row[0],
                            "NOMBRE": row[1],
                            "DESCRIPCION": row[2],
                            "CANTIDAD": row[3],
                            "PRECIO_UNITARIO": row[4],
                            "CANTIDAD_MINIMA": row[5],
                        }
                        for row in records
                    ]

            # Broadcast to all connected clients
            disconnected = []
            for client in connected_clients:
                try:
                    await client.send_json(data)
                except Exception as e:
                    logging.error(f"Error sending data to {client.client}: {e}")
                    disconnected.append(client)

            # Remove disconnected clients
            for client in disconnected:
                connected_clients.remove(client)
                logging.info(f"Client disconnected: {client.client}")

            await asyncio.sleep(3)

    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
            logging.info(f"Client disconnected: {websocket.client}")

@app.websocket("/ws/herramienta")
async def websocket_herramienta(websocket: WebSocket):
    await websocket.accept()
    connected_clients_tools.append(websocket)

    try:
        while True:
            # Consulta y envía datos a los clientes conectados
            async with get_connection() as conn:
                async with conn.cursor() as cursor:
                    query = """
                    SELECT ID, NOMBRE, DESCRIPCION, CANTIDAD, PRECIO_UNITARIO, CANTIDAD_MINIMA 
                    FROM HERRAMIENTA
                    """
                    await cursor.execute(query)
                    records = await cursor.fetchall()

                    # Formatear los datos
                    data = [
                        {
                            "ID": row[0],
                            "NOMBRE": row[1],
                            "DESCRIPCION": row[2],
                            "CANTIDAD": row[3],
                            "PRECIO_UNITARIO": row[4],
                            "CANTIDAD_MINIMA": row[5],
                        }
                        for row in records
                    ]

                    # Enviar datos a todos los clientes conectados
                    for client in connected_clients_tools:
                        try:
                            await client.send_json(data)
                        except WebSocketDisconnect:
                            connected_clients_tools.remove(client)

            # Espera 3 segundos antes de enviar la siguiente actualización
            await asyncio.sleep(3)

    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if websocket in connected_clients_tools:
            connected_clients_tools.remove(websocket)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
