"""bom.py - cruza la lista de la IA con el inventario, sin IA (dueño: P3)."""
import difflib
import db


def _buscar_parecido(cod: str, todos: list[str]):
    prefijos = [t for t in todos if t.startswith(cod) or cod.startswith(t)]
    parecido = (difflib.get_close_matches(cod, prefijos, n=1, cutoff=0)
                or difflib.get_close_matches(cod, todos, n=1, cutoff=0.8))
    return db.obtener(parecido[0]) if parecido else None


def cruzar_bom(lista_ia: list[dict]) -> list[dict]:
    """lista_ia = [{'codigo':'LM358','funcion':'comparador','cantidad':2}, ...]"""
    todos = [c["codigo"] for c in db.listar_componentes()]
    resultado = []
    for item in lista_ia:
        cod = db.normalizar(item.get("codigo", ""))
        comp = db.obtener(cod) or _buscar_parecido(cod, todos)   # 'LM358N' -> 'LM358'
        fila = {"pedido": item.get("codigo"), "para_que": item.get("funcion", ""),
                "cantidad": int(item.get("cantidad", 1) or 1)}
        if comp is None:
            fila |= {"en_almacen": "-", "stock": 0, "estado": "NO EXISTE"}
        else:
            fila |= {"en_almacen": comp["codigo"], "stock": comp["stock"],
                     "ubicacion": comp["ubicacion"],
                     "estado": "OK" if comp["stock"] >= fila["cantidad"] else "FALTA"}
        fila["alt_codigo"] = None
        if fila["estado"] != "OK":
            base = comp["codigo"] if comp else cod
            alts = [e for e in db.equivalentes(base) if (e["stock"] or 0) >= fila["cantidad"]]
            fila["alternativa"] = ("; ".join(f"{a['codigo']} ({a['condicion']})" for a in alts)
                                   or "sin equivalente en stock")
            fila["alt_codigo"] = alts[0]["codigo"] if alts else None
        resultado.append(fila)
    return resultado
