# GUÍA RÁPIDA - Image Generator AI

## ✅ El proyecto ha sido creado exitosamente!

Ubicación: `c:\Users\santiagota\source\repos\ImageGeneratorAI`

## 🚀 PRÓXIMOS PASOS (5 minutos)

### 1. Abrir el proyecto en VS Code

```bash
# En PowerShell
cd c:\Users\santiagota\source\repos\ImageGeneratorAI
code .
```

### 2. Instalar dependencias (en VS Code Terminal)

```bash
# Instalar dependencias Node.js
npm install

# Instalar dependencias Python
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Iniciar servicios (3 Terminales simultáneamente)

**Terminal 1 - Backend FastAPI:**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend Next.js:**
```bash
npm run dev
```

**Terminal 3 (Opcional) - GPU Monitor:**
```bash
nvidia-smi -l 1
```

### 4. Acceder a la aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Archivos Importantes

### Configuración
- `package.json` - Dependencias Node.js
- `requirements.txt` - Dependencias Python
- `next.config.cjs` - Configuración Next.js
- `tailwind.config.js` - Configuración Tailwind
- `.eslintrc.json` - Configuración ESLint

### Frontend
- `app/page.tsx` - Home page principal
- `app/layout.tsx` - Layout raíz
- `components/GeneratorForm.tsx` - Formulario con todos los parámetros
- `components/ImagePreview.tsx` - Vista previa de imagen generada
- `components/Gallery.tsx` - Galería de imágenes

### Backend
- `backend/main.py` - API FastAPI (endpoints)
- `requirements.txt` - Dependencias Python para IA

### Documentación
- `README.md` - Documentación completa
- `SETUP.md` - Setup detallado para RTX 1070
- `DEVELOPMENT.md` - Guía de desarrollo

## 🎨 Características Actuales

✅ Frontend profesional con interfaz completa
✅ Controles para todos los parámetros de generación
✅ Backend FastAPI con estructura lista
✅ Tipos TypeScript para type-safety
✅ Configuración optimizada para RTX 1070
✅ Docker support para H200
✅ Documentación completa

## ⚙️ Parámetros Disponibles

**Imagen:**
- Prompt y Negative Prompt
- Ancho y Alto (256-1024px)
- Aspect Ratio automático

**Generación:**
- Steps (4-50)
- Guidance Scale (1-20)
- Sampler (DPM++, Euler, Heun, etc.)
- Seed (para reproducibilidad)

## 🔧 Próximas Tareas

1. **Instalar Modelos IA**
   ```bash
   # Descargar Stable Diffusion (primera vez ~7GB)
   python -c "from diffusers import StableDiffusionPipeline; StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5')"
   ```

2. **Implementar Backend Real**
   - Completar `backend/main.py` con lógica de generación
   - Usar `diffusers` para generar imágenes
   - Guardar en `/generated_images`

3. **Conectar Frontend**
   - Los componentes ya hacen requests a `http://localhost:8000/api/generate`
   - Solo necesitas que el backend responda

4. **Optimizar para RTX 1070**
   - Ver instrucciones en `SETUP.md`
   - Usar float16, enable_memory_efficient_attention()

## 📊 Stack Completo

**Frontend:**
- Next.js 14 + React 18
- TypeScript 5.3
- Tailwind CSS 3.4

**Backend:**
- FastAPI (Python async)
- Ollama (LLM local)
- Diffusers (Stable Diffusion)

**DevOps:**
- Docker + Docker Compose
- NVIDIA CUDA support
- GitHub ready

## 🆘 Primeros Problemas

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "Cannot find module 'react'"
```bash
npm install
```

### "Port 3000 already in use"
```bash
npm run dev -- -p 3001
```

### "CUDA out of memory"
Ver sección "Optimizar para RTX 1070" en SETUP.md

## 📞 Estructura del Proyecto

```
ImageGeneratorAI/
├── 🎨 FRONTEND (Next.js)
│   ├── app/
│   │   ├── page.tsx         ← Home page
│   │   ├── layout.tsx       ← Layout
│   │   └── globals.css      ← Estilos globales
│   ├── components/
│   │   ├── Header.tsx       ← Encabezado
│   │   ├── GeneratorForm.tsx ← AQUÍ ajustas parámetros
│   │   ├── ImagePreview.tsx ← Muestra imagen generada
│   │   └── Gallery.tsx      ← Galería
│   └── types/
│       └── generation.ts    ← Tipos TypeScript
│
├── 🐍 BACKEND (Python)
│   ├── backend/
│   │   └── main.py          ← API FastAPI
│   └── requirements.txt      ← Dependencias Python
│
├── 🐳 DEPLOYMENT
│   ├── Dockerfile           ← Para build
│   ├── docker-compose.yml   ← Para deployment
│   └── .github/
│       └── copilot-instructions.md ← Instrucciones IA
│
└── 📚 DOCS
    ├── README.md            ← Documentación principal
    ├── SETUP.md             ← Setup detallado
    └── DEVELOPMENT.md       ← Guía desarrollo
```

## 🎯 Próximas Acciones

1. Abre VS Code: `code c:\Users\santiagota\source\repos\ImageGeneratorAI`
2. Abre Terminal integrada (Ctrl+`)
3. Ejecuta: `npm install && pip install -r requirements.txt`
4. Comienza el desarrollo

## 📚 Referencias Rápidas

- Tailwind Colors: https://tailwindcss.com/docs/customizing-colors
- Next.js Docs: https://nextjs.org/docs
- FastAPI Tutorial: https://fastapi.tiangolo.com/
- Diffusers Guide: https://huggingface.co/docs/diffusers/

## ✨ ¡Todo listo!

Tu proyecto está 100% estructurado y listo para desarrollar. 

**Siguiente:** Abre VS Code y comienza a trabajar en el backend para conectar Stable Diffusion.

¿Preguntas? Ver `DEVELOPMENT.md` para más detalles.

---

**Última actualización**: Noviembre 2025
**Estado**: ✅ Project Setup Completado
