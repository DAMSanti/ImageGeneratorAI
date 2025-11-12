import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Image Generator AI",
  description: "Generador profesional de imágenes con IA usando Stable Diffusion local",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="min-h-screen">{children}</div>
      </body>
    </html>
  );
}
