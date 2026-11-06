from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psutil

app = FastAPI(title="Servicio de Asignación Transparente de Usuarios", version="1.0")

class ResourceRequirements(BaseModel):
    min_cpu_weight: int
    max_memory_mb: int

class AssignRequest(BaseModel):
    client_id: str
    session_type: str
    resource_requirements: ResourceRequirements

@app.post("/api/v1/assign")
def assign_user_session(data: AssignRequest):
    try:
        # Simulación de asignación de UID y cgroups v2 en Linux según el entregable
        assigned_uid = 1005
        cgroup_path = f"/sys/fs/cgroup/ihc_users/user_{assigned_uid}"
        
        # Lectura de métricas básicas del sistema para verificar carga (/proc simulado con psutil)
        cpu_usage = psutil.cpu_percent(interval=0.1)
        mem_info = psutil.virtual_memory()

        return {
            "status": "success",
            "assigned_uid": assigned_uid,
            "cgroup_path": cgroup_path,
            "session_token": "eyA_token_seguro_simulado",
            "ws_telemetry_url": f"ws://localhost:8081/status/{assigned_uid}",
            "system_telemetry": {
                "current_cpu_load": cpu_usage,
                "available_memory_mb": mem_info.available // (1024 * 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))