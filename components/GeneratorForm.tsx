"use client";

import { useState, useEffect } from "react";

interface Model {
  id: string;
  name: string;
  description: string;
  path?: string;
}

interface GeneratorFormProps {
  onImageGenerated?: (imageUrl: string) => void;
}

export default function GeneratorForm({ onImageGenerated }: GeneratorFormProps) {
  const [prompt, setPrompt] = useState("");
  const [negativePrompt, setNegativePrompt] = useState("blurry, low quality, distorted, ugly");
  const [steps, setSteps] = useState(20);
  const [guidanceScale, setGuidanceScale] = useState(7.5);
  const [seed, setSeed] = useState(0);
  const [loading, setLoading] = useState(false);
  const [width, setWidth] = useState(512);
  const [height, setHeight] = useState(512);
  const [sampler, setSampler] = useState("DPM++ 2M");

  // Nuevos estados para modelos dinámicos
  const [model, setModel] = useState("stable-diffusion-v1-5");
  const [vae, setVae] = useState("default");
  const [lora, setLora] = useState("");
  const [loraScale, setLoraScale] = useState(0.75);
  const [upscaleFactor, setUpscaleFactor] = useState(0);
  const [negativeEmbedding, setNegativeEmbedding] = useState("");

  const [models, setModels] = useState<Model[]>([]);
  const [vaes, setVaes] = useState<Model[]>([]);
  const [loras, setLoras] = useState<Model[]>([]);
  const [embeddings, setEmbeddings] = useState<Model[]>([]);
  const [loadingModels, setLoadingModels] = useState(true);

  // Cargar lista de modelos al montar
  useEffect(() => {
    const fetchModels = async () => {
      try {
        const [modelsRes, vaesRes, lorasRes, embeddingsRes, lastMetadataRes] = await Promise.all([
          fetch("http://localhost:8000/api/models"),
          fetch("http://localhost:8000/api/vaes"),
          fetch("http://localhost:8000/api/loras"),
          fetch("http://localhost:8000/api/negative-embeddings"),
          fetch("http://localhost:8000/api/last-metadata"),
        ]);

        const modelsData = await modelsRes.json();
        const vaesData = await vaesRes.json();
        const lorasData = await lorasRes.json();
        const embeddingsData = await embeddingsRes.json();
        const lastMetadataData = await lastMetadataRes.json();

        setModels(modelsData.models || []);
        setVaes(vaesData.vaes || []);
        setLoras(lorasData.loras || []);
        setEmbeddings(embeddingsData.embeddings || []);

        // Cargar último prompt si existe
        if (lastMetadataData.success && lastMetadataData.metadata) {
          const meta = lastMetadataData.metadata;
          setPrompt(meta.prompt || "");
          setNegativePrompt(meta.negative_prompt || "");
          setSteps(meta.steps || 20);
          setGuidanceScale(meta.guidance_scale || 7.5);
          setSeed(meta.seed || 0);
          setWidth(meta.width || 512);
          setHeight(meta.height || 512);
          setModel(meta.model || "stable-diffusion-v1-5");
          setVae(meta.vae || "default");
          if (meta.lora) setLora(meta.lora);
          if (meta.lora_scale) setLoraScale(meta.lora_scale);
          if (meta.upscale_factor) setUpscaleFactor(meta.upscale_factor);
          if (meta.negative_embedding) setNegativeEmbedding(meta.negative_embedding);
        }
      } catch (error) {
        console.error("Error cargando modelos:", error);
      } finally {
        setLoadingModels(false);
      }
    };

    fetchModels();
  }, []);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt,
          negative_prompt: negativePrompt,
          steps,
          guidance_scale: guidanceScale,
          seed: seed === 0 ? Math.floor(Math.random() * 1000000) : seed,
          width,
          height,
          model,
          vae,
          lora_path: lora || undefined,
          lora_scale: loraScale,
          upscale_factor: upscaleFactor,
          negative_embedding: negativeEmbedding || undefined,
        }),
      });

      const data = await response.json();
      if (data.image_url) {
        onImageGenerated?.(data.image_url);
      } else if (data.error) {
        console.error("Error:", data.error);
        alert("Error: " + data.error);
      }
    } catch (error) {
      console.error("Error generando imagen:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-effect rounded-2xl p-6 space-y-6">
      <h2 className="text-2xl font-bold text-white">Configuración</h2>

      {/* Modelo */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          🤖 Modelo
        </label>
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          disabled={loadingModels}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none disabled:opacity-50"
        >
          {models.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name} - {m.description}
            </option>
          ))}
        </select>
      </div>

      {/* VAE */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          ✨ VAE (Calidad)
        </label>
        <select
          value={vae}
          onChange={(e) => setVae(e.target.value)}
          disabled={loadingModels}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none disabled:opacity-50"
        >
          {vaes.map((v) => (
            <option key={v.id} value={v.id}>
              {v.name}
            </option>
          ))}
        </select>
      </div>

      {/* LoRA */}
      {loras.length > 0 && (
        <div>
          <label className="block text-sm font-semibold text-gray-300 mb-2">
            🎨 LoRA (Opcional)
          </label>
          <select
            value={lora}
            onChange={(e) => setLora(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none"
          >
            <option value="">Ninguno</option>
            {loras.map((l) => (
              <option key={l.id} value={l.path || l.id}>
                {l.name}
              </option>
            ))}
          </select>
          {lora && (
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-2 mt-2">
                Escala LoRA: {loraScale.toFixed(2)}
              </label>
              <input
                type="range"
                min="0.1"
                max="1"
                step="0.05"
                value={loraScale}
                onChange={(e) => setLoraScale(Number(e.target.value))}
                className="w-full"
              />
            </div>
          )}
        </div>
      )}

      {/* Negative Embedding */}
      {embeddings.length > 0 && (
        <div>
          <label className="block text-sm font-semibold text-gray-300 mb-2">
            🚫 Negative Embedding
          </label>
          <select
            value={negativeEmbedding}
            onChange={(e) => setNegativeEmbedding(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none"
          >
            <option value="">Ninguno</option>
            {embeddings.map((e) => (
              <option key={e.id} value={e.path || e.id}>
                {e.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Prompt */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          📝 Prompt (Descripción)
        </label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe lo que quieres generar..."
          className="w-full h-32 bg-white/5 border border-white/10 rounded-lg p-4 text-white placeholder-gray-500 focus:border-primary focus:outline-none resize-none"
        />
      </div>

      {/* Negative Prompt */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          🚫 Negative Prompt
        </label>
        <input
          type="text"
          value={negativePrompt}
          onChange={(e) => setNegativePrompt(e.target.value)}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white placeholder-gray-500 focus:border-primary focus:outline-none"
        />
      </div>

      {/* Dimensiones */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-semibold text-gray-300 mb-2">
            Ancho: {width}px
          </label>
          <input
            type="range"
            min="256"
            max="1024"
            step="64"
            value={width}
            onChange={(e) => setWidth(Number(e.target.value))}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm font-semibold text-gray-300 mb-2">
            Alto: {height}px
          </label>
          <input
            type="range"
            min="256"
            max="1024"
            step="64"
            value={height}
            onChange={(e) => setHeight(Number(e.target.value))}
            className="w-full"
          />
        </div>
      </div>

      {/* Steps */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          ⚙️ Steps: {steps}
        </label>
        <input
          type="range"
          min="4"
          max="50"
          value={steps}
          onChange={(e) => setSteps(Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* Guidance Scale */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          🎯 Guidance Scale: {guidanceScale.toFixed(1)}
        </label>
        <input
          type="range"
          min="1"
          max="20"
          step="0.1"
          value={guidanceScale}
          onChange={(e) => setGuidanceScale(Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* Upscaler */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          🔍 Upscaler
        </label>
        <select
          value={upscaleFactor}
          onChange={(e) => setUpscaleFactor(Number(e.target.value))}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none"
        >
          <option value={0}>Ninguno</option>
          <option value={2}>x2 Upscale</option>
          <option value={4}>x4 Upscale</option>
        </select>
      </div>

      {/* Sampler */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          🎬 Sampler
        </label>
        <select
          value={sampler}
          onChange={(e) => setSampler(e.target.value)}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none"
        >
          <option>DPM++ 2M</option>
          <option>Euler</option>
          <option>Euler A</option>
          <option>Heun</option>
          <option>LMS</option>
          <option>LMS Karras</option>
        </select>
      </div>

      {/* Seed */}
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-2">
          🌱 Seed: {seed === 0 ? "Random" : seed}
        </label>
        <input
          type="number"
          value={seed}
          onChange={(e) => setSeed(Number(e.target.value))}
          className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none"
        />
        <p className="text-xs text-gray-400 mt-1">0 = Random, otro número = Reproducible</p>
      </div>

      {/* Botón Generar */}
      <button
        onClick={handleGenerate}
        disabled={loading || !prompt.trim()}
        className={`w-full py-4 rounded-lg font-bold text-white transition-all ${
          loading || !prompt.trim()
            ? "bg-gray-600 cursor-not-allowed opacity-50"
            : "bg-gradient-to-r from-primary to-secondary hover:shadow-lg shadow-primary/50"
        }`}
      >
        {loading ? (
          <div className="flex items-center justify-center gap-2">
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Generando...
          </div>
        ) : (
          "🎨 Generar Imagen"
        )}
      </button>
    </div>
  );
}
