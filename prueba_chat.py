import db, ia_chat

db.iniciar()
mi_lista = []
chat = ia_chat.nuevo_chat(mi_lista)
print("1)", ia_chat.preguntar(chat, "¿Hay LM358?"))
print("2)", ia_chat.preguntar(chat, "¿Hay 2N2222? necesito 2, agrégalo a mi lista"))
print("3)", ia_chat.preguntar(chat, "Busco algo para medir distancia"))
print("4)", ia_chat.preguntar(chat, "¿Hay Raspberry Pi?"))
print("MI LISTA:", mi_lista)
