import db

print("1. Iniciando base de datos...")
db.iniciar()

print("\n2. Probando listar_componentes():")
comps = db.listar_componentes()
print(f"Total de componentes: {len(comps)}")

print("\n3. Probando buscar('LM358'):")
print(db.buscar("LM358"))

print("\n4. Probando obtener('2N2222A'):")
print(db.obtener("2N2222A"))

print("\n5. Probando equivalentes('2N2222A'):")
print(db.equivalentes("2N2222A"))

