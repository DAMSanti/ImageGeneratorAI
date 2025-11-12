"use client";

import { useState } from "react";
import Header from "@/components/Header";
import GeneratorForm from "@/components/GeneratorForm";
import ImagePreview from "@/components/ImagePreview";
import Gallery from "@/components/Gallery";
import CivitaiDownloader from "@/components/CivitaiDownloader";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"generator" | "gallery" | "download">("generator");
  const [lastGeneratedImage, setLastGeneratedImage] = useState<string | null>(null);
  const [refreshGallery, setRefreshGallery] = useState(false);

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header />

      <div className="container mx-auto px-4 py-12">
        {/* Navigation Tabs */}
        <div className="flex gap-4 mb-8 justify-center flex-wrap">
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
          <button
            onClick={() => setActiveTab("download")}
            className={`px-6 py-3 rounded-lg font-semibold transition-all ${
              activeTab === "download"
                ? "bg-gradient-to-r from-primary to-secondary text-white shadow-lg"
                : "bg-white/10 text-gray-300 hover:bg-white/20"
            }`}
          >
            📥 Descargar Modelos
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

        {/* Download Tab */}
        {activeTab === "download" && (
          <div className="max-w-2xl mx-auto">
            <CivitaiDownloader
              onModelDownloaded={() => {
                setRefreshGallery(!refreshGallery);
              }}
            />
          </div>
        )}
      </div>
    </main>
  );
}
