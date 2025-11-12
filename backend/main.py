from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from pathlib import Path
import torch
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    StableDiffusionInpaintPipeline,
    AutoencoderKL,
    DPMSolverMultistepScheduler,
)
from datetime import datetime
import uuid
import logging
from typing import Optional
from backend.enhancement import (
    LoRAManager,
    ControlNetManager,
    Upscaler,
    NegativeEmbedding,
    Image2ImageProcessor,
    InpaintingProcessor,
)
from PIL import Image
import io

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Image Generator AI Backend", version="0.2.0")

# Rutas base para modelos
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
VAES_DIR = BASE_DIR / "vaes"
LORAS_DIR = BASE_DIR / "loras"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
CONTROLNETS_DIR = BASE_DIR / "controlnets"
UPSCALERS_DIR = BASE_DIR / "upscalers"

# Crear directorios si no existen
for directory in [MODELS_DIR, VAES_DIR, LORAS_DIR, EMBEDDINGS_DIR, CONTROLNETS_DIR, UPSCALERS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def scan_local_models(folder: Path, extensions: tuple = (".pt", ".safetensors", ".ckpt")) -> dict:
    """Escanea una carpeta en busca de modelos locales"""
    models = {}
    if not folder.exists():
        return models
    
    for item in folder.iterdir():
        if item.is_dir():
            # Buscar archivos de modelo dentro del directorio
            for file in item.iterdir():
                if file.suffix in extensions or (item / "model_index.json").exists():
                    models[item.name] = {
                        "name": item.name,
                        "path": str(item),
                        "type": "local",
                        "description": f"Modelo local: {item.name}",
                    }
                    break
        elif item.is_file() and item.suffix in extensions:
            # Archivo de modelo individual
            name = item.stem
            models[name] = {
                "name": name,
                "path": str(item),
                "type": "local_file",
                "description": f"Modelo: {name}",
            }
    
    return models


def get_available_models() -> dict:
    """Obtiene modelos disponibles: locales + Hugging Face"""
    local_models = scan_local_models(MODELS_DIR)
    
    # Modelos por defecto de Hugging Face (si no hay locales)
    default_models = {
        # Modelos rápidos
        "stable-diffusion-v1-5": {
            "name": "Stable Diffusion v1.5",
            "model_id": "runwayml/stable-diffusion-v1-5",
            "type": "huggingface",
            "description": "⚡ Rápido, equilibrado (512x512)",
        },
        # Modelos de mejor calidad
        "stable-diffusion-v2-1": {
            "name": "Stable Diffusion v2.1",
            "model_id": "stabilityai/stable-diffusion-2-1",
            "type": "huggingface",
            "description": "🎨 Mejor calidad pero más lento",
        },
        # Modelos XL
        "stable-diffusion-xl": {
            "name": "Stable Diffusion XL Base 1.0",
            "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
            "type": "huggingface",
            "description": "🔥 Excelente calidad (1024x1024)",
        },
        "sdxl-turbo": {
            "name": "SDXL Turbo",
            "model_id": "stabilityai/sdxl-turbo",
            "type": "huggingface",
            "description": "⚡ SDXL rápido (4 steps)",
        },
        # Modelos alternativos
        "animagine": {
            "name": "Animagine XL 2.0",
            "model_id": "Linaqruf/animagine-xl-2.0",
            "type": "huggingface",
            "description": "🎌 Anime de alta calidad",
        },
    }
    
    # Combinar: locales tienen prioridad
    return {**default_models, **local_models}


def get_available_vaes() -> dict:
    """Obtiene VAEs disponibles: locales + Hugging Face"""
    local_vaes = scan_local_models(VAES_DIR)
    
    default_vaes = {
        "default": {
            "name": "VAE por defecto",
            "vae_id": None,
            "type": "huggingface",
            "description": "✨ VAE estándar del modelo",
        },
        "vae-ft-mse-840000": {
            "name": "VAE MSE Fp32",
            "vae_id": "stabilityai/sd-vae-ft-mse-840000",
            "type": "huggingface",
            "description": "🎯 Más detalles (más lento)",
        },
        "vae-fp32": {
            "name": "VAE FP32 Fix",
            "vae_id": "madebyollin/sdxl-vae-fp16-fix",
            "type": "huggingface",
            "description": "🔧 Mejor estabilidad",
        },
        "vae-cleaner": {
            "name": "VAE Cleaner",
            "vae_id": "openai/CLIP-ViT-L-14",
            "type": "huggingface",
            "description": "🧹 Colores más limpios",
        },
    }
    
    return {**default_vaes, **local_vaes}


def get_available_loras() -> dict:
    """Obtiene LoRAs disponibles locales"""
    return scan_local_models(LORAS_DIR)


def get_available_embeddings() -> dict:
    """Obtiene embeddings negativos disponibles"""
    return scan_local_models(EMBEDDINGS_DIR, extensions=(".pt", ".safetensors", ".bin"))


def get_available_controlnets() -> dict:
    """Obtiene ControlNets disponibles"""
    return scan_local_models(CONTROLNETS_DIR)


def get_available_upscalers() -> dict:
    """Obtiene upscalers disponibles"""
    return scan_local_models(UPSCALERS_DIR, extensions=(".pth", ".pt", ".safetensors"))


# Obtener modelos disponibles
AVAILABLE_MODELS = get_available_models()
AVAILABLE_VAES = get_available_vaes()

# Estado global
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INFO] Usando device: {DEVICE}")

current_model_id = None
pipe = None
img2img_pipe = None
inpaint_pipe = None
upscaler = Upscaler()
current_lora = None

def load_model(model_key: str, vae_key: str = "default"):
    """Carga un modelo específico con VAE personalizado"""
    global pipe, img2img_pipe, inpaint_pipe, current_model_id

    if model_key not in AVAILABLE_MODELS:
        raise ValueError(f"Modelo no disponible: {model_key}")

    if vae_key not in AVAILABLE_VAES:
        raise ValueError(f"VAE no disponible: {vae_key}")

    model_info = AVAILABLE_MODELS[model_key]
    vae_info = AVAILABLE_VAES[vae_key]

    print(f"[INFO] Cargando modelo: {model_info['name']}")

    # Descargar modelo anterior si existe
    if pipe is not None:
        del pipe
        if img2img_pipe is not None:
            del img2img_pipe
        if inpaint_pipe is not None:
            del inpaint_pipe
        if DEVICE == "cuda":
            torch.cuda.empty_cache()

    # Cargar modelo principal
    try:
        model_source = model_info.get("path") or model_info.get("model_id")
        pipe = StableDiffusionPipeline.from_pretrained(
            model_source,
            torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
            safety_checker=None,
            local_files_only=model_info.get("type") == "local",
        )
    except Exception as e:
        print(f"[WARN] Error con dtype/revision, intentando con defaults: {e}")
        model_source = model_info.get("path") or model_info.get("model_id")
        pipe = StableDiffusionPipeline.from_pretrained(
            model_source,
            safety_checker=None,
            local_files_only=model_info.get("type") == "local",
        )

    # Cargar VAE si se especifica
    if vae_info.get("vae_id") or vae_info.get("path"):
        print(f"[INFO] Cargando VAE: {vae_info['name']}")
        try:
            vae_source = vae_info.get("path") or vae_info.get("vae_id")
            vae = AutoencoderKL.from_pretrained(
                vae_source,
                torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
                local_files_only=vae_info.get("type") == "local",
            )
            pipe.vae = vae
        except Exception as e:
            print(f"[WARN] Error cargando VAE: {e}")

    # Optimizaciones para GPU
    pipe = pipe.to(DEVICE)
    if DEVICE == "cuda":
        pipe.enable_attention_slicing()
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            pipe.scheduler.config,
            algorithm_type="dpmsolver",
            use_karras_sigmas=True,
        )

    # Crear pipelines Image2Image e Inpaint basados en este modelo
    img2img_pipe = StableDiffusionImg2ImgPipeline(**pipe.components)
    inpaint_pipe = StableDiffusionInpaintPipeline(**pipe.components)

    current_model_id = model_key
    print(f"[INFO] Modelo cargado exitosamente: {model_info['name']}")
    return True

# Cargar modelo inicial
try:
    # Usar el primer modelo disponible
    first_model = list(AVAILABLE_MODELS.keys())[0] if AVAILABLE_MODELS else None
    if first_model:
        load_model(first_model, "default")
    else:
        print(f"[ERROR] No hay modelos disponibles")
        pipe = None
except Exception as e:
    print(f"[ERROR] No se pudo cargar el modelo inicial: {e}")
    pipe = None

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
    model: str = "stable-diffusion-v1-5"
    vae: str = "default"
    use_karras: bool = True
    lora_path: Optional[str] = None
    lora_scale: float = 0.75
    upscale_factor: int = 0  # 0 = no upscale, 2 o 4
    negative_embedding: Optional[str] = None


class Image2ImageRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    steps: int = 20
    guidance_scale: float = 7.5
    seed: int = 0
    strength: float = 0.8  # 0.0-1.0, qué tanto cambiar
    model: str = "stable-diffusion-v1-5"
    vae: str = "default"
    lora_path: Optional[str] = None
    lora_scale: float = 0.75
    # Base64 de imagen o URL


class InpaintRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    steps: int = 20
    guidance_scale: float = 7.5
    seed: int = 0
    model: str = "stable-diffusion-v1-5"
    vae: str = "default"
    # Base64 de imagen + máscara


class ControlNetRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    steps: int = 20
    guidance_scale: float = 7.5
    seed: int = 0
    controlnet_type: str  # openpose, depth, canny, etc.
    conditioning_scale: float = 1.0
    # Base64 de imagen de control


class ModelChangeRequest(BaseModel):
    model: str
    vae: str = "default"


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Backend is running",
        "device": DEVICE,
        "current_model": current_model_id,
    }


@app.post("/api/generate")
async def generate_image(request: GenerateRequest):
    """
    Genera una imagen usando Stable Diffusion con opciones avanzadas.
    Soporta: LoRA, Upscaler, Negative Embeddings
    """
    if pipe is None:
        return {"success": False, "error": "Modelo no cargado. Verifica las dependencias."}

    if not request.prompt.strip():
        return {"success": False, "error": "El prompt no puede estar vacío."}

    try:
        # Cambiar modelo si es diferente
        if request.model != current_model_id:
            print(f"[INFO] Cambiando modelo a {request.model}")
            load_model(request.model, request.vae)

        print(f"[INFO] Generando imagen - Prompt: {request.prompt}")
        print(f"[INFO] Parámetros: steps={request.steps}, guidance={request.guidance_scale}, model={request.model}, vae={request.vae}")

        # Cargar LoRA si se especifica
        if request.lora_path:
            logger.info(f"Cargando LoRA: {request.lora_path}")
            LoRAManager.load_lora(pipe, request.lora_path, request.lora_scale)

        # Cargar Negative Embedding si se especifica
        if request.negative_embedding:
            logger.info(f"Cargando Negative Embedding: {request.negative_embedding}")
            NegativeEmbedding.load_embedding(pipe, request.negative_embedding)
            # Agregar token al negative prompt
            if request.negative_embedding not in request.negative_prompt:
                request.negative_prompt += f", {request.negative_embedding}"

        # Generar imagen
        with torch.no_grad():
            if request.seed == 0:
                request.seed = int(torch.randint(0, 1000000, (1,)).item())

            result = pipe(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                num_inference_steps=request.steps,
                guidance_scale=request.guidance_scale,
                height=request.height,
                width=request.width,
                generator=torch.Generator(device=DEVICE).manual_seed(request.seed),
            )

        image = result.images[0]

        # Upscalear si se solicita
        if request.upscale_factor in [2, 4]:
            logger.info(f"Upscaleando imagen x{request.upscale_factor}")
            upscaled_image = upscaler.upscale(image, request.upscale_factor)
            if upscaled_image:
                image = upscaled_image

        # Descargar LoRA para liberar memoria
        if request.lora_path:
            LoRAManager.unload_lora(pipe)

        # Guardar imagen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}_{uuid.uuid4().hex[:8]}.png"
        image_path = GENERATIONS_DIR / filename
        image.save(image_path)

        # Guardar metadatos (prompts, parámetros) en JSON
        metadata = {
            "filename": filename,
            "timestamp": timestamp,
            "prompt": request.prompt,
            "negative_prompt": request.negative_prompt,
            "model": request.model,
            "vae": request.vae,
            "lora": request.lora_path,
            "lora_scale": request.lora_scale,
            "negative_embedding": request.negative_embedding,
            "steps": request.steps,
            "guidance_scale": request.guidance_scale,
            "seed": request.seed,
            "width": request.width,
            "height": request.height,
            "upscale_factor": request.upscale_factor,
        }
        
        metadata_path = image_path.with_suffix(".json")
        import json
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        image_url = f"http://localhost:8000/api/image/{filename}"

        logger.info(f"Imagen guardada en: {image_path}")
        logger.info(f"Metadatos guardados en: {metadata_path}")

        return {
            "success": True,
            "image_url": image_url,
            "filename": filename,
            "prompt": request.prompt,
            "seed": request.seed,
            "parameters": {
                "steps": request.steps,
                "guidance_scale": request.guidance_scale,
                "model": request.model,
                "vae": request.vae,
                "width": request.width,
                "height": request.height,
                "lora": request.lora_path,
                "lora_scale": request.lora_scale,
                "upscale_factor": request.upscale_factor,
                "negative_embedding": request.negative_embedding,
            },
        }
    except Exception as e:
        logger.error(f"Error generando imagen: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


@app.get("/api/last-metadata")
async def get_last_metadata():
    """Obtiene los metadatos de la última imagen generada"""
    try:
        # Buscar el archivo JSON más reciente
        json_files = list(GENERATIONS_DIR.glob("generated_*.json"))
        if not json_files:
            return {"success": False, "error": "No hay imágenes generadas"}
        
        latest_json = max(json_files, key=lambda p: p.stat().st_mtime)
        
        import json
        with open(latest_json, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        return {"success": True, "metadata": metadata}
    except Exception as e:
        logger.error(f"Error obteniendo metadatos: {e}")
        return {"success": False, "error": str(e)}


@app.get("/api/gallery")
async def get_gallery():
    """Retorna lista de todas las imágenes generadas con sus metadatos"""
    try:
        images = []
        
        # Buscar todas las imágenes PNG
        png_files = sorted(GENERATIONS_DIR.glob("generated_*.png"), reverse=True)
        
        for png_file in png_files:
            json_file = png_file.with_suffix(".json")
            
            image_info = {
                "filename": png_file.name,
                "url": f"http://localhost:8000/api/image/{png_file.name}",
                "timestamp": png_file.stat().st_mtime,
            }
            
            # Cargar metadatos si existen
            if json_file.exists():
                import json
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                    image_info["metadata"] = metadata
                except:
                    pass
            
            images.append(image_info)
        
        return {
            "success": True,
            "total": len(images),
            "images": images
        }
    except Exception as e:
        logger.error(f"Error en galería: {e}")
        return {"success": False, "error": str(e), "images": []}


@app.get("/api/models")
async def list_models():
    """Retorna lista de modelos disponibles"""
    return {
        "models": [
            {
                "id": key,
                "name": info["name"],
                "description": info["description"],
            }
            for key, info in get_available_models().items()
        ]
    }


@app.get("/api/vaes")
async def list_vaes():
    """Retorna lista de VAEs disponibles"""
    return {
        "vaes": [
            {
                "id": key,
                "name": info["name"],
                "description": info["description"],
            }
            for key, info in get_available_vaes().items()
        ]
    }


@app.get("/api/loras")
async def list_loras():
    """Retorna lista de LoRAs disponibles"""
    loras = get_available_loras()
    return {
        "loras": [
            {
                "id": key,
                "name": info["name"],
                "description": info.get("description", f"LoRA: {key}"),
                "path": info["path"],
            }
            for key, info in loras.items()
        ],
        "note": "Puedes colocar LoRAs en la carpeta /loras"
    }


@app.get("/api/embeddings")
async def list_embeddings():
    """Retorna lista de embeddings negativos disponibles"""
    embeddings = get_available_embeddings()
    return {
        "embeddings": [
            {
                "id": key,
                "name": info["name"],
                "description": info.get("description", f"Embedding: {key}"),
                "path": info["path"],
            }
            for key, info in embeddings.items()
        ],
        "note": "Puedes colocar embeddings en la carpeta /embeddings"
    }


@app.get("/api/controlnets")
async def list_controlnets():
    """Retorna lista de ControlNets disponibles"""
    controlnets = get_available_controlnets()
    return {
        "controlnets": [
            {
                "id": key,
                "name": info["name"],
                "description": info.get("description", f"ControlNet: {key}"),
                "path": info["path"],
            }
            for key, info in controlnets.items()
        ],
        "note": "Puedes colocar ControlNets en la carpeta /controlnets"
    }


@app.get("/api/upscalers")
async def list_upscalers():
    """Retorna lista de upscalers disponibles"""
    upscalers = get_available_upscalers()
    return {
        "upscalers": [
            {
                "id": key,
                "name": info["name"],
                "description": info.get("description", f"Upscaler: {key}"),
                "path": info["path"],
            }
            for key, info in upscalers.items()
        ],
        "note": "Puedes colocar upscalers en la carpeta /upscalers"
    }


@app.post("/api/load-model")
async def load_model_endpoint(request: ModelChangeRequest):
    """Carga un modelo diferente"""
    try:
        load_model(request.model, request.vae)
        return {
            "success": True,
            "message": f"Modelo {AVAILABLE_MODELS[request.model]['name']} cargado",
            "current_model": current_model_id,
        }
    except Exception as e:
        print(f"[ERROR] Error cargando modelo: {e}")
        return {"success": False, "error": str(e)}


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


@app.get("/api/image/{filename}")
async def get_image(filename: str):
    """Descarga una imagen generada"""
    image_path = GENERATIONS_DIR / filename
    if not image_path.exists():
        return {"success": False, "error": "Imagen no encontrada"}
    return FileResponse(image_path, media_type="image/png")




@app.get("/api/controlnets")
async def list_controlnets():
    """Retorna lista de ControlNets disponibles"""
    controlnets = get_available_controlnets()
    return {
        "controlnets": [
            {
                "id": key,
                "name": info["name"],
                "description": info.get("description", f"ControlNet: {key}"),
                "path": info["path"],
            }
            for key, info in controlnets.items()
        ],
        "note": "Puedes colocar ControlNets en la carpeta /controlnets"
    }


@app.get("/api/negative-embeddings")
async def list_negative_embeddings():
    """Retorna lista de embeddings negativos disponibles"""
    embeddings = get_available_embeddings()
    return {
        "embeddings": [
            {
                "id": key,
                "name": info["name"],
                "description": info.get("description", f"Embedding: {key}"),
                "path": info["path"],
            }
            for key, info in embeddings.items()
        ],
        "note": "Puedes colocar embeddings en la carpeta /embeddings"
    }


@app.post("/api/image2image")
async def image_to_image(request: Image2ImageRequest, image_file: UploadFile = File(...)):
    """
    Transforma una imagen existente manteniendo su estructura
    Soporta: cambio de estilo, Image2Image
    """
    if img2img_pipe is None:
        return {"success": False, "error": "Modelo no cargado."}

    try:
        # Leer imagen
        image_data = await image_file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")

        logger.info(f"[Image2Image] Procesando imagen: {image.size}")

        # Cambiar modelo si es necesario
        if request.model != current_model_id:
            load_model(request.model, request.vae)

        # Preparar imagen
        image = Image2ImageProcessor.prepare_image(image, 512, 512)

        # Generar
        with torch.no_grad():
            if request.seed == 0:
                request.seed = int(torch.randint(0, 1000000, (1,)).item())

            result = img2img_pipe(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                image=image,
                strength=request.strength,
                num_inference_steps=request.steps,
                guidance_scale=request.guidance_scale,
                generator=torch.Generator(device=DEVICE).manual_seed(request.seed),
            )

        output_image = result.images[0]

        # Guardar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"img2img_{timestamp}_{uuid.uuid4().hex[:8]}.png"
        image_path = GENERATIONS_DIR / filename
        output_image.save(image_path)

        return {
            "success": True,
            "image_url": f"http://localhost:8000/api/image/{filename}",
            "filename": filename,
            "prompt": request.prompt,
            "seed": request.seed,
            "parameters": {
                "steps": request.steps,
                "guidance_scale": request.guidance_scale,
                "strength": request.strength,
                "model": request.model,
                "vae": request.vae,
            },
        }
    except Exception as e:
        logger.error(f"[Image2Image] Error: {e}")
        return {"success": False, "error": str(e)}


# ==================== CIVITAI INTEGRATION ====================

from backend.civitai_downloader import CivitaiDownloader

class DownloadRequest(BaseModel):
    """Solicitud de descarga de modelo"""
    model_id: int
    version_id: int
    model_type: str = "Checkpoint"  # Checkpoint, LoRA, Embeddings, VAE


@app.get("/api/civitai/search")
async def search_civitai_models(query: str, model_type: str = "Checkpoint", limit: int = 10):
    """Busca modelos en Civitai"""
    try:
        downloader = CivitaiDownloader()
        models = downloader.search_models(query, model_type=model_type, limit=limit)
        return {"models": models, "total": len(models)}
    except Exception as e:
        logger.error(f"Error searching Civitai: {e}")
        return {"error": str(e), "models": []}


@app.get("/api/civitai/trending")
async def get_trending_civitai(limit: int = 20):
    """Obtiene modelos trending de Civitai"""
    try:
        downloader = CivitaiDownloader()
        models = downloader.get_trending_models(limit=limit)
        return {"models": models, "total": len(models)}
    except Exception as e:
        logger.error(f"Error getting trending: {e}")
        return {"error": str(e), "models": []}


@app.post("/api/civitai/download")
async def download_from_civitai(request: DownloadRequest):
    """
    Descarga un modelo desde Civitai
    
    Ejemplo:
    {
        "model_id": 275988,
        "version_id": 12345,
        "model_type": "Checkpoint"
    }
    """
    try:
        downloader = CivitaiDownloader()
        
        # Determinar directorio según tipo
        type_map = {
            "Checkpoint": MODELS_DIR,
            "LoRA": LORAS_DIR,
            "Embeddings": EMBEDDINGS_DIR,
            "VAE": VAES_DIR,
        }
        
        output_dir = type_map.get(request.model_type, MODELS_DIR)
        
        filepath = downloader.download_model(
            request.model_id,
            request.version_id,
            output_dir,
            request.model_type
        )
        
        if filepath:
            return {
                "success": True,
                "message": f"Descargado a: {filepath}",
                "path": str(filepath)
            }
        else:
            return {
                "success": False,
                "error": "Error descargando el modelo",
                "path": None
            }
            
    except Exception as e:
        logger.error(f"Error en descarga de Civitai: {e}")
        return {"success": False, "error": str(e), "path": None}


@app.get("/api/civitai/popular")
async def get_popular_civitai():
    """Obtiene lista de modelos populares de Civitai"""
    from backend.civitai_downloader import CIVITAI_POPULAR_MODELS
    return {"popular": CIVITAI_POPULAR_MODELS}


@app.get("/")
async def root():
    return {
        "name": "Image Generator AI Backend",
        "version": "0.2.0",
        "docs": "/docs",
        "health": "/health",
        "features": [
            "text-to-image",
            "image-to-image",
            "lora-support",
            "upscaler",
            "negative-embeddings",
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
