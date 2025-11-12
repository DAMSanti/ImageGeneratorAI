# 🚀 Guía Rápida - Descarga de Modelos desde Civitai

## ¿Qué acabamos de agregar?

### ✨ Nuevas Características

1. **Descargador Visual de Civitai** - Interfaz en la app para descargar modelos
2. **Búsqueda en Civitai** - Busca modelos directamente desde la app
3. **Modelos Populares** - Lista curada de modelos más descargados
4. **API Backend** - Endpoints para interactuar con Civitai

### 📁 Archivos Nuevos

- `backend/civitai_downloader.py` - Clase para descargar desde Civitai
- `components/CivitaiDownloader.tsx` - Interfaz React
- Endpoints en `backend/main.py`:
  - `GET /api/civitai/search` - Buscar modelos
  - `GET /api/civitai/trending` - Modelos trending
  - `POST /api/civitai/download` - Descargar modelo
  - `GET /api/civitai/popular` - Modelos recomendados

---

## 🎯 Cómo Usar

### Desde la App (Interfaz Gráfica)

1. **Inicia el sistema**:
   ```bash
   npm run dev:all
   ```

2. **Abre en navegador**:
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8000/docs

3. **Ve a "📥 Descargar Modelos"**

4. **Busca o elige populares**:
   - Escribe en la barra: "Proteus", "Anime", "Photorealistic"
   - O haz clic en "⭐ Ver Modelos Populares"

5. **Descarga con un clic**:
   - El sistema la descarga automáticamente
   - Se coloca en la carpeta correcta (`/models`, `/loras`, etc)
   - Aparece en el desplegable del generador

### Desde Python (Línea de Comandos)

```python
from backend.civitai_downloader import CivitaiDownloader
from pathlib import Path

# Crear descargador
downloader = CivitaiDownloader()

# Opción 1: Buscar y descargar por nombre
downloader.download_by_name("Proteus", Path("./models"), "Checkpoint")

# Opción 2: Descarga directa si conoces los IDs
downloader.download_model(
    model_id=275988,  # Proteus
    version_id=12345,
    output_dir=Path("./models"),
    model_type="Checkpoint"
)

# Opción 3: Búsqueda
models = downloader.search_models("anime", model_type="Checkpoint", limit=5)
for model in models:
    print(f"{model['name']} - {model['downloadCount']} descargas")
```

---

## 🔑 (Opcional) API Key de Civitai

Para descargas sin límite de tasa:

### Obtener API Key
1. Ve a https://civitai.com/user/account
2. Copia tu **API Token**

### Configurar
```bash
# PowerShell
$env:CIVITAI_API_KEY = "tu_api_key_aqui"

# CMD
set CIVITAI_API_KEY=tu_api_key_aqui

# Linux/Mac
export CIVITAI_API_KEY="tu_api_key_aqui"
```

### Verificar
```bash
python -c "import os; print(os.getenv('CIVITAI_API_KEY', 'No configurado'))"
```

---

## 📊 Modelos Recomendados

### Para Empezar (Rápidos)
- **Stable Diffusion v1.5** - Rápido, equilibrado
- **SDXL Turbo** - SDXL en 4 steps

### Fotorrealismo (Realistas)
- **Proteus v0.2** - El mejor fotorrealismo
- **Cyberrealistic** - Fotorrealismo cibernético
- **Epic Realism** - Cinematográfico

### Estilo Artístico
- **DreamShaper 7** - Versatilidad, anime
- **Deliberate v2** - Muy controlable
- **Animagine XL 2.0** - Anime ultra HD

### Alternativas
- **Stable Diffusion XL** - Balance calidad/velocidad
- **SDXL Refiner** - Refinamiento de detalles

---

## 🎮 Flujo Típico de Uso

```
1. Abre app en http://localhost:3001
   ↓
2. Haz clic en "📥 Descargar Modelos"
   ↓
3. Busca "Proteus" o ve a "Populares"
   ↓
4. Haz clic en "⬇️ Descargar"
   ↓
5. Espera a que termine (🟢 se pone verde)
   ↓
6. Ve a la pestaña "🎨 Generador"
   ↓
7. Selecciona "Proteus" en el desplegable de modelos
   ↓
8. Escribe tu prompt y genera 🎨
```

---

## 🐛 Solución de Problemas

### ❌ "Error buscando en Civitai"
- Verifica que el backend esté corriendo
- Comprueba conexión a internet
- Prueba con un término más genérico

### ❌ "Error descargando"
- El archivo puede ser muy grande (>5GB)
- Verifica espacio en disco
- Intenta con una versión más pequeña

### ❌ El modelo no aparece en el desplegable
- Reinicia el backend
- Verifica que está en la carpeta correcta
- Comprueba que la extensión es `.safetensors` o `.pt`

### ❌ Descarga muy lenta
- Agrega tu API key de Civitai
- Cierra otras descargas
- Intenta en otra hora

---

## 💾 Estructura de Carpetas

Después de descargar, verás:

```
proyecto/
├── models/              # Checkpoints
│   ├── Proteus/
│   ├── Dreamshaper/
│   └── ...
├── loras/              # LoRAs
│   ├── Better-Hands/
│   └── ...
├── embeddings/         # Embeddings negativos
│   ├── BadDream/
│   └── ...
└── vaes/              # VAEs
```

---

## 📈 Rendimiento según GPU

| GPU | Modelo Recomendado | Resolución | Velocidad |
|-----|-------------------|-----------|----------|
| **RTX 1070** | SD v1.5 | 512x512 | ~45 seg |
| **RTX 2060** | SD v1.5 | 512x512 | ~30 seg |
| **RTX 3090** | SDXL | 1024x1024 | ~20 seg |
| **H200** | Cualquiera | Máxima | ~5 seg |

---

## 🔗 Enlaces Útiles

- **Civitai**: https://civitai.com/models
- **HuggingFace**: https://huggingface.co/models?pipeline_tag=text-to-image
- **API Civitai**: https://github.com/civitai/civitai-node
- **Docs Diffusers**: https://huggingface.co/docs/diffusers

---

## 💡 Tips Avanzados

### Descargar múltiples modelos
```python
modelos = ["Proteus", "Dreamshaper", "Deliberate"]
for nombre in modelos:
    downloader.download_by_name(nombre, Path("./models"), "Checkpoint")
    print(f"✅ {nombre} descargado")
```

### Automatizar búsqueda de LoRAs
```python
loras = downloader.search_models("hands", model_type="LoRA", limit=10)
print(f"Encontradas {len(loras)} LoRAs para manos")
```

### Batching de descargas
```python
# Descargar todos los trending
trending = downloader.get_trending_models(limit=30)
for model in trending[:5]:  # Los 5 mejores
    # Descargar...
```

---

## 📱 Próximas Mejoras Planeadas

- [ ] Descarga de múltiples modelos a la vez
- [ ] Gestor de descargas con pausar/reanudar
- [ ] Previsualización de modelos antes de descargar
- [ ] Caché de búsquedas para offline
- [ ] Estadísticas de modelos (uso de VRAM, tiempo de gen)

---

*Creado: Nov 2025 | Última actualización: Nov 2025*
