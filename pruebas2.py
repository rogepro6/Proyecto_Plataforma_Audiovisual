diccionario = {"roge_fav": [1, 2, 3],
               "luis_fav": [3, 4, 5],
               "paco_fav": [4, 5, 6, 7]}
nombres = []

for i, x in diccionario.items():
    nombres.append(i[:-4])
    print(len(x))

print(nombres)

palabra = "rogelio_favoritos"

nombre = palabra[:-10]
print(nombre)
