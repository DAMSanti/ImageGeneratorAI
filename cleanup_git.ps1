# Script para limpiar archivos grandes del repositorio de git (Windows PowerShell)

Write-Host "Limpiando archivos grandes del repositorio de git..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Archivos a excluir de git:" -ForegroundColor Yellow
Write-Host "  - models/ (modelos de IA)"
Write-Host "  - loras/ (LoRAs)"
Write-Host "  - vaes/ (VAEs)"
Write-Host "  - embeddings/ (Embeddings)"
Write-Host "  - controlnets/ (ControlNets)"
Write-Host "  - upscalers/ (Upscalers)"
Write-Host "  - generated_images/ (Imagenes generadas)"
Write-Host ""

Write-Host "Removiendo archivos del indice de git..." -ForegroundColor Cyan

$folders = @("models", "loras", "vaes", "embeddings", "controlnets", "upscalers", "generated_images")

foreach ($folder in $folders) {
    if (Test-Path $folder) {
        Write-Host "  Removiendo $folder..." -ForegroundColor Gray
        git rm -r --cached $folder 2>$null
    }
}

Write-Host ""
Write-Host "Limpieza completada!" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora haz:" -ForegroundColor Yellow
Write-Host "  git add .gitignore"
Write-Host "  git commit -m 'Actualizar .gitignore para excluir modelos e imagenes'"
Write-Host "  git push"
