"use client";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 glass-effect border-b border-white/20 shadow-soft">
      <div className="container mx-auto px-4 lg:px-8 py-4 flex justify-between items-center">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="text-3xl">🎨</div>
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              Image Generator
            </h1>
            <p className="text-xs text-gray-400">AI Local • RTX 1070</p>
          </div>
        </div>

        {/* Info */}
        <div className="hidden md:flex items-center gap-6 text-sm text-gray-300">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span>Backend: Conectado</span>
          </div>
          <div>GPU: RTX 1070 (8GB)</div>
        </div>
      </div>
    </header>
  );
}
