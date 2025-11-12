"use client";

import { useState } from "react";

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
          sampler,
        }),
      });

      const data = await response.json();
      if (data.image_url) {
        onImageGenerated?.(data.image_url);
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
