"use client";

import Image from "next/image";

interface ImagePreviewProps {
  imageUrl: string | null;
}

export default function ImagePreview({ imageUrl }: ImagePreviewProps) {
  return (
    <div className="glass-effect rounded-2xl p-6 h-full flex flex-col items-center justify-center min-h-[600px]">
      {imageUrl ? (
        <div className="w-full space-y-4">
          <h3 className="text-lg font-bold text-white">Vista Previa</h3>
          <div className="relative w-full h-[500px] rounded-lg overflow-hidden bg-white/5 border border-white/10">
            <Image
              src={imageUrl}
              alt="Generated image"
              fill
              className="object-cover"
            />
          </div>
          <a
            href={imageUrl}
            download
            className="w-full py-2 bg-gradient-to-r from-primary to-secondary text-white rounded-lg font-semibold hover:shadow-lg text-center transition-all"
          >
            ⬇️ Descargar
          </a>
        </div>
      ) : (
        <div className="text-center space-y-4">
          <div className="text-6xl">🎨</div>
          <div>
            <p className="text-gray-400">Aquí aparecerá tu imagen</p>
            <p className="text-sm text-gray-500 mt-2">Configura los parámetros y haz clic en "Generar"</p>
          </div>
        </div>
      )}
    </div>
  );
}
