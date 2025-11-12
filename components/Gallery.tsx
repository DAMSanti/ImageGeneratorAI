"use client";

import { useState, useEffect } from "react";
import Image from "next/image";

interface ImageMetadata {
  filename: string;
  timestamp: string;
  prompt: string;
  negative_prompt: string;
  model: string;
  seed: number;
  steps: number;
  guidance_scale: number;
  width: number;
  height: number;
  lora?: string;
  upscale_factor?: number;
}

interface GalleryImage {
  filename: string;
  url: string;
  timestamp: number;
  metadata?: ImageMetadata;
}

export default function Gallery() {
  const [images, setImages] = useState<GalleryImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState<GalleryImage | null>(null);
  const [copiedPrompt, setCopiedPrompt] = useState(false);

  useEffect(() => {
    fetchGallery();
    const interval = setInterval(fetchGallery, 3000); // Refrescar cada 3 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchGallery = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/gallery");
      const data = await response.json();
      if (data.success && data.images) {
        setImages(data.images);
      }
    } catch (error) {
      console.error("Error cargando galería:", error);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedPrompt(true);
    setTimeout(() => setCopiedPrompt(false), 2000);
  };

  const downloadImage = async (filename: string) => {
    const link = document.createElement("a");
    link.href = `http://localhost:8000/api/image/${filename}`;
    link.download = filename;
    link.click();
  };

  return (
    <div className="space-y-6">
      <div className="glass-effect rounded-2xl p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white">📸 Galería ({images.length})</h2>
          <button
            onClick={fetchGallery}
            disabled={loading}
            className="px-4 py-2 bg-primary hover:bg-primary/80 rounded-lg font-semibold text-white disabled:opacity-50 transition"
          >
            {loading ? "🔄..." : "🔄 Actualizar"}
          </button>
        </div>

        {images.length === 0 ? (
          <div className="text-center py-12 text-gray-400">
            <p className="text-xl">📭 Aún no hay imágenes generadas</p>
            <p className="text-sm mt-2">Genera tu primera imagen en el generador</p>
          </div>
        ) : (
          <>
            {/* Grid de imágenes */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              {images.map((image) => (
                <div
                  key={image.filename}
                  className="relative group cursor-pointer rounded-lg overflow-hidden bg-white/5 border border-white/10 hover:border-primary hover:border-2 transition-all aspect-square"
                  onClick={() => setSelectedImage(image)}
                >
                  <img
                    src={image.url}
                    alt={image.filename}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  {/* Overlay */}
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-end justify-between p-3">
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <p className="text-white text-xs font-semibold truncate">
                        {image.filename}
                      </p>
                      {image.metadata?.prompt && (
                        <p className="text-gray-300 text-xs truncate line-clamp-1">
                          {image.metadata.prompt}
                        </p>
                      )}
                    </div>
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          downloadImage(image.filename);
                        }}
                        className="p-2 bg-white/20 hover:bg-white/30 rounded-lg"
                        title="Descargar"
                      >
                        ⬇️
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Panel de detalles */}
            {selectedImage && selectedImage.metadata && (
              <div className="glass-effect rounded-2xl p-6 space-y-4">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-bold text-white">📋 Detalles de la Imagen</h3>
                  <button
                    onClick={() => setSelectedImage(null)}
                    className="text-gray-400 hover:text-white text-2xl"
                  >
                    ✕
                  </button>
                </div>

                {/* Prompts */}
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">
                      ✨ Prompt Positivo
                    </label>
                    <div className="bg-white/5 border border-white/10 rounded-lg p-3 text-white relative group">
                      <p className="text-sm break-words pr-10">{selectedImage.metadata.prompt}</p>
                      <button
                        onClick={() => copyToClipboard(selectedImage.metadata!.prompt)}
                        className="absolute top-2 right-2 p-2 bg-white/10 hover:bg-white/20 rounded text-xs opacity-0 group-hover:opacity-100 transition"
                        title="Copiar prompt"
                      >
                        {copiedPrompt ? "✅" : "📋"}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-300 mb-2">
                      🚫 Prompt Negativo
                    </label>
                    <div className="bg-white/5 border border-white/10 rounded-lg p-3 text-white relative group">
                      <p className="text-sm break-words pr-10">
                        {selectedImage.metadata.negative_prompt}
                      </p>
                      <button
                        onClick={() => copyToClipboard(selectedImage.metadata!.negative_prompt)}
                        className="absolute top-2 right-2 p-2 bg-white/10 hover:bg-white/20 rounded text-xs opacity-0 group-hover:opacity-100 transition"
                        title="Copiar prompt"
                      >
                        {copiedPrompt ? "✅" : "📋"}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Parámetros */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">🤖 Modelo</p>
                    <p className="text-white font-semibold">{selectedImage.metadata.model}</p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">🌱 Seed</p>
                    <p className="text-white font-semibold">{selectedImage.metadata.seed}</p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">⚙️ Steps</p>
                    <p className="text-white font-semibold">{selectedImage.metadata.steps}</p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">🎯 Guidance</p>
                    <p className="text-white font-semibold">
                      {selectedImage.metadata.guidance_scale}
                    </p>
                  </div>
                  <div className="bg-white/5 rounded-lg p-3">
                    <p className="text-gray-400 text-xs">📐 Resolución</p>
                    <p className="text-white font-semibold">
                      {selectedImage.metadata.width}x{selectedImage.metadata.height}
                    </p>
                  </div>
                  {selectedImage.metadata.lora && (
                    <div className="bg-white/5 rounded-lg p-3">
                      <p className="text-gray-400 text-xs">🎨 LoRA</p>
                      <p className="text-white font-semibold text-xs truncate">
                        {selectedImage.metadata.lora}
                      </p>
                    </div>
                  )}
                </div>

                {/* Botón para usar estos parámetros */}
                <button
                  onClick={() => {
                    // Copiar los prompts al copiar el formato
                    const fullPrompt = `Prompt: ${selectedImage.metadata!.prompt}\nNegative: ${selectedImage.metadata!.negative_prompt}`;
                    copyToClipboard(fullPrompt);
                  }}
                  className="w-full px-4 py-2 bg-gradient-to-r from-primary to-secondary hover:shadow-lg rounded-lg font-semibold text-white transition shadow-primary/50"
                >
                  📋 Copiar Parámetros
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
