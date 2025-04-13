#!/bin/bash

set -e

echo "📦 Instalando dependencias..."
sudo dnf groupinstall "Development Tools" -y
sudo dnf install -y gcc make zlib-devel bzip2 bzip2-devel \
    readline-devel sqlite-devel wget curl \
    openssl openssl-devel libffi-devel xz-devel tk-devel

echo "⬇️ Descargando Python 3.12.2..."
cd ~
wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz
tar xzf Python-3.12.2.tgz
cd Python-3.12.2

echo "⚙️ Configurando compilación con soporte OpenSSL..."
./configure --enable-optimizations --with-openssl=/usr

echo "🛠️ Compilando Python (esto puede tardar)..."
make -j$(nproc)

echo "📥 Instalando Python 3.12.2..."
sudo make altinstall

echo "✅ Verificando módulo SSL..."
/usr/local/bin/python3.12 -m ssl && echo "✔️ SSL disponible" || echo "❌ ERROR: No se pudo habilitar SSL"

echo "🚀 Instalando pip y FastAPI con Uvicorn..."
/usr/local/bin/python3.12 -m ensurepip --upgrade
/usr/local/bin/python3.12 -m pip install --upgrade pip
/usr/local/bin/python3.12 -m pip install fastapi "uvicorn[standard]"

echo "🎉 Listo. Ejecuta tu app con: /usr/local/bin/python3.12 -m uvicorn main:app --reload"
