#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_inventario.py (versión extendida)
---------------------------------
Script en Python que replica el comportamiento del script PowerShell y agrega:
- .gitignore en la raíz del proyecto
- Archivos tailwind.config.js y postcss.config.js preconfigurados
"""

import os
import sys
import subprocess
from pathlib import Path
from textwrap import dedent

EMOJI_OK = "✅"
EMOJI_ROCKET = "🚀"
EMOJI_PHONE = "📱"
EMOJI_PC = "🖥"
EMOJI_ROBOT = "🤖"
EMOJI_DOCS = "📑"

def run(cmd, cwd=None):
    """Ejecuta un comando en shell mostrando salida en tiempo real.
    Ajusta automáticamente los comandos para Windows (.cmd) si es necesario.
    """
    if os.name == "nt":
        # En Windows, los comandos npm/npx/ionic requieren .cmd
        if cmd[0] in ["npm", "npx", "ionic"]:
            cmd[0] = cmd[0] + ".cmd"
    print(f"\n$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

def mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def touch(path: Path, content: str = ""):
    path.parent.mkdir(parents=True, exist_ok=True)
    if content is None:
        content = ""
    path.write_text(content, encoding="utf-8")

def main():
    print(f"{EMOJI_ROCKET} Creando proyecto Inventario (Frontend + Backend IA + ML + Docs)...")

    root = Path("inventario-app").resolve()
    mkdir(root)

    # =========================
    # FRONTEND
    # =========================
    print(f"{EMOJI_PHONE} Creando frontend con Ionic + React + Tailwind + TS...")
    frontend_dir = root / "frontend"
    if not frontend_dir.exists() or not any(frontend_dir.iterdir()):
        # run(["ionic", "start", "frontend", "tabs", "--type=react", "--no-interactive"], cwd=root)
        run([r"C:\Users\campu\AppData\Roaming\npm\npx.cmd", "ionic", "start", "frontend", "tabs", "--type=react", "--no-interactive"], cwd=root)
    else:
        print("ℹ️  Se detectó carpeta 'frontend' existente. Omitiendo 'ionic start'.")

    # Dependencias
    run(["npm", "install", "axios", "@ionic/storage", "react-router-dom", "--legacy-peer-deps"], cwd=frontend_dir)
    run(["npm", "install", "@capacitor/core", "@capacitor/cli", "--legacy-peer-deps"], cwd=frontend_dir)
    run(["npm", "install", "@capacitor-community/barcode-scanner@4.0.1", "--legacy-peer-deps"], cwd=frontend_dir)
    run(["npm", "install", "-D", "tailwindcss", "postcss", "autoprefixer", "--legacy-peer-deps"], cwd=frontend_dir)

    # Inicializar Tailwind de forma portable
    try:
        run(["npx", "--package", "tailwindcss", "tailwindcss", "init", "-p"], cwd=frontend_dir)
    except subprocess.CalledProcessError:
        print("⚠️ No se pudo inicializar Tailwind automáticamente, usando los archivos generados por el script.")



    # Configuración inicial para Tailwind y PostCSS
    tailwind_config = dedent('''
    /** @type {import('tailwindcss').Config} */
    module.exports = {
        content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}"
        ],
        theme: {
        extend: {},
        },
        plugins: [],
    }
    ''').strip() + "\n"

    postcss_config = dedent('''
    module.exports = {
        plugins: {
            tailwindcss: {},
            autoprefixer: {},
        },
    }
    ''').strip() + "\n"

    touch(frontend_dir / "tailwind.config.js", tailwind_config)
    touch(frontend_dir / "postcss.config.js", postcss_config)

    # Estructura
    for sub in ["src/assets", "src/components", "src/pages", "src/services",
                "src/context", "src/hooks", "src/utils"]:
        mkdir(frontend_dir / sub)

    # Archivos en services
    touch(frontend_dir / "src/services/api.ts")
    touch(frontend_dir / "src/services/supabase.ts")

    # =========================
    # BACKEND
    # =========================
    print(f"{EMOJI_PC} Creando backend con FastAPI...")
    backend_dir = root / "backend"
    mkdir(backend_dir)

    run([sys.executable, "-m", "venv", "venv"], cwd=backend_dir)

    app_dir = backend_dir / "app"
    mkdir(app_dir / "api")
    mkdir(app_dir / "core")
    mkdir(app_dir / "services")

    # Archivos backend
    main_py = dedent('''
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
    ''').strip() + "\n"

    ai_service_py = dedent('''
        # app/services/ai_service.py
        from typing import Any

        def predict_image(data: bytes) -> Any:
            # TODO: lógica real de ML/IA
            return "ok"
    ''').strip() + "\n"

    config_py = dedent('''
        # app/core/config.py
        import os

        class Settings:
            APP_NAME: str = "Inventario API"
        settings = Settings()
    ''').strip() + "\n"

    supabase_service_py = "# app/services/supabase_service.py\n"
    routes_ai_py = "# app/api/routes_ai.py\n"
    requirements_txt = "fastapi\nuvicorn[standard]\n"

    touch(app_dir / "main.py", main_py)
    touch(app_dir / "api" / "routes_ai.py", routes_ai_py)
    touch(app_dir / "core" / "config.py", config_py)
    touch(app_dir / "services" / "ai_service.py", ai_service_py)
    touch(app_dir / "services" / "supabase_service.py", supabase_service_py)
    touch(backend_dir / "requirements.txt", requirements_txt)

    # =========================
    # MACHINE LEARNING
    # =========================
    print(f"{EMOJI_ROBOT} Creando carpeta de IA...")
    ml_dir = root / "ml"
    mkdir(ml_dir / "data")
    mkdir(ml_dir / "notebooks")
    mkdir(ml_dir / "saved_models")
    touch(ml_dir / "train.py")
    touch(ml_dir / "model.py")
    touch(ml_dir / "export_model.py")

    # =========================
    # DOCS
    # =========================
    print(f"{EMOJI_DOCS} Creando carpeta de documentación...")
    docs_dir = root / "docs"
    mkdir(docs_dir)
    touch(docs_dir / "arquitectura.png", "")
    touch(docs_dir / "estructura.md")
    touch(docs_dir / "decisiones.md")

    # =========================
    # README & .gitignore
    # =========================
    touch(root / "README.md", "# Inventario App (Ionic + React + FastAPI + Supabase)\n")

    gitignore = dedent('''
    # Node
    node_modules/
    npm-debug.log
    yarn-error.log

    # Python
    __pycache__/
    *.py[cod]
    venv/

    # Env
    .env
    .DS_Store
    ''').strip() + "\n"

    touch(root / ".gitignore", gitignore)

    print(f"{EMOJI_OK} Proyecto Inventario generado correctamente en: {root}")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("❌ Error ejecutando un comando.")
        print(f"Comando: {e.cmd}")
        print(f"Código de salida: {e.returncode}")
        sys.exit(e.returncode)
    except Exception as ex:
        print(f"❌ Error: {ex}")
        sys.exit(1)