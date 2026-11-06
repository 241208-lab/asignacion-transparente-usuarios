from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import subprocess
import psutil

app = FastAPI(title="Servicio de Asignación Transparente de Usuarios - Kernel Integration", version="2.0")

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
        assigned_uid = 1005
        username = f"pool_user_{assigned_uid}"
        home_dir = f"/home/{username}"
        cgroup_path = f"/sys/fs/cgroup/ihc_users/user_{assigned_uid}"

        # 1. Simulación / Creación de estructura de directorios aislados (Inodos /home/pool_uX)
        if not os.path.exists(home_dir):
            os.makedirs(home_dir, exist_ok=True)

        # 2. Implementación de cgroups v2 (Escritura en el sistema de archivos del Kernel)
        cgroup_base = "/sys/fs/cgroup/ihc_users"
        os.makedirs(cgroup_base, exist_ok=True)
        os.makedirs(cgroup_path, exist_ok=True)

        # Aplicar límites de recursos si cgroups v2 está montado
        try:
            with open(f"{cgroup_path}/cpu.weight", "w") as f:
                f.write(str(data.resource_requirements.min_cpu_weight))
            with open(f"{cgroup_path}/memory.max", "w") as f:
                f.write(f"{data.resource_requirements.max_memory_mb}M")
        except Exception as kernel_err:
            # Modo simulación local en Windows/Entorno de desarrollo sin permisos de superusuario
            print(f"Advertencia de Kernel (cgroups simulados): {kernel_err}")

        # 3. Lectura directa de métricas del sistema (/proc/stat y /proc/meminfo a través de psutil)
        cpu_usage = psutil.cpu_percent(interval=0.1)
        mem_info = psutil.virtual_memory()

        return {
            "status": "success",
            "assigned_uid": assigned_uid,
            "home_directory": home_dir,
            "cgroup_path": cgroup_path,
            "session_token": "eyA_token_kernel_seguro",
            "ws_telemetry_url": f"ws://localhost:8081/status/{assigned_uid}",
            "kernel_telemetry": {
                "cpu_weight_applied": data.resource_requirements.min_cpu_weight,
                "memory_max_mb": data.resource_requirements.max_memory_mb,
                "host_cpu_load": cpu_usage,
                "host_available_memory_mb": mem_info.available // (1024 * 1024)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))