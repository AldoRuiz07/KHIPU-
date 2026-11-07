"""lista.py - 'Mi lista': lo que el chat o Mi proyecto recomiendan (dueño: P3).
La lista vive en st.session_state.mi_lista y la usa la pestaña Laboratorio."""
import db


def agregar(lista: list, codigo: str, cantidad: int = 1, origen: str = "") -> dict:
    """Agrega o suma un componente. Devuelve lo que quedó, o un error si no existe."""
    comp = db.obtener(codigo)
    if comp is None:
        return {"ok": False, "error": f"{codigo} no existe en el almacén"}
    for item in lista:
        if item["codigo"] == comp["codigo"]:
            item["cantidad"] += int(cantidad)
            return {"ok": True, "codigo": comp["codigo"], "cantidad": item["cantidad"]}
    lista.append({"codigo": comp["codigo"], "nombre": comp["nombre"],
                  "cantidad": int(cantidad), "origen": origen})
    return {"ok": True, "codigo": comp["codigo"], "cantidad": int(cantidad)}


def quitar(lista: list, codigo: str):
    lista[:] = [i for i in lista if i["codigo"] != codigo]
