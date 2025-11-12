"use client";

import { useState } from "react";

interface CivitaiModel {
  id: number;
  name: string;
  description: string;
  downloadCount: number;
  rating: number;
  versions: Array<{
    id: number;
    name: string;
  }>;
}

interface CivitaiDownloaderProps {
  onModelDownloaded?: () => void;
}

export default function CivitaiDownloader({ onModelDownloaded }: CivitaiDownloaderProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [modelType, setModelType] = useState("Checkpoint");
  const [models, setModels] = useState<CivitaiModel[]>([]);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [showPopular, setShowPopular] = useState(false);
  const [popular, setPopular] = useState<any>(null);

  const searchModels = async () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        `http://localhost:8000/api/civitai/search?query=${encodeURIComponent(
          searchQuery
        )}&model_type=${modelType}&limit=10`
      );
      const data = await response.json();
      setModels(data.models || []);

      if (data.models?.length === 0) {
        setMessage("❌ No se encontraron modelos");
      } else {
        setMessage(`✅ Encontrados ${data.models?.length || 0} modelos`);
      }
    } catch (error) {
      console.error("Error buscando modelos:", error);
      setMessage("❌ Error en la búsqueda");
    } finally {
      setLoading(false);
    }
  };

  const loadPopular = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/civitai/popular");
      const data = await response.json();
      setPopular(data.popular);
      setShowPopular(true);
      setModels([]);
    } catch (error) {
      console.error("Error cargando populares:", error);
      setMessage("❌ Error cargando modelos populares");
    } finally {
      setLoading(false);
    }
  };

  const downloadModel = async (modelId: number, versionId: number) => {
    setDownloading(modelId);
    setMessage("");

    try {
      const response = await fetch("http://localhost:8000/api/civitai/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model_id: modelId,
          version_id: versionId,
          model_type: modelType,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMessage(`✅ ${data.message}`);
        onModelDownloaded?.();
        // Limpiar búsqueda
        setTimeout(() => {
          setModels([]);
          setSearchQuery("");
          setShowPopular(false);
        }, 2000);
      } else {
        setMessage(`❌ Error: ${data.error}`);
      }
    } catch (error) {
      console.error("Error descargando:", error);
      setMessage("❌ Error en la descarga");
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div className="glass-effect rounded-2xl p-6 space-y-4">
      <h2 className="text-2xl font-bold text-white">📥 Descargar de Civitai</h2>

      {/* Tipo de modelo */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          📦 Tipo de Modelo
        </label>
        <select
          value={modelType}
          onChange={(e) => setModelType(e.target.value)}
          disabled={loading}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none disabled:opacity-50"
        >
          <option>Checkpoint</option>
          <option>LoRA</option>
          <option>Embeddings</option>
          <option>VAE</option>
        </select>
      </div>

      {/* Búsqueda */}
      <div className="flex gap-2">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Buscar en Civitai (ej: Proteus, anime, photorealistic)..."
          onKeyPress={(e) => e.key === "Enter" && searchModels()}
          disabled={loading}
          className="flex-1 bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:border-primary focus:outline-none disabled:opacity-50"
        />
        <button
          onClick={searchModels}
          disabled={loading || !searchQuery.trim()}
          className="px-6 py-2 bg-primary hover:bg-primary/80 rounded-lg font-semibold text-white disabled:opacity-50 disabled:cursor-not-allowed transition"
        >
          {loading ? "🔍..." : "🔍"}
        </button>
      </div>

      {/* Botón de populares */}
      <button
        onClick={loadPopular}
        disabled={loading}
        className="w-full px-4 py-2 bg-secondary/20 hover:bg-secondary/30 border border-secondary rounded-lg font-semibold text-white disabled:opacity-50 transition"
      >
        ⭐ Ver Modelos Populares
      </button>

      {/* Mensaje */}
      {message && (
        <div
          className={`p-3 rounded-lg text-white ${
            message.includes("✅") ? "bg-green-500/20 border border-green-500" : "bg-red-500/20 border border-red-500"
          }`}
        >
          {message}
        </div>
      )}

      {/* Resultados de búsqueda */}
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {models.map((model) => (
          <div
            key={model.id}
            className="bg-white/5 border border-white/10 rounded-lg p-4 hover:bg-white/10 transition"
          >
            <div className="flex justify-between items-start gap-4">
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-white text-lg">{model.name}</h3>
                <p className="text-gray-400 text-sm line-clamp-2">{model.description}</p>
                <div className="flex gap-4 mt-2 text-xs text-gray-500">
                  <span>⬇️ {(model.downloadCount / 1000).toFixed(0)}K descargas</span>
                  <span>⭐ {model.rating.toFixed(1)}</span>
                  <span>📦 {model.versions.length} versiones</span>
                </div>
              </div>
              <button
                onClick={() => {
                  const version = model.versions[0];
                  if (version) {
                    downloadModel(model.id, version.id);
                  }
                }}
                disabled={downloading === model.id || model.versions.length === 0}
                className="px-4 py-2 bg-gradient-to-r from-primary to-secondary hover:shadow-lg rounded-lg font-semibold text-white text-sm whitespace-nowrap disabled:opacity-50 disabled:cursor-not-allowed transition shadow-primary/50"
              >
                {downloading === model.id ? "⬇️..." : "⬇️ Descargar"}
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modelos populares */}
      {showPopular && popular && (
        <div className="space-y-4">
          {Object.entries(popular).map(([category, items]: any) => (
            <div key={category}>
              <h3 className="text-lg font-bold text-primary mb-2">📦 {category}</h3>
              <div className="space-y-2">
                {items.map((item: any, idx: number) => (
                  <div
                    key={idx}
                    className="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-white/10 transition"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <p className="font-semibold text-white">{item.name}</p>
                        <p className="text-sm text-gray-400">{item.description}</p>
                        {item.downloads && (
                          <p className="text-xs text-gray-500 mt-1">
                            ⬇️ {(item.downloads / 1000).toFixed(0)}K descargas
                          </p>
                        )}
                      </div>
                      {item.civitai_id && (
                        <a
                          href={`https://civitai.com/models/${item.civitai_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-3 py-1 bg-secondary/20 hover:bg-secondary/30 rounded text-sm text-white transition"
                        >
                          🔗 Ver
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Estado vacío */}
      {!showPopular && models.length === 0 && !message && (
        <div className="text-center py-8 text-gray-400">
          <p>🔍 Busca un modelo o haz clic en "Ver Populares"</p>
          <p className="text-sm mt-2">💡 Prueba: "Proteus", "Dreamshaper", "anime"</p>
        </div>
      )}
    </div>
  );
}
