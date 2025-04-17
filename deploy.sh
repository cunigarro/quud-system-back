#!/bin/bash

LOG_FILE=log.txt

echo "🐍 Activando entorno virtual"
python3.12 -m venv venv
source venv/bin/activate

echo "⬆️ Actualizando código"
git pull

echo "📦 Instalando dependencias"
pip install uvicorn
pip install -r requirements.txt


echo "🛑 Deteniendo procesos previos de Uvicorn"
pkill -f uvicorn || echo "No se encontró proceso Uvicorn"
kill $(lsof -t -i:8000)

echo "🚀 Ejecutando la aplicación"
nohup uvicorn main:app --host 0.0.0.0 --port=8000 > $LOG_FILE 2>&1 &

echo "✅ Despliegue completo. Revisa logs con: tail -f $LOG_FILE"