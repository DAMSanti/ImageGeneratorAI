"""
Script para descargar LoRAs populares desde Civitai
"""

import os
from pathlib import Path
from backend.civitai_downloader import CivitaiDownloader, CIVITAI_POPULAR_MODELS

def download_popular_loras():
    """Descarga los LoRAs populares"""
    downloader = CivitaiDownloader()
    
    loras_dir = Path("./loras")
    loras_dir.mkdir(parents=True, exist_ok=True)
    
    popular_loras = CIVITAI_POPULAR_MODELS.get("LoRAs", [])
    
    print("\n" + "="*60)
    print("📥 Descargador de LoRAs Populares desde Civitai")
    print("="*60)
    
    if not popular_loras:
        print("❌ No hay LoRAs configurados")
        return
    
    for i, lora in enumerate(popular_loras, 1):
        name = lora.get("name", f"LoRA {i}")
        description = lora.get("description", "")
        
        print(f"\n[{i}/{len(popular_loras)}] 📦 {name}")
        print(f"    📝 {description}")
        
        # Buscar en Civitai
        print(f"    🔍 Buscando en Civitai...")
        results = downloader.search_models(name, model_type="LoRA", limit=1)
        
        if results:
            model = results[0]
            if model.get("versions"):
                version = model["versions"][0]
                print(f"    ✅ Encontrado: {model['name']}")
                print(f"    ⬇️  Descargando v{version['name']}...")
                
                filepath = downloader.download_model(
                    model["id"],
                    version["id"],
                    loras_dir,
                    "LoRA"
                )
                
                if filepath:
                    print(f"    ✅ Guardado en: {filepath}")
                else:
                    print(f"    ❌ Error descargando")
            else:
                print(f"    ❌ Sin versiones disponibles")
        else:
            print(f"    ❌ No encontrado en Civitai")
    
    print("\n" + "="*60)
    print("✅ Descarga completada")
    print("="*60)


def download_popular_embeddings():
    """Descarga los embeddings negativos populares"""
    downloader = CivitaiDownloader()
    
    embeddings_dir = Path("./embeddings")
    embeddings_dir.mkdir(parents=True, exist_ok=True)
    
    popular_embeddings = CIVITAI_POPULAR_MODELS.get("Embeddings", [])
    
    print("\n" + "="*60)
    print("📥 Descargador de Embeddings desde Civitai")
    print("="*60)
    
    if not popular_embeddings:
        print("❌ No hay Embeddings configurados")
        return
    
    for i, embedding in enumerate(popular_embeddings, 1):
        name = embedding.get("name", f"Embedding {i}")
        description = embedding.get("description", "")
        
        print(f"\n[{i}/{len(popular_embeddings)}] 🚫 {name}")
        print(f"    📝 {description}")
        
        # Buscar en Civitai
        print(f"    🔍 Buscando en Civitai...")
        results = downloader.search_models(name, model_type="Embeddings", limit=1)
        
        if results:
            model = results[0]
            if model.get("versions"):
                version = model["versions"][0]
                print(f"    ✅ Encontrado: {model['name']}")
                print(f"    ⬇️  Descargando...")
                
                filepath = downloader.download_model(
                    model["id"],
                    version["id"],
                    embeddings_dir,
                    "Embeddings"
                )
                
                if filepath:
                    print(f"    ✅ Guardado en: {filepath}")
                else:
                    print(f"    ❌ Error descargando")
            else:
                print(f"    ❌ Sin versiones disponibles")
        else:
            print(f"    ❌ No encontrado en Civitai")
    
    print("\n" + "="*60)
    print("✅ Descarga completada")
    print("="*60)


if __name__ == "__main__":
    import sys
    
    print("\n🎯 ¿Qué deseas descargar?")
    print("1. LoRAs")
    print("2. Embeddings negativos")
    print("3. Ambos")
    
    choice = input("\nElige una opción (1-3): ").strip()
    
    if choice == "1":
        download_popular_loras()
    elif choice == "2":
        download_popular_embeddings()
    elif choice == "3":
        download_popular_loras()
        download_popular_embeddings()
    else:
        print("❌ Opción inválida")
