#!/bin/bash
# Doble clic para abrir el Werkstatt Dashboard en esta Mac.
cd "$(dirname "$0")" || exit 1

if ! command -v node >/dev/null 2>&1; then
  echo "Falta Node.js. Instálalo desde https://nodejs.org (elige una versión compatible con tu macOS) y vuelve a abrir este archivo."
  read -r -p "Presiona Enter para cerrar..." _
  exit 1
fi

PORT="${PORT:-4173}"
( sleep 1; open "http://localhost:${PORT}/" ) &
PORT="$PORT" node server.js
