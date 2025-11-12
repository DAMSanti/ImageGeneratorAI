# 📚 Lista de Modelos Disponibles - Image Generator AI

## 🎨 Modelos de Generación (Text-to-Image)

### Modelos Rápidos (⚡)
- **Stable Diffusion v1.5** - `runwayml/stable-diffusion-v1-5`
  - Rápido y equilibrado (512x512)
  - Perfecto para RTX 1070

### Modelos de Calidad Media (🎨)
- **Stable Diffusion v2.1** - `stabilityai/stable-diffusion-2-1`
  - Mejor que v1.5, pero más lento
  - Mejor manejo de prompts en lenguaje natural

### Modelos XL (🔥)
- **Stable Diffusion XL Base 1.0** - `stabilityai/stable-diffusion-xl-base-1.0`
  - Excelente calidad (1024x1024)
  - Más pesado pero superior
  - Con SDXL-Refiner para post-procesamiento

- **SDXL Turbo** - `stabilityai/sdxl-turbo`
  - SDXL pero rápido (solo 4 steps)
  - Ideal para GPU limitada

### Modelos Alternativos

#### Fotorrealistas (📸)
- **Proteus v0.2** - `dataautogpt3/Proteus`
  - Fotorrealismo extremo
  - Excelente para personas y objetos reales

- **Epic Realism** - `Lykon/DreamShaper`
  - Realismo épico y cinematográfico
  - Muy detallado

#### Artísticos (🎭)
- **Animagine XL 2.0** - `Linaqruf/animagine-xl-2.0`
  - Anime de ultra alta calidad
  - Basado en SDXL

---

## ✨ VAEs (Variational Autoencoders)

Los VAEs afectan la calidad visual y el aspecto de las imágenes:

- **VAE por defecto** - Estándar del modelo
- **VAE MSE FP32** - Más detalles, más lento
- **VAE FP32 Fix** - Mejor estabilidad numérica
- **VAE Cleaner** - Colores más limpios y vibrantes

---

## 🎨 LoRAs (Low-Rank Adaptations)

Carpeta: `/loras/`

Ejemplos populares:
- `Add Details` - Añade más detalle fino
- `Better-Hands` - Mejora manos (problema común)
- `Cinematic` - Efecto cinematográfico
- `Detail-LoRA` - Detalles mejorados
- `More-Details` - Más detalles generales

---

## 🚫 Embeddings Negativos

Carpeta: `/embeddings/`

Ejemplos:
- `BadDream` - Previene artefactos y sueños malos
- `BadHands` - Evita manos deformes
- `BadPrompt` - Arregla problemas de prompts
- `EasyNegative` - Filtro general de baja calidad
- `UnrealisticDream` - Evita efectos irreales

---

## 🔍 Upscalers

Carpeta: `/upscalers/`

- `RealESRGAN_x2` - Upscale 2x
- `RealESRGAN_x4` - Upscale 4x
- `RealESRGAN_x4_Anime` - Upscale 4x optimizado para anime

---

## 📥 Cómo Agregar Modelos

### Opción 1: Desde la App (⭐ Recomendado)
1. Abre la app en `http://localhost:3001`
2. Ve a la sección "📥 Descargar de Civitai"
3. Busca el modelo deseado
4. Haz clic en "⬇️ Descargar"
5. El sistema lo coloca automáticamente en la carpeta correcta

**Ventaja**: Interfaz gráfica, no necesita terminal

### Opción 2: Usar `download_models.py`
```bash
python download_models.py download --model proteus --type model
python download_models.py download --model animagine --type model
```

### Opción 3: Descargar Manualmente
1. Ve a [HuggingFace](https://huggingface.co/models?pipeline_tag=text-to-image) o [Civitai](https://civitai.com/models)
2. Descarga el modelo
3. Coloca los archivos en `/models/{nombre}/` (o `/loras/`, `/embeddings/`, etc)

El sistema detectará automáticamente:
- Archivos `.safetensors`
- Archivos `.pt` y `.ckpt`
- Carpetas con `model_index.json`

---

## 🔑 API Key de Civitai (Opcional)

Para descargas más rápidas sin límites, puedes agregar tu API key:

1. Ve a https://civitai.com/user/account
2. Copia tu API Token
3. Crea una variable de entorno:
   ```bash
   # Windows PowerShell
   $env:CIVITAI_API_KEY = "tu_token_aqui"
   
   # Linux/Mac
   export CIVITAI_API_KEY="tu_token_aqui"
   ```
4. Reinicia el backend

**Sin API key**: Funciona igual, solo con límites de descarga más bajos

---

## 🚀 Recomendaciones por GPU

### RTX 1070 (8GB VRAM)
- **Mejor**: Stable Diffusion v1.5 con 512x512
- **Aceptable**: SDXL Turbo con steps bajos
- **Usar**: `dtype=float16` en el backend

### RTX 3090 (24GB VRAM)
- **Mejor**: SDXL completo con 1024x1024
- **Recomendado**: Proteus o Epic Realism
- **Usar**: `dtype=float32` para máxima calidad

### H200 (141GB VRAM)
- **Todo funcionará**: Todos los modelos sin restricción
- **Recomendado**: SDXL XL + Refiner en paralelo
- **Potencial**: Batch processing de 10+ imágenes

---

## 🔗 Enlaces Útiles

- **HuggingFace Models**: https://huggingface.co/models?pipeline_tag=text-to-image
- **Civitai (LoRAs y modelos)**: https://civitai.com/
- **ModelScope**: https://modelscope.cn/
- **Hugging Face Docs**: https://huggingface.co/docs

---

## 💡 Tips

1. **Primero prueba modelos rápidos** con tus datos
2. **Usa LoRAs + embeddings** para mejorar resultados sin cambiar modelo
3. **Experimenta con VAEs** para encontrar el mejor aspecto
4. **Upscalea al final** para imágenes más grandes
5. **Guarda seeds** que te gusten para reproducibilidad

---

*Última actualización: Nov 2025*
