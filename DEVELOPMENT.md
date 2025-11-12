# Development Guide

## 🛠️ Estructura del Proyecto

```
ImageGeneratorAI/
├── app/                    # Next.js App Router
│   ├── api/               # API routes (proxy a backend)
│   ├── page.tsx           # Home page
│   ├── layout.tsx         # Root layout
│   └── globals.css        # Global styles
├── components/            # React components
│   ├── Header.tsx         # Header
│   ├── GeneratorForm.tsx  # Formulario principal
│   ├── ImagePreview.tsx   # Preview de imagen
│   └── Gallery.tsx        # Galería
├── hooks/                 # Custom React hooks
│   ├── useGenerator.ts    # Lógica de generación
│   └── useGallery.ts      # Lógica de galería
├── types/                 # TypeScript types
│   ├── generation.ts      # Tipos de generación
│   └── api.ts             # Tipos de API
├── lib/                   # Utilidades
│   └── api.ts             # Cliente HTTP
├── backend/               # Python FastAPI
│   ├── main.py           # Aplicación principal
│   ├── routes/           # Rutas API
│   ├── services/         # Lógica negocio
│   └── models/           # Esquemas Pydantic
├── public/                # Archivos estáticos
├── requirements.txt       # Dependencias Python
├── package.json          # Dependencias Node
├── next.config.cjs       # Config Next.js
├── tailwind.config.js    # Config Tailwind
└── tsconfig.json         # Config TypeScript
```

## 🔄 Flujo de Datos

```
Frontend (Next.js)
    ↓
User fills GeneratorForm
    ↓
handleGenerate() → POST /api/generate (Frontend proxy)
    ↓
NextJS API Route
    ↓
Proxy to Backend (FastAPI)
    ↓
Backend: POST /api/generate
    ↓
Load Stable Diffusion Model
    ↓
Generate Image
    ↓
Save to disk
    ↓
Return image URL
    ↓
Frontend displays in ImagePreview
```

## 📝 Agregar Nuevo Parámetro

### Ejemplo: Agregar "LoRA Strength"

**1. Backend - `backend/main.py`:**
```python
class GenerateRequest(BaseModel):
    # ... existing fields ...
    lora_scale: float = 1.0  # NEW
```

**2. Frontend - `components/GeneratorForm.tsx`:**
```tsx
const [loraScale, setLoraScale] = useState(1.0);

// En JSX:
<div>
  <label>LoRA Strength: {loraScale.toFixed(1)}</label>
  <input
    type="range"
    min="0"
    max="2"
    step="0.1"
    value={loraScale}
    onChange={(e) => setLoraScale(Number(e.target.value))}
  />
</div>

// En handleGenerate:
body: JSON.stringify({
  // ... otros campos ...
  lora_scale: loraScale,
})
```

**3. API Backend - Procesar parámetro:**
```python
@app.post("/api/generate")
async def generate_image(request: GenerateRequest):
    # ... código ...
    if request.lora_scale != 1.0:
        pipe.set_lora_scale(request.lora_scale)
```

## 🎯 Agregar Nuevo Modelo

### Ejemplo: Agregar FLUX.1

**1. Crear nuevo endpoint:**
```python
@app.post("/api/generate-flux")
async def generate_flux(request: GenerateRequest):
    from diffusers import FluxPipeline
    
    pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell")
    image = pipe(request.prompt).images[0]
    return {"image_url": f"/generated/{image_id}"}
```

**2. Agregar al selector del frontend:**
```tsx
<select value={model} onChange={(e) => setModel(e.target.value)}>
  <option value="sd-xl">Stable Diffusion XL</option>
  <option value="flux">FLUX.1</option>  {/* NEW */}
</select>

// En handleGenerate:
const endpoint = model === "flux" ? "/api/generate-flux" : "/api/generate";
```

## 🔌 Agregar Servicio Externo

### Ejemplo: Integrar con ComfyUI

```python
# backend/services/comfyui_service.py
import httpx

class ComfyUIService:
    def __init__(self, url: str = "http://localhost:8188"):
        self.url = url
    
    async def generate(self, prompt: str, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/api/generate",
                json={"prompt": prompt, **kwargs}
            )
        return response.json()
```

## 🧪 Testing

### Test Backend
```bash
# Ver API docs
http://localhost:8000/docs

# Hacer request directo
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a red car"}'
```

### Test Frontend
```bash
npm run dev
# Ir a http://localhost:3000
# Llenar formulario y probar
```

## 📊 Performance Tuning

### Para RTX 1070

```python
# backend/config.py
CONFIG = {
    "device": "cuda",
    "dtype": torch.float16,  # Half precision
    "enable_attention_slicing": True,
    "enable_vae_tiling": True,
    "max_batch_size": 1,  # No batch processing
    "optimal_steps": 15,  # Rápido sin perder calidad
}
```

### Para H200

```python
CONFIG = {
    "device": "cuda",
    "dtype": torch.float32,  # Full precision
    "enable_attention_slicing": False,
    "max_batch_size": 4,  # Paralelo
    "optimal_steps": 50,  # Alta calidad
}
```

## 🚀 Deployment

### Local a H200 (via Docker)

```bash
# Crear Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-alpine as frontend
WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.10-slim as backend
WORKDIR /app/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .

FROM node:18-alpine
WORKDIR /app
COPY --from=frontend /app/.next ./.next
COPY --from=backend /app/backend ./backend
COPY package.json .
RUN npm install --production
EXPOSE 3000 8000
CMD ["npm", "run", "dev:all"]
EOF

# Build y push
docker build -t image-generator-ai:latest .
docker save image-generator-ai:latest | gzip > image-generator-ai.tar.gz

# En H200:
scp image-generator-ai.tar.gz user@h200:/tmp/
ssh user@h200 'docker load < /tmp/image-generator-ai.tar.gz'
docker run -p 3000:3000 -p 8000:8000 --gpus all image-generator-ai:latest
```

## 📚 Recursos

- [Diffusers API](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/)
- [Next.js Performance](https://nextjs.org/docs/advanced-features/performance)
- [React Hooks](https://react.dev/reference/react)

## 🐛 Debugging

### Habilitar verbose logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Profiling de GPU
```bash
# En otra terminal
nvidia-smi dmon
```

### Console logs frontend
```tsx
console.log("Debug:", { prompt, steps, seed });
```
