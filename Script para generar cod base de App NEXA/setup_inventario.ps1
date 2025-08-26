Write-Host "🚀 Creando proyecto Inventario (Frontend + Backend IA + ML + Docs)..."

# =========================
# ROOT
# =========================
New-Item -ItemType Directory -Name "inventario-app" -Force
Set-Location inventario-app

# =========================
# FRONTEND
# =========================
Write-Host "📱 Creando frontend con Ionic + React + Tailwind + TS..."
ionic start frontend tabs --type=react --no-interactive
Set-Location frontend

# Dependencias
npm install axios @ionic/storage react-router-dom
npm install @capacitor/core @capacitor/cli
npm install @capacitor-community/barcode-scanner
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Estructura
New-Item -ItemType Directory -Path "src/assets" -Force
New-Item -ItemType Directory -Path "src/components" -Force
New-Item -ItemType Directory -Path "src/pages" -Force
New-Item -ItemType Directory -Path "src/services" -Force
New-Item -ItemType Directory -Path "src/context" -Force
New-Item -ItemType Directory -Path "src/hooks" -Force
New-Item -ItemType Directory -Path "src/utils" -Force

# Archivos en services
New-Item -ItemType File -Path "src/services/api.ts" -Force
New-Item -ItemType File -Path "src/services/supabase.ts" -Force

Set-Location ..

# =========================
# BACKEND
# =========================
Write-Host "🖥 Creando backend con FastAPI..."
New-Item -ItemType Directory -Name "backend" -Force
Set-Location backend

python -m venv venv

# Estructura
New-Item -ItemType Directory -Path "app/api" -Force
New-Item -ItemType Directory -Path "app/core" -Force
New-Item -ItemType Directory -Path "app/services" -Force

New-Item -ItemType File -Path "app/main.py" -Force
New-Item -ItemType File -Path "app/api/routes_ai.py" -Force
New-Item -ItemType File -Path "app/core/config.py" -Force
New-Item -ItemType File -Path "app/services/ai_service.py" -Force
New-Item -ItemType File -Path "app/services/supabase_service.py" -Force
New-Item -ItemType File -Path "requirements.txt" -Force

# Contenido principal de FastAPI (Python dentro de un here-string)
Set-Content -Path "app/main.py" -Value @"
from fastapi import FastAPI, UploadFile, File
from app.services.ai_service import predict_image

app = FastAPI(title="Inventario API")

@app.get("/ping")
def ping():
    return {"msg": "Servidor activo 🚀"}

@app.post("/clasificar")
async def clasificar(file: UploadFile = File(...)):
    result = predict_image(await file.read())
    return {"estado": result}
"@

Set-Location ..

# =========================
# MACHINE LEARNING
# =========================
Write-Host "🤖 Creando carpeta de IA..."
New-Item -ItemType Directory -Name "ml" -Force
Set-Location ml
New-Item -ItemType Directory -Name "data" -Force
New-Item -ItemType Directory -Name "notebooks" -Force
New-Item -ItemType Directory -Name "saved_models" -Force
New-Item -ItemType File -Name "train.py" -Force
New-Item -ItemType File -Name "model.py" -Force
New-Item -ItemType File -Name "export_model.py" -Force
Set-Location ..

# =========================
# DOCS
# =========================
Write-Host "📑 Creando carpeta de documentación..."
New-Item -ItemType Directory -Name "docs" -Force
New-Item -ItemType File -Path "docs/arquitectura.png" -Force
New-Item -ItemType File -Path "docs/estructura.md" -Force
New-Item -ItemType File -Path "docs/decisiones.md" -Force

# =========================
# README
# =========================
Set-Content -Path "README.md" -Value "# Inventario App (Ionic + React + FastAPI + Supabase)"

Write-Host "✅ Proyecto Inventario generado correctamente."