"""
Script para descargar y gestionar modelos de IA
Descarga modelos de Hugging Face y los organiza en carpetas específicas
"""

import os
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline, AutoencoderKL
import argparse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rutas base
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
VAES_DIR = BASE_DIR / "vaes"
LORAS_DIR = BASE_DIR / "loras"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
CONTROLNETS_DIR = BASE_DIR / "controlnets"
UPSCALERS_DIR = BASE_DIR / "upscalers"

# Crear directorios si no existen
for directory in [MODELS_DIR, VAES_DIR, LORAS_DIR, EMBEDDINGS_DIR, CONTROLNETS_DIR, UPSCALERS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# Modelos disponibles
AVAILABLE_MODELS = {
    "stable-diffusion-v1-5": {
        "model_id": "runwayml/stable-diffusion-v1-5",
        "description": "Stable Diffusion v1.5 - Modelo estándar",
    },
    "stable-diffusion-v2-1": {
        "model_id": "stabilityai/stable-diffusion-2-1",
        "description": "Stable Diffusion v2.1 - Mayor calidad",
    },
}

# VAEs disponibles
AVAILABLE_VAES = {
    "vae-ft-mse-840000": {
        "model_id": "stabilityai/sd-vae-ft-mse-840000",
        "description": "VAE MSE - Mejor preservación de detalles",
    },
}

# ControlNets disponibles
AVAILABLE_CONTROLNETS = {
    "openpose": {
        "model_id": "lllyasviel/control_v11p_openpose",
        "description": "ControlNet OpenPose",
    },
    "depth": {
        "model_id": "lllyasviel/control_v11f1p_sd15_depth",
        "description": "ControlNet Depth",
    },
    "canny": {
        "model_id": "lllyasviel/control_v11p_canny",
        "description": "ControlNet Canny Edges",
    },
}

# Upscalers
AVAILABLE_UPSCALERS = {
    "RealESRGAN_x2": {
        "model_id": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
        "description": "Real-ESRGAN x2 Upscaler",
    },
    "RealESRGAN_x4": {
        "model_id": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x4plus.pth",
        "description": "Real-ESRGAN x4 Upscaler",
    },
}


class ModelDownloader:
    """Descargador de modelos de IA"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Usando device: {self.device}")
    
    def download_model(self, model_name: str, model_type: str = "model"):
        """
        Descarga un modelo específico
        
        Args:
            model_name: Nombre del modelo
            model_type: Tipo de modelo (model, vae, controlnet, upscaler, lora, embedding)
        """
        try:
            if model_type == "model":
                self._download_diffuser_model(model_name, AVAILABLE_MODELS, MODELS_DIR)
            elif model_type == "vae":
                self._download_diffuser_model(model_name, AVAILABLE_VAES, VAES_DIR)
            elif model_type == "controlnet":
                self._download_diffuser_model(model_name, AVAILABLE_CONTROLNETS, CONTROLNETS_DIR)
            elif model_type == "upscaler":
                self._download_upscaler(model_name)
            else:
                logger.error(f"Tipo de modelo no soportado: {model_type}")
        except Exception as e:
            logger.error(f"Error descargando {model_type} {model_name}: {e}")
    
    def _download_diffuser_model(self, model_name: str, available_models: dict, output_dir: Path):
        """Descarga un modelo de diffusers"""
        if model_name not in available_models:
            logger.error(f"Modelo no encontrado: {model_name}")
            return
        
        model_info = available_models[model_name]
        model_id = model_info["model_id"]
        
        logger.info(f"Descargando {model_name}...")
        logger.info(f"Modelo ID: {model_id}")
        
        try:
            # Descargar modelo de Hugging Face
            pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None,
            )
            
            # Guardar modelo localmente
            save_path = output_dir / model_name
            logger.info(f"Guardando modelo en: {save_path}")
            pipeline.save_pretrained(save_path)
            
            logger.info(f"✓ Modelo descargado exitosamente: {model_name}")
        except Exception as e:
            logger.error(f"Error descargando modelo: {e}")
    
    def _download_upscaler(self, upscaler_name: str):
        """Descarga un upscaler"""
        if upscaler_name not in AVAILABLE_UPSCALERS:
            logger.error(f"Upscaler no encontrado: {upscaler_name}")
            return
        
        logger.warning("Descarga de upscalers no implementada aún")
    
    def list_available_models(self, model_type: str = "all"):
        """Lista los modelos disponibles"""
        print("\n=== Modelos Disponibles ===\n")
        
        if model_type in ["all", "model"]:
            print("MODELOS DIFFUSERS:")
            for name, info in AVAILABLE_MODELS.items():
                print(f"  - {name}: {info['description']}")
        
        if model_type in ["all", "vae"]:
            print("\nVAEs:")
            for name, info in AVAILABLE_VAES.items():
                print(f"  - {name}: {info['description']}")
        
        if model_type in ["all", "controlnet"]:
            print("\nCONTROLNETS:")
            for name, info in AVAILABLE_CONTROLNETS.items():
                print(f"  - {name}: {info['description']}")
        
        if model_type in ["all", "upscaler"]:
            print("\nUPSCALERS:")
            for name, info in AVAILABLE_UPSCALERS.items():
                print(f"  - {name}: {info['description']}")
        
        print("\n")
    
    def list_downloaded_models(self):
        """Lista los modelos ya descargados"""
        print("\n=== Modelos Descargados ===\n")
        
        print("MODELOS:")
        if MODELS_DIR.exists():
            models = [d.name for d in MODELS_DIR.iterdir() if d.is_dir()]
            if models:
                for model in models:
                    print(f"  - {model}")
            else:
                print("  (ninguno)")
        
        print("\nVAES:")
        if VAES_DIR.exists():
            vaes = [d.name for d in VAES_DIR.iterdir() if d.is_dir()]
            if vaes:
                for vae in vaes:
                    print(f"  - {vae}")
            else:
                print("  (ninguno)")
        
        print("\nLORAS:")
        if LORAS_DIR.exists():
            loras = [d.name for d in LORAS_DIR.iterdir() if d.is_dir()]
            if loras:
                for lora in loras:
                    print(f"  - {lora}")
            else:
                print("  (ninguno)")
        
        print("\nEMBEDDINGS:")
        if EMBEDDINGS_DIR.exists():
            embeddings = [d.name for d in EMBEDDINGS_DIR.iterdir() if d.is_dir()]
            if embeddings:
                for emb in embeddings:
                    print(f"  - {emb}")
            else:
                print("  (ninguno)")
        
        print("\n")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Descargador de modelos de IA")
    parser.add_argument(
        "command",
        choices=["download", "list", "list-downloaded"],
        help="Comando a ejecutar"
    )
    parser.add_argument(
        "--model",
        help="Nombre del modelo a descargar"
    )
    parser.add_argument(
        "--type",
        choices=["model", "vae", "controlnet", "upscaler", "lora", "embedding"],
        default="model",
        help="Tipo de modelo"
    )
    
    args = parser.parse_args()
    
    downloader = ModelDownloader()
    
    if args.command == "download":
        if not args.model:
            logger.error("Debe especificar --model")
            return
        downloader.download_model(args.model, args.type)
    
    elif args.command == "list":
        downloader.list_available_models(args.type if args.type != "model" else "all")
    
    elif args.command == "list-downloaded":
        downloader.list_downloaded_models()


if __name__ == "__main__":
    main()
