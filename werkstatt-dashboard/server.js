'use strict';
/*
  Werkstatt Dashboard: servidor local, sin dependencias.
  Sirve las secciones como páginas independientes y guarda los datos en data/*.json.
  Solo escucha en esta computadora (127.0.0.1).
*/
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const RAIZ = __dirname;
const DATOS = path.join(RAIZ, 'data');
const SEMILLA = path.join(RAIZ, 'semilla');
const RESPALDOS = path.join(RAIZ, 'respaldos');
const PUERTO = Number(process.env.PORT) || 4173;
const HOST = '127.0.0.1';
const VERSION = '1.0.0';

const TIPOS = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8'
};
const CARPETAS_PRIVADAS = new Set(['data', 'semilla', 'respaldos', 'node_modules']);
const ARCHIVOS_PRIVADOS = new Set(['server.js', 'package.json', 'readme.md', 'iniciar.command']);
const NOMBRE_COLECCION = /^[a-z0-9-]{1,40}$/;
const NOMBRE_CAMPO = /^[A-Za-z0-9_]{1,40}$/;
const CAMPOS_PROHIBIDOS = new Set(['__proto__', 'constructor', 'prototype']);
const CAMPOS_DEL_SISTEMA = new Set(['id', 'creado', 'actualizado']);
const LIMITE_CUERPO = 1024 * 1024;

/* ---------- datos ---------- */

function preparar() {
  fs.mkdirSync(DATOS, { recursive: true });
  if (!fs.existsSync(SEMILLA)) return;
  for (const f of fs.readdirSync(SEMILLA)) {
    if (f.endsWith('.json') && !fs.existsSync(path.join(DATOS, f))) {
      fs.copyFileSync(path.join(SEMILLA, f), path.join(DATOS, f));
    }
  }
}

function archivo(c) { return path.join(DATOS, c + '.json'); }

function leer(c) {
  let texto;
  try { texto = fs.readFileSync(archivo(c), 'utf8'); }
  catch (e) { if (e.code === 'ENOENT') return []; throw e; }
  let lista;
  try { lista = JSON.parse(texto); }
  catch (e) { throw new Error('El archivo data/' + c + '.json no es un JSON válido. Revísalo o restaura un respaldo.'); }
  return Array.isArray(lista) ? lista : [];
}

function escribir(c, lista) {
  const destino = archivo(c);
  const temporal = destino + '.tmp';
  fs.writeFileSync(temporal, JSON.stringify(lista, null, 2));
  fs.renameSync(temporal, destino);
}

function nuevoId() { return Date.now().toString(36) + crypto.randomBytes(3).toString('hex'); }

function limpiar(cuerpo) {
  if (!cuerpo || typeof cuerpo !== 'object' || Array.isArray(cuerpo)) throw error(400, 'El cuerpo debe ser un objeto.');
  const salida = {};
  for (const k of Object.keys(cuerpo)) {
    if (!NOMBRE_CAMPO.test(k) || CAMPOS_PROHIBIDOS.has(k)) throw error(400, 'Campo no permitido: ' + k);
    if (CAMPOS_DEL_SISTEMA.has(k)) continue;
    const v = cuerpo[k];
    if (v === null || typeof v === 'number' || typeof v === 'boolean') { salida[k] = v; continue; }
    if (typeof v === 'string') {
      if (v.length > 5000) throw error(400, 'Texto demasiado largo en ' + k);
      salida[k] = v;
      continue;
    }
    throw error(400, 'Valor no permitido en ' + k);
  }
  return salida;
}

function error(estado, mensaje) { const e = new Error(mensaje); e.estado = estado; return e; }

function secciones() {
  const lista = [];
  for (const d of fs.readdirSync(RAIZ, { withFileTypes: true })) {
    if (!d.isDirectory() || d.name.startsWith('.') || d.name === 'shared' || CARPETAS_PRIVADAS.has(d.name)) continue;
    const manifiesto = path.join(RAIZ, d.name, 'seccion.json');
    if (!fs.existsSync(manifiesto)) continue;
    try {
      const m = JSON.parse(fs.readFileSync(manifiesto, 'utf8'));
      lista.push({ id: d.name, titulo: String(m.titulo || d.name), descripcion: String(m.descripcion || ''), orden: Number(m.orden) || 99 });
    } catch (e) { /* manifiesto dañado: la sección se omite */ }
  }
  return lista.sort((a, b) => a.orden - b.orden || a.id.localeCompare(b.id));
}

function sello() {
  const f = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return f.getFullYear() + '-' + p(f.getMonth() + 1) + '-' + p(f.getDate()) + '_' + p(f.getHours()) + p(f.getMinutes()) + p(f.getSeconds());
}

function respaldar() {
  const carpeta = path.join(RESPALDOS, sello());
  fs.mkdirSync(carpeta, { recursive: true });
  let n = 0;
  for (const f of fs.readdirSync(DATOS)) {
    if (f.endsWith('.json')) { fs.copyFileSync(path.join(DATOS, f), path.join(carpeta, f)); n++; }
  }
  return { carpeta: 'respaldos/' + path.basename(carpeta), archivos: n };
}

function todo() {
  const colecciones = {};
  for (const f of fs.readdirSync(DATOS)) {
    if (f.endsWith('.json')) colecciones[f.slice(0, -5)] = leer(f.slice(0, -5));
  }
  return { version: VERSION, fecha: new Date().toISOString(), colecciones };
}

/* ---------- http ---------- */

function responder(res, estado, cuerpo, cabeceras) {
  const base = {
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'Content-Security-Policy': "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
  };
  res.writeHead(estado, Object.assign(base, cabeceras || {}));
  res.end(cuerpo);
}

function json(res, estado, objeto, extra) {
  responder(res, estado, estado === 204 ? undefined : JSON.stringify(objeto),
    Object.assign({ 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }, extra || {}));
}

function leerCuerpo(req) {
  return new Promise((resolver, rechazar) => {
    const trozos = [];
    let total = 0;
    req.on('data', (t) => {
      total += t.length;
      if (total > LIMITE_CUERPO) { rechazar(error(413, 'Cuerpo demasiado grande.')); req.destroy(); return; }
      trozos.push(t);
    });
    req.on('end', () => {
      if (!total) { resolver(null); return; }
      try { resolver(JSON.parse(Buffer.concat(trozos).toString('utf8'))); }
      catch (e) { rechazar(error(400, 'JSON no válido.')); }
    });
    req.on('error', rechazar);
  });
}

async function api(req, res, partes) {
  const metodo = req.method;
  if (metodo !== 'GET' && metodo !== 'HEAD') {
    if (req.headers['x-werkstatt'] !== '1') throw error(403, 'Falta la cabecera X-Werkstatt.');
  }
  const [recurso, coleccion, id] = partes;

  if (recurso === 'secciones' && metodo === 'GET') return json(res, 200, secciones());
  if (recurso === 'estado' && metodo === 'GET') return json(res, 200, { version: VERSION, puerto: PUERTO, datos: 'data/' });
  if (recurso === 'exportar' && metodo === 'GET') {
    return json(res, 200, todo(), { 'Content-Disposition': 'attachment; filename="werkstatt-dashboard-' + sello() + '.json"' });
  }
  if (recurso === 'respaldo' && metodo === 'POST') return json(res, 201, respaldar());

  if (recurso === 'c') {
    if (!coleccion || !NOMBRE_COLECCION.test(coleccion)) throw error(400, 'Nombre de colección no válido.');
    if (metodo === 'GET' && !id) return json(res, 200, leer(coleccion));
    if (metodo === 'POST' && !id) {
      const registro = Object.assign({ id: nuevoId() }, limpiar(await leerCuerpo(req)), { creado: new Date().toISOString() });
      const lista = leer(coleccion);
      lista.push(registro);
      escribir(coleccion, lista);
      return json(res, 201, registro);
    }
    if (id) {
      const lista = leer(coleccion);
      const i = lista.findIndex((x) => x.id === id);
      if (i < 0) throw error(404, 'No existe ese registro.');
      if (metodo === 'GET') return json(res, 200, lista[i]);
      if (metodo === 'PUT') {
        lista[i] = Object.assign({}, lista[i], limpiar(await leerCuerpo(req)), { id, actualizado: new Date().toISOString() });
        escribir(coleccion, lista);
        return json(res, 200, lista[i]);
      }
      if (metodo === 'DELETE') {
        lista.splice(i, 1);
        escribir(coleccion, lista);
        return json(res, 204);
      }
    }
  }
  throw error(404, 'Ruta de API desconocida.');
}

function estatico(req, res, ruta) {
  if (req.method !== 'GET' && req.method !== 'HEAD') return responder(res, 405, 'Método no permitido', { 'Allow': 'GET, HEAD' });
  let relativa;
  try { relativa = decodeURIComponent(ruta); } catch (e) { return responder(res, 400, 'Ruta no válida'); }
  if (relativa.includes('\0')) return responder(res, 400, 'Ruta no válida');
  if (relativa === '/') return responder(res, 302, '', { Location: '/inicio/' });
  if (relativa.endsWith('/')) relativa += 'index.html';
  const segmentos = relativa.split('/').filter(Boolean);
  if (segmentos.some((s) => s.startsWith('.') || s === '..')) return responder(res, 404, 'No encontrado');
  if (CARPETAS_PRIVADAS.has(segmentos[0]) || (segmentos.length === 1 && ARCHIVOS_PRIVADOS.has(segmentos[0].toLowerCase()))) {
    return responder(res, 404, 'No encontrado');
  }
  const completa = path.join(RAIZ, ...segmentos);
  if (!completa.startsWith(RAIZ + path.sep)) return responder(res, 404, 'No encontrado');
  fs.stat(completa, (err, info) => {
    if (err || !info.isFile()) {
      // /seccion sin barra final: redirige a /seccion/
      if (!err && info.isDirectory()) return responder(res, 302, '', { Location: ruta.replace(/\/?$/, '/') });
      return responder(res, 404, 'No encontrado');
    }
    const tipo = TIPOS[path.extname(completa).toLowerCase()] || 'application/octet-stream';
    res.writeHead(200, {
      'Content-Type': tipo,
      'Content-Length': info.size,
      'Cache-Control': 'no-cache',
      'X-Content-Type-Options': 'nosniff',
      'Content-Security-Policy': "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    });
    if (req.method === 'HEAD') return res.end();
    fs.createReadStream(completa).pipe(res);
  });
}

const servidor = http.createServer(async (req, res) => {
  try {
    // Defensa contra DNS rebinding: solo se atiende por localhost o 127.0.0.1
    const anfitrion = String(req.headers.host || '').toLowerCase();
    if (anfitrion !== 'localhost:' + PUERTO && anfitrion !== '127.0.0.1:' + PUERTO) {
      return responder(res, 403, 'Anfitrión no permitido');
    }
    const url = new URL(req.url, 'http://localhost');
    if (url.pathname.startsWith('/api/')) {
      const partes = url.pathname.slice(5).split('/').filter(Boolean);
      return await api(req, res, partes);
    }
    return estatico(req, res, url.pathname);
  } catch (e) {
    const estado = e.estado || 500;
    if (estado === 500) console.error(e);
    if (!res.headersSent) json(res, estado, { error: e.message || 'Error interno.' });
  }
});

servidor.on('error', (e) => {
  if (e.code === 'EADDRINUSE') console.error('\nEl puerto ' + PUERTO + ' ya está en uso. Si el dashboard ya está abierto, usa esa ventana; si no, ejecuta: PORT=4174 node server.js\n');
  else console.error(e);
  process.exit(1);
});

preparar();
servidor.listen(PUERTO, HOST, () => {
  console.log('\nWerkstatt Dashboard v' + VERSION);
  console.log('Abierto en http://localhost:' + PUERTO + '/  (solo en esta computadora)');
  console.log('Datos en: ' + DATOS);
  console.log('Para cerrarlo: Control + C\n');
});
