#!/usr/bin/env python3
"""
Script para preparar os arquivos para deploy público
"""

import os
import shutil
import zipfile
from pathlib import Path

def criar_pasta_deploy():
    """Cria pasta com apenas os arquivos necessários para deploy"""
    
    # Pasta de destino
    deploy_dir = Path("deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Arquivos principais
    arquivos_principais = [
        "index.html",
        "firebase-config.js", 
        "firebase.json"
    ]
    
    # Pastas
    pastas = [
        "css",
        "js", 
        "static"
    ]
    
    print("📦 Preparando arquivos para deploy...")
    
    # Copiar arquivos principais
    for arquivo in arquivos_principais:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, deploy_dir)
            print(f"✅ Copiado: {arquivo}")
    
    # Copiar pastas
    for pasta in pastas:
        if os.path.exists(pasta):
            shutil.copytree(pasta, deploy_dir / pasta)
            print(f"✅ Copiada pasta: {pasta}")
    
    # Criar ZIP
    zip_path = "sistema-alubras-deploy.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Arquivos preparados!")
    print(f"📁 Pasta: {deploy_dir}")
    print(f"📦 ZIP: {zip_path}")
    print(f"\n🚀 Agora você pode:")
    print(f"   1. Ir para https://app.netlify.com/drop")
    print(f"   2. Arrastar a pasta '{deploy_dir}' ou o arquivo '{zip_path}'")
    print(f"   3. Aguardar deploy e receber seu link público!")

if __name__ == "__main__":
    criar_pasta_deploy()
