#!/bin/bash
# Script para limpiar archivos grandes del repositorio de git

echo "🧹 Limpiando archivos grandes del repositorio de git..."
echo ""

# Listar archivos que se van a excluir
echo "📋 Archivos a excluir de git:"
echo "  ✗ models/ (modelos de IA)"
echo "  ✗ loras/ (LoRAs)"
echo "  ✗ vaes/ (VAEs)"
echo "  ✗ embeddings/ (Embeddings)"
echo "  ✗ controlnets/ (ControlNets)"
echo "  ✗ upscalers/ (Upscalers)"
echo "  ✗ generated_images/ (Imágenes generadas)"
echo ""

# Eliminar del índice de git
echo "🔄 Removiendo archivos del índice de git..."
git rm -r --cached models/ 2>/dev/null
git rm -r --cached loras/ 2>/dev/null
git rm -r --cached vaes/ 2>/dev/null
git rm -r --cached embeddings/ 2>/dev/null
git rm -r --cached controlnets/ 2>/dev/null
git rm -r --cached upscalers/ 2>/dev/null
git rm -r --cached generated_images/ 2>/dev/null

echo "✅ Done!"
echo ""
echo "📝 Ahora haz:"
echo "  git add .gitignore"
echo "  git commit -m 'Actualizar .gitignore para excluir modelos e imágenes'"
echo "  git push"
