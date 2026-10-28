# Werkstatt Dashboard

Panel interno local de Werkstatt. Sin dependencias: solo necesita Node.js.

## Abrirlo

- Mac: doble clic en `iniciar.command` (si macOS lo bloquea, clic derecho > Abrir).
- Terminal: `node server.js` y abre http://localhost:4173/
- Otro puerto: `PORT=4174 node server.js`

Solo responde en esta computadora (127.0.0.1). Para cerrarlo: Control + C.

## Datos

- Los datos reales viven en `data/*.json` y no se suben a GitHub (`.gitignore`).
- La primera vez se copian de `semilla/`, que lleva datos de ejemplo.
- Botón "Respaldar datos": copia `data/` a `respaldos/<fecha>/`. "Exportar todo": descarga un JSON único.

## Cómo agregar una sección

1. Copia la carpeta de una sección existente (por ejemplo `web/`) con otro nombre en minúsculas.
2. Edita `seccion.json` (título, orden, descripción) y `seccion.js` (colecciones y campos).
3. Reinicia o recarga: el menú se arma solo con cada carpeta que tenga `seccion.json`.

Cada sección es una página independiente y guarda sus datos en sus propias colecciones. `shared/` solo trae el menú, los estilos y la tabla editable.

## Estructura

```
server.js        servidor y API (/api/c/<coleccion>)
shared/          menú, estilos, tabla editable, fuentes (OFL) y logos
semilla/         datos iniciales de ejemplo
<seccion>/       index.html, seccion.json, seccion.js
data/            datos reales (local, ignorado por git)
```

Fuentes: Archivo Black, Inter y Cormorant, licencia SIL OFL 1.1 (copias en `shared/fonts/licencias/`).
