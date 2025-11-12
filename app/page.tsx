"use client";

import { useState } from "react";
import Header from "@/components/Header";
import GeneratorForm from "@/components/GeneratorForm";
import ImagePreview from "@/components/ImagePreview";
import Gallery from "@/components/Gallery";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"generator" | "gallery">("generator");
  const [lastGeneratedImage, setLastGeneratedImage] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header />

      <div className="container mx-auto px-4 py-12">
        {/* Navigation Tabs */}
        <div className="flex gap-4 mb-8 justify-center">
          <button
            onClick={() => setActiveTab("generator")}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === "generator"
                ? "bg-gradient-to-r from-primary to-secondary text-white shadow-lg"
                : "bg-white/10 text-gray-300 hover:bg-white/20"
            }`}
          >
            🎨 Generador
          </button>
          <button
            onClick={() => setActiveTab("gallery")}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === "gallery"
                ? "bg-gradient-to-r from-primary to-secondary text-white shadow-lg"
                : "bg-white/10 text-gray-300 hover:bg-white/20"
            }`}
          >
            📸 Galería
          </button>
        </div>

        {/* Generator Tab */}
        {activeTab === "generator" && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Form Section */}
            <div className="lg:col-span-1">
              <GeneratorForm onImageGenerated={setLastGeneratedImage} />
            </div>

            {/* Preview Section */}
            <div className="lg:col-span-2">
              <ImagePreview imageUrl={lastGeneratedImage} />
            </div>
          </div>
        )}

        {/* Gallery Tab */}
        {activeTab === "gallery" && <Gallery />}
      </div>
    </main>
  );
}
