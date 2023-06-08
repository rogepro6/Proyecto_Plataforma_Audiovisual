lista =["roge", "paco", "luis"]

if "roger" not in lista:
    print("no esta")
else:
    print("Si esta")


diccionario = {"roge":["una", "dos", "tres"],
               "paco":["una", "dos"]}

if "roge" in diccionario.keys():
    print()
else:
    print("no")



    for user_p, peliculas in dict_peliculas_audiovisual.items():

        cantidad = 0
        if user_p[-7:] == "_vistas":
            nombres_usuario.append(user_p[:-7])
            cantidad += len(peliculas)
            if user_p in dict_series_audiovisual.keys():
                cantidad += len(dict_series_audiovisual[user_p])

            cantidades_vistas.append(cantidad)
