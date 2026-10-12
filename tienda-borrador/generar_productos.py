"""Genera productos.js a partir de la tabla de productos (xlsx).

Uso:
    python3 generar_productos.py tienda-productos-prueba.xlsx productos.js

La hoja Productos es la fuente única de los datos; este script solo la lee.
El botón y su enlace se calculan en la propia tabla (columnas Botón y Enlace del botón),
así que la regla vive en un solo lugar. Para que esos valores existan, el archivo debe
haberse guardado con las fórmulas calculadas (Excel lo hace solo al guardar).
"""
import json
import sys

from openpyxl import load_workbook


def texto(valor):
    return "" if valor is None else str(valor).strip()


def main(origen, destino):
    wb = load_workbook(origen, data_only=True)
    hoja, param = wb["Productos"], wb["Parámetros"]

    familias = []
    fila = 4
    while param.cell(fila, 1).value:
        familias.append({"letra": texto(param.cell(fila, 1).value), "nombre": texto(param.cell(fila, 2).value)})
        fila += 1
    nombre_de = {f["letra"]: f["nombre"] for f in familias}

    productos = []
    fila = 2
    while hoja.cell(fila, 1).value:
        codigo = texto(hoja.cell(fila, 1).value)
        precio = hoja.cell(fila, 7).value
        productos.append({
            "codigo": codigo,
            "familia": codigo[0],
            "familiaNombre": texto(hoja.cell(fila, 2).value) or nombre_de.get(codigo[0], ""),
            "nombre": texto(hoja.cell(fila, 3).value),
            "descripcion": texto(hoja.cell(fila, 4).value),
            "materiales": texto(hoja.cell(fila, 5).value),
            "tallas": texto(hoja.cell(fila, 6).value),
            "precio": precio if isinstance(precio, (int, float)) else None,
            "estado": texto(hoja.cell(fila, 8).value),
            "venta": texto(hoja.cell(fila, 9).value),
            "pago": texto(hoja.cell(fila, 10).value),
            "fotos": texto(hoja.cell(fila, 11).value),
            "boton": texto(hoja.cell(fila, 12).value),
            "enlace": texto(hoja.cell(fila, 13).value),
        })
        fila += 1

    datos = {"correo": texto(param["B17"].value), "familias": familias, "productos": productos}
    with open(destino, "w", encoding="utf-8") as f:
        f.write("/* Generado desde la tabla de productos con generar_productos.py. No editar a mano. */\n")
        f.write("window.TIENDA = " + json.dumps(datos, ensure_ascii=False, indent=1) + ";\n")
    print(f"{len(productos)} productos, {len(familias)} familias -> {destino}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
