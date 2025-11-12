# Image Generator AI

**Generador de Imágenes con IA Local** - Web profesional para generar imágenes usando Stable Diffusion en tu RTX 1070 (o superior).

## 🎯 Características

- ✅ **Generación Local** - Usa tu GPU (RTX 1070+) sin depender de APIs cloud
- ✅ **Control Total** - Ajusta todos los parámetros de generación
- ✅ **Interfaz Profesional** - UI moderna con preview en tiempo real
- ✅ **Historial** - Guarda y gestiona todas tus generaciones
- ✅ **Batch Processing** - Genera múltiples imágenes en paralelo
- ✅ **Escalable** - Diseñado para migrar a H200 droplet
- ✅ **Multiidioma** - Soporte para múltiples idiomas (ES, EN, FR, DE, IT)

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│    Frontend: Next.js 14 + React         │
│    (Interfaz en localhost:3000)         │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│  Backend: Python FastAPI                │
│  (API en localhost:8000)                │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│  IA Local: Ollama + ComfyUI             │
│  (Generación en GPU - RTX 1070)         │
└─────────────────────────────────────────┘
```

## 🚀 Requisitos

- **Sistema**: Windows 11 / Linux
- **GPU**: RTX 1070 8GB VRAM (mínimo)
- **RAM**: 16GB (recomendado 32GB)
- **Almacenamiento**: 40GB libre (para modelos)
- **Node.js**: 18+
- **Python**: 3.10+
- **Docker**: Opcional (para H200)

## ⚡ Setup Rápido (5 minutos)

### Paso 1: Instalar Ollama

```bash
# Windows
choco install ollama
# o descarga desde: https://ollama.ai

# Linux
curl https://ollama.ai/install.sh | sh
```

### Paso 2: Descargar Modelo

```bash
ollama pull mistral
# (descarga ~4GB)
```

### Paso 3: Instalar Dependencias

```bash
cd c:\Users\santiagota\source\repos\ImageGeneratorAI
npm install
pip install -r requirements.txt
```

### Paso 4: Iniciar Servicios

```bash
# Terminal 1: Backend
npm run backend

# Terminal 2: Frontend
npm run dev

# Terminal 3: Ollama (si no está en background)
ollama serve
```

### Paso 5: Acceder

```
Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

## 📝 Controles Principales

### Parámetros de Imagen
- **Prompt**: Descripción detallada de lo que quieres generar
- **Negative Prompt**: Lo que NO quieres en la imagen
- **Dimensiones**: Ancho x Alto (512-1024px recomendado)
- **Aspect Ratio**: 1:1, 16:9, 9:16, etc.

### Parámetros de Generación
- **Steps**: 4-50 (más = mejor pero más lento)
- **Guidance Scale**: 1.0-20.0 (adherencia al prompt)
- **Sampler**: DPM++, Euler, Heun, etc.
- **Seed**: Para reproducibilidad (0 = random)

### Modelo
- **Base Model**: Stable Diffusion XL, FLUX, etc.
- **LoRA**: Estilos personalizados (opcional)
- **VAE**: Mejorador de calidad (opcional)

## 🎨 Ejemplos de Uso

### Generación Simple
```
Prompt: "Apartamento moderno, Barcelona, balcón con vista al mar, luz dorada"
Negative: "blurry, low quality, distorted"
Steps: 20
Guidance: 7.5
```

### Batch Processing
```
Generar 5 variaciones del mismo prompt con diferentes seeds
Ahorra tiempo en iteraciones
```

### Historial y Galería
- Todas las imágenes se guardan automáticamente
- Puedes ver el prompt exacto de cada una
- Descarga en alta calidad
- Exporta metadatos

## 📊 Rendimiento Esperado

| GPU | Resolución | Pasos | Tiempo |
|-----|-----------|-------|--------|
| RTX 1070 | 512x512 | 20 | ~45 seg |
| RTX 1070 | 768x768 | 20 | ~120 seg |
| RTX 1070 | 1024x1024 | 20 | ~180 seg |
| H200 | 1024x1024 | 50 | ~20 seg |

## 🐳 Deployment a H200

### Opción 1: Docker (Recomendado)

```bash
# Build imagen
npm run docker:build

# Subir a H200
docker save image-generator-ai:latest | ssh user@h200 docker load

# Ejecutar en H200
ssh user@h200 'docker run -p 3000:3000 -p 8000:8000 --gpus all image-generator-ai:latest'
```

### Opción 2: Manual

```bash
# En H200
git clone <tu-repo>
npm install
pip install -r requirements.txt
npm run dev:all
```

## 🔧 Stack Tecnológico

### Frontend
- **Next.js 14** - Framework React
- **React 18** - UI components
- **TypeScript 5.3** - Type safety
- **Tailwind CSS** - Styling
- **Zustand** - Estado global
- **React Hook Form** - Formularios
- **Axios** - HTTP client

### Backend
- **FastAPI** - API Python
- **Ollama** - Motor IA
- **ComfyUI** - Orquestación
- **SQLAlchemy** - Base de datos
- **Pydantic** - Validación

### IA
- **Stable Diffusion XL** - Modelo base
- **FLUX.1** - Modelo rápido (opcional)
- **LoRA** - Personalización (opcional)

## 📁 Estructura del Proyecto

```
ImageGeneratorAI/
├── app/                      # Frontend Next.js
│   ├── page.tsx             # Home
│   ├── generator/           # Página principal
│   ├── gallery/             # Galería de imágenes
│   ├── history/             # Historial
│   ├── api/                 # Rutas API (proxy)
│   └── layout.tsx
├── components/              # Componentes React
│   ├── GeneratorForm.tsx    # Formulario de generación
│   ├── ImagePreview.tsx     # Vista previa
│   ├── ParameterSliders.tsx # Controles
│   ├── Gallery.tsx          # Galería
│   └── Header.tsx           # Encabezado
├── hooks/                   # Custom hooks
│   ├── useGenerator.ts      # Lógica generación
│   ├── useGallery.ts        # Lógica galería
│   └── useSettings.ts       # Configuraciones
├── types/                   # TypeScript types
│   ├── generation.ts        # Tipos generación
│   └── api.ts               # Tipos API
├── backend/                 # Backend Python FastAPI
│   ├── main.py             # Aplicación principal
│   ├── routes/             # Rutas API
│   │   ├── generate.py     # Generación
│   │   ├── history.py      # Historial
│   │   └── models.py       # Modelos
│   ├── services/           # Lógica negocio
│   │   ├── ollama_service.py
│   │   ├── image_service.py
│   │   └── storage_service.py
│   ├── models/             # Esquemas Pydantic
│   └── config.py           # Configuración
├── public/                  # Archivos estáticos
├── requirements.txt         # Dependencias Python
├── next.config.js          # Config Next.js
├── tsconfig.json           # Config TypeScript
├── tailwind.config.js      # Config Tailwind
├── Dockerfile              # Para H200
└── docker-compose.yml      # Docker compose
```

## 🛠️ Desarrollo

### Agregar Nuevo Parámetro

1. **Backend** (`backend/models/`): Agregar a Pydantic model
2. **Frontend** (`components/`): Agregar slider/input
3. **API** (`backend/routes/`): Procesar parámetro
4. **Hook** (`hooks/`): Actualizar lógica

### Agregar Nuevo Modelo

1. Descargar: `ollama pull nombre-modelo`
2. Backend: Agregar a lista de modelos
3. Frontend: Actualizar selector
4. Testear generación

## 📊 Monitoreo

```bash
# Ver GPU usage
nvidia-smi -l 1

# Ver logs backend
tail -f logs/backend.log

# Ver logs Ollama
tail -f logs/ollama.log
```

## 🐛 Troubleshooting

### Error: CUDA out of memory
```
Solución: Reducir dimensiones o steps, activar quantization
```

### Generación lenta
```
Solución: Usar modelo más pequeño, reducir resolution
```

### Backend no conecta
```
Solución: Verificar puerto 8000, python ejecutándose
```

## 📚 Documentación Completa

Ver archivos:
- `DEVELOPMENT.md` - Guía de desarrollo
- `SETUP.md` - Setup detallado
- `API.md` - Documentación API
- `.github/copilot-instructions.md` - Instrucciones Copilot

## 🤝 Contribuir

Este es un proyecto personal pero está abierto a mejoras.

## 📄 Licencia

MIT

## 📞 Contacto

Santiago Ota - [@DAMSanti](https://github.com/DAMSanti)

---

**Última actualización**: Noviembre 2025
