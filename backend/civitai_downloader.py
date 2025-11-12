"""
Descargador de modelos desde Civitai
Requiere API key de https://civitai.com/user/account
"""

import os
import requests
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class CivitaiDownloader:
    """Descarga modelos, LoRAs, embeddings, etc. desde Civitai"""
    
    BASE_URL = "https://api.civitai.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el descargador de Civitai
        
        Args:
            api_key: Token de Civitai (opcional, pero recomendado para más descargas)
        """
        self.api_key = api_key or os.getenv("CIVITAI_API_KEY")
        self.headers = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def search_models(self, query: str, model_type: str = "Checkpoint", limit: int = 10) -> List[dict]:
        """
        Busca modelos en Civitai
        
        Args:
            query: Término de búsqueda (ej: "anime", "photorealistic", "proteus")
            model_type: Tipo de modelo ("Checkpoint", "LoRA", "Embeddings", "VAE")
            limit: Número máximo de resultados
            
        Returns:
            Lista de modelos encontrados
        """
        params = {
            "query": query,
            "type": model_type,
            "limit": limit,
            "sort": "Highest Rated"
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}/models", params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            models = []
            for item in data.get("items", []):
                model_info = {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "description": item.get("description", ""),
                    "type": item.get("type"),
                    "downloadCount": item.get("stats", {}).get("downloadCount", 0),
                    "rating": item.get("stats", {}).get("rating", 0),
                    "versions": []
                }
                
                # Obtener versiones
                for version in item.get("modelVersions", []):
                    version_info = {
                        "id": version.get("id"),
                        "name": version.get("name"),
                        "downloadUrl": version.get("downloadUrl"),
                        "files": version.get("files", [])
                    }
                    model_info["versions"].append(version_info)
                
                models.append(model_info)
            
            return models
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error buscando en Civitai: {e}")
            return []
    
    def download_model(
        self,
        model_id: int,
        version_id: int,
        output_dir: Path,
        model_type: str = "Checkpoint"
    ) -> Optional[Path]:
        """
        Descarga un modelo específico desde Civitai
        
        Args:
            model_id: ID del modelo en Civitai
            version_id: ID de la versión específica
            output_dir: Directorio donde guardar
            model_type: Tipo para organizar (Checkpoint, LoRA, etc)
            
        Returns:
            Ruta del archivo descargado o None si falló
        """
        try:
            # Obtener detalles de la versión
            response = requests.get(
                f"{self.BASE_URL}/models/{model_id}/versions/{version_id}",
                headers=self.headers
            )
            response.raise_for_status()
            version_data = response.json()
            
            # Organizar por tipo
            type_dir = output_dir / model_type.lower()
            type_dir.mkdir(parents=True, exist_ok=True)
            
            # Descargar el archivo principal
            download_url = version_data.get("downloadUrl")
            if not download_url:
                logger.error("No download URL found")
                return None
            
            filename = f"{version_data.get('name', 'model')}.safetensors"
            filepath = type_dir / filename
            
            logger.info(f"Descargando {filename}...")
            response = requests.get(download_url, stream=True, headers=self.headers)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            logger.info(f"Progreso: {percent:.1f}%")
            
            logger.info(f"✅ Descargado a: {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error descargando modelo: {e}")
            return None
    
    def get_trending_models(self, limit: int = 20) -> List[dict]:
        """Obtiene modelos trending en Civitai"""
        return self.search_models("*", model_type="Checkpoint", limit=limit)
    
    def download_by_name(
        self,
        model_name: str,
        output_dir: Path,
        model_type: str = "Checkpoint"
    ) -> Optional[Path]:
        """
        Busca y descarga un modelo por nombre
        
        Args:
            model_name: Nombre del modelo (ej: "Proteus", "Dreamshaper")
            output_dir: Directorio de salida
            model_type: Tipo de modelo
            
        Returns:
            Ruta del archivo descargado
        """
        # Buscar el modelo
        models = self.search_models(model_name, model_type=model_type, limit=1)
        
        if not models:
            logger.error(f"Modelo '{model_name}' no encontrado")
            return None
        
        model = models[0]
        if not model["versions"]:
            logger.error(f"No hay versiones disponibles para {model_name}")
            return None
        
        # Descargar la primera versión (más reciente)
        version = model["versions"][0]
        
        return self.download_model(
            model["id"],
            version["id"],
            output_dir,
            model_type
        )


# Modelos populares de Civitai que recomendamos
CIVITAI_POPULAR_MODELS = {
    "Checkpoints": [
        {
            "name": "Proteus v0.2",
            "civitai_id": 275988,
            "description": "Fotorrealismo extremo, detalles increíbles",
            "downloads": 500000,
        },
        {
            "name": "DreamShaper 7",
            "civitai_id": 112902,
            "description": "Estilo artístico, versátil, anime",
            "downloads": 1000000,
        },
        {
            "name": "Deliberate v2",
            "civitai_id": 95798,
            "description": "Muy controlable, calidad consistente",
            "downloads": 800000,
        },
        {
            "name": "Cyberrealistic",
            "civitai_id": 174616,
            "description": "Fotorrealismo cibernético",
            "downloads": 600000,
        },
        {
            "name": "LORA",
            "civitai_id": 168906,
            "description": "Modelo ligero y rápido",
            "downloads": 400000,
        },
    ],
    "LoRAs": [
        {
            "name": "Better Hands",
            "description": "Mejora significativa de manos",
        },
        {
            "name": "Add Details",
            "description": "Añade más detalle fino a todo",
        },
        {
            "name": "Cinematic",
            "description": "Efecto cinematográfico profesional",
        },
        {
            "name": "Detail Tweaker",
            "description": "Control fino de detalles",
        },
    ],
    "Embeddings": [
        {
            "name": "BadDream",
            "description": "Elimina artefactos y sueños malos",
        },
        {
            "name": "EasyNegative",
            "description": "Filtro general de baja calidad",
        },
        {
            "name": "BadHands",
            "description": "Evita manos deformes",
        },
    ],
}


if __name__ == "__main__":
    import sys
    
    # Ejemplo de uso
    downloader = CivitaiDownloader()
    
    # Buscar modelos
    print("🔍 Buscando modelos 'Proteus'...")
    models = downloader.search_models("Proteus", model_type="Checkpoint", limit=5)
    
    for model in models:
        print(f"\n✨ {model['name']}")
        print(f"   Descargas: {model['downloadCount']:,}")
        print(f"   Rating: {model['rating']:.1f}⭐")
        print(f"   Versiones: {len(model['versions'])}")
