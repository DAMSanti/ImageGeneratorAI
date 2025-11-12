from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from pathlib import Path

app = FastAPI(title="Image Generator AI Backend", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio de generaciones
GENERATIONS_DIR = Path("./generated_images")
GENERATIONS_DIR.mkdir(exist_ok=True)


class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    steps: int = 20
    guidance_scale: float = 7.5
    seed: int = 0
    width: int = 512
    height: int = 512
    sampler: str = "DPM++ 2M"


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running"}


@app.post("/api/generate")
async def generate_image(request: GenerateRequest):
    """
    Genera una imagen usando Stable Diffusion local.
    
    Para esta versión, retornamos una imagen de placeholder.
    El backend real usaría Ollama + ComfyUI o diffusers.
    """
    try:
        # Aquí irá la lógica de generación real
        # Por ahora retornamos un placeholder
        return {
            "success": True,
            "image_url": "https://via.placeholder.com/512x512?text=Generated+Image",
            "prompt": request.prompt,
            "parameters": {
                "steps": request.steps,
                "guidance_scale": request.guidance_scale,
                "seed": request.seed,
                "sampler": request.sampler,
            },
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/models")
async def list_models():
    """Retorna lista de modelos disponibles"""
    return {
        "models": [
            {
                "id": "stable-diffusion-xl",
                "name": "Stable Diffusion XL",
                "description": "Modelo base de alta calidad",
            },
            {
                "id": "stable-diffusion-v1-5",
                "name": "Stable Diffusion v1.5",
                "description": "Modelo estándar optimizado",
            },
        ]
    }


@app.get("/api/samplers")
async def list_samplers():
    """Retorna lista de samplers disponibles"""
    return {
        "samplers": [
            "DPM++ 2M",
            "DPM++ 2M Karras",
            "Euler",
            "Euler A",
            "Heun",
            "LMS",
            "LMS Karras",
        ]
    }


@app.get("/")
async def root():
    return {
        "name": "Image Generator AI Backend",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
