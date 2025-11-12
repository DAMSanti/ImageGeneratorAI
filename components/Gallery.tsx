"use client";

export default function Gallery() {
  return (
    <div className="glass-effect rounded-2xl p-6">
      <h2 className="text-2xl font-bold text-white mb-6">📸 Galería</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="bg-white/5 border border-white/10 rounded-lg aspect-square flex items-center justify-center text-gray-500 hover:bg-white/10 transition-all cursor-pointer"
          >
            <span className="text-center">
              <div className="text-3xl mb-2">🖼️</div>
              <p className="text-xs">Imagen {i + 1}</p>
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
