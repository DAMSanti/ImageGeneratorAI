# Setup Detallado - Image Generator AI

## 🖥️ Requisitos del Sistema

### Hardware
- **GPU**: RTX 1070 8GB (mínimo)
  - RTX 2060: ~6GB VRAM
  - RTX 2070: ~8GB VRAM
  - RTX 3060: ~12GB VRAM
  - H200: 141GB VRAM (para escalado)
- **RAM**: 16GB mínimo, 32GB recomendado
- **Almacenamiento**: 50GB libre (modelos + generaciones)
- **CPU**: Intel i7 / AMD Ryzen 5 (cualquier generación reciente)

### Software
- Windows 10/11 o Linux (Ubuntu 20.04+)
- Node.js 18+ ([descargar](https://nodejs.org/))
- Python 3.10+ ([descargar](https://www.python.org/))
- Git ([descargar](https://git-scm.com/))

## 🚀 Instalación Paso a Paso

### Paso 1: Instalar CUDA Toolkit (para GPU NVIDIA)

**Windows:**
```bash
# Descargar desde: https://developer.nvidia.com/cuda-downloads
# Seleccionar: Windows → x86_64 → Windows 11 (o tu versión)

# Verificar instalación
nvidia-smi

# Deberías ver algo como:
# NVIDIA-SMI 536.99    Driver Version: 536.99    CUDA Version: 12.2
```

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install -y nvidia-driver-525
sudo apt-get install -y nvidia-utils

# Reiniciar
sudo reboot

# Verificar
nvidia-smi
```

### Paso 2: Instalar Ollama (para modelo LLM - opcional pero recomendado)

```bash
# Windows: Descargar desde https://ollama.ai/download
# Linux:
curl https://ollama.ai/install.sh | sh

# Descargar modelo
ollama pull mistral

# Iniciar servidor (en background)
ollama serve
```

### Paso 3: Clonar Proyecto y Instalar Dependencias

```bash
# Clonar o navegar a directorio
cd c:\Users\santiagota\source\repos\ImageGeneratorAI

# Instalar dependencias Node.js
npm install

# Instalar dependencias Python
python -m venv venv

# Activar virtual environment
# Windows:
venv\Scripts\activate
# Linux:
source venv/bin/activate

# Instalar paquetes Python
pip install -r requirements.txt

# Descargar modelo Stable Diffusion (primera vez ~7GB)
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
```

### Paso 4: Configurar Variables de Entorno

Crear `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
PYTHON_API_HOST=localhost
PYTHON_API_PORT=8000
HF_TOKEN=tu_token_huggingface  # Opcional para modelos privados
```

Crear `.env` (backend):
```
DEVICE=cuda  # o "cpu" si no tienes GPU
MODEL_NAME=stable-diffusion-v1-5
OUTPUT_DIR=./generated_images
```

### Paso 5: Iniciar Servicios

**Terminal 1 - Backend Python:**
```bash
# Asegúrate de tener venv activado
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend Next.js:**
```bash
npm run dev
```

**Terminal 3 (Opcional) - Ollama:**
```bash
ollama serve
```

### Paso 6: Acceder a la Aplicación

```
Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

## 🔧 Configuración de Modelos

### Cambiar Modelo de Base

En `backend/main.py`:

```python
# Modelos disponibles
MODEL_OPTIONS = {
    "sd-v1-5": "runwayml/stable-diffusion-v1-5",
    "sd-xl": "stabilityai/stable-diffusion-xl-base-1.0",
    "sd-turbo": "stabilityai/sd-turbo",
}

# Usar en generación
model_name = "sd-xl"  # Más calidad pero más lento
```

### Agregar LoRA Personalizado

```python
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe.load_lora_weights("path/to/lora_weights.safetensors", adapter_name="custom")
```

### Optimizar para RTX 1070 (8GB VRAM)

```python
import torch
from diffusers import StableDiffusionPipeline

# Cargar con precisión reducida
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,  # Usa half precision
    safety_checker=None,  # Desactiva si necesitas VRAM
)

# Mover a GPU
pipe = pipe.to("cuda")

# Habilitar memory efficient attention
pipe.enable_memory_efficient_attention()

# Enable VAE tiling (para imágenes grandes)
pipe.enable_vae_tiling()
```

## 🎯 Optimizaciones para RTX 1070

### 1. Reducir Resolución
```
Máximo recomendado: 768x768
Óptimo: 512x512
```

### 2. Reducir Steps
```
Normal: 20-30 steps
RTX 1070: 12-20 steps
```

### 3. Usar Half Precision (float16)
```python
torch_dtype=torch.float16
```

### 🆘 Si se ejecuta lentamente:

1. **Reducir dimensiones** a 512x512
2. **Reducir steps** a 15
3. **Usar sampler más rápido**: Euler A o LMS
4. **Desactivar safety checker**
5. **Usar quantización**: 8-bit o 4-bit

## 📊 Monitoreo

### Ver uso de GPU en tiempo real

```bash
# Windows
nvidia-smi -l 1  # Actualiza cada 1 segundo

# Linux
watch nvidia-smi
```

### Ver logs del backend

```bash
# Los logs aparecen en la terminal donde corriste uvicorn
# Buscar errores CUDA si hay problemas
```

## 🐳 Deployment a H200

### Crear imagen Docker

```bash
npm run docker:build
```

### Subir a H200

```bash
# Crear archivo docker-compose.yml con GPU support
docker run -p 3000:3000 -p 8000:8000 --gpus all image-generator-ai:latest
```

## 🆘 Troubleshooting

### Error: "CUDA out of memory"
```
Solución:
1. Reduce width/height a 512x512
2. Reduce steps a 10-15
3. Reduce guidance_scale a 5-7
4. Activa memory_efficient_attention()
```

### Error: "Module not found"
```
pip install -r requirements.txt
```

### Error: "Could not load model"
```
# Verifica conexión a internet
# Comprueba que HuggingFace está disponible
# Intenta descargar manualmente:
python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
```

### RTX 1070 muy lenta
```
Optimizaciones:
1. torch.float16 en lugar de float32
2. enable_memory_efficient_attention()
3. Reducir resolución
4. Reducir steps
5. Usar sampler: Euler A
```

## 📚 Referencias

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Diffusers Docs](https://huggingface.co/docs/diffusers)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [NVIDIA CUDA Setup](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
