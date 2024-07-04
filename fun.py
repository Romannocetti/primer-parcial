import random
import json

#recibimos el nombre del archivo
def cargar_archivo():
    """
    Solicita al usuario ingresar el nombre del archivo 'ciclistas.csv' para cargarlo.
    Muestra un mensaje de confirmación una vez que se carga correctamente.
    """
    while True:
        NOMBRE = input("Ingrese el archivo que desea cargar: ")
        if NOMBRE == "ciclistas.csv":
            break
        else:
            print("El archivo no existe")
    print("--------------------------------------------------------------------------")
    print(f"Se ha cargado el archivo: {NOMBRE}")


def get_path_actual(nombre_archivo):
    """
    Obtiene la ruta completa del archivo especificado en función del directorio actual del script.

    Args:
    - nombre_archivo (str): Nombre del archivo del cual se desea obtener la ruta.

    Returns:
    - str: Ruta completa del archivo.
    """
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

with open(get_path_actual("ciclistas.csv"), "r", encoding="utf-") as archivo:
    lista = []	
    encabezado = archivo.readline().strip("\n").split(",")

    print(encabezado)

    for linea in archivo.readlines():
        ciclista = {}
        linea = linea.strip("\n").split(",")

        id_bike, nombre, tipo, tiempo = linea
        ciclista["id_bike"] = id_bike
        ciclista["nombre"] = nombre
        ciclista["tipo"] = tipo
        ciclista["tiempo"] = int(tiempo)
        lista.append(ciclista)



def asignar_tiempos(ciclista):
    """
    Asigna tiempos aleatorios a cada ciclista en la lista proporcionada.

    Args:
    - lista (list): Lista de diccionarios donde cada diccionario representa a un ciclista.
    """
    import random
    for ciclista in lista:
        ciclista["tiempo"] = random.randint(50, 120)


def reduce_list(funcion, lista):
    """
    Reduce la lista aplicando la función especificada.

    Args:
    - funcion (function): Función a aplicar en la reducción.
    - lista (list): Lista sobre la cual se aplica la reducción.

    Returns:
    - El resultado de aplicar la función sobre la lista.
    """
    ant = lista[0]
    for el in lista[1:]:
        ant = funcion(ant, el)
    return ant


def ganador_o_empate(lista):
    """
    Determina al ganador o muestra empate entre los ciclistas con el menor tiempo registrado.

    Args:
    - lista (list): Lista de diccionarios, cada uno representa a un ciclista con sus datos.
    """
    resultado = reduce_list(lambda ciclista, ciclista2: ciclista if float(ciclista["tiempo"]) > float(ciclista2["tiempo"]) else ciclista2, lista)

    # Filtrar a todos los ciclistas que tienen el mismo menor tiempo
    ganadores = [ciclista for ciclista in lista if float(ciclista["tiempo"]) == float(resultado["tiempo"])]

    # Mostrar el resultado según si hay empate o no
    if len(ganadores) == 1:
        print(f'El ganador es {ganadores[0]["nombre"]} con un tiempo de {ganadores[0]["tiempo"]} segundos.')
    else:
        print('Hubo un empate entre los siguientes ciclistas:')
        for ganador in ganadores:
            print(f'{ganador["nombre"]} con un tiempo de {ganador["tiempo"]} segundos.')


def filtrar_por_tipo(tipo):
    """
    Filtra y guarda en un archivo separado por tipo de bicicleta.

    Args:
    - tipo (str): Tipo de bicicleta a filtrar y guardar.
    """
    with open(get_path_actual(f"{tipo}.csv"), "w", encoding="utf-8") as archivo:
        encabezado = ",".join(list(lista[0].keys())) + "\n"
        archivo.write(encabezado)
        
        for persona in lista:
            if persona['tipo'] == tipo:
                values = [str(value) if isinstance(value, (int, float)) else value for value in persona.values()]
                linea = ",".join(values) + "\n"
                archivo.write(linea)


def calcular_promedio_por_tipo(lista):
    """
    Calcula y muestra el promedio de tiempos por cada tipo de bicicleta.

    Args:
    - lista (list): Lista de diccionarios representando a los ciclistas.
    """
    if not lista:
        print("No hay datos de ciclistas cargados.")
        return
    
    acumuladores = {}
    conteos = {}
    
    def actualizar_acumuladores(acumuladores, conteos, ciclista):
        tipo = ciclista["tipo"]
        tiempo = float(ciclista["tiempo"])
        
        if tipo not in acumuladores:
            acumuladores[tipo] = tiempo
            conteos[tipo] = 1
        else:
            acumuladores[tipo] += tiempo
            conteos[tipo] += 1
    
    reduce_list(lambda _, ciclista: actualizar_acumuladores(acumuladores, conteos, ciclista), lista)
    
    print("Promedio de tiempos por tipo de bicicleta:")
    for tipo, acumulado in acumuladores.items():
        promedio = acumulado / conteos[tipo]
        print(f'Tipo: {tipo}, Promedio de Tiempo: {promedio:.2f} segundos')


def mostrar_posiciones(lista):
    """
    Muestra las posiciones de los ciclistas ordenadas por tipo y tiempo ascendente.

    Args:
    - lista (list): Lista de diccionarios representando a los ciclistas.
    """
    # Agrupar bicicletas por tipo
    bicicletas_por_tipo = {}
    for ciclista in lista:
        tipo = ciclista["tipo"]
        if tipo not in bicicletas_por_tipo:
            bicicletas_por_tipo[tipo] = []
        bicicletas_por_tipo[tipo].append(ciclista)

    # Ordenar cada grupo por tiempo ascendente
    for tipo in bicicletas_por_tipo:
        bicicletas_por_tipo[tipo].sort(key=lambda x: x["tiempo"])

    # Mostrar por pantalla el resultado ordenado
    print("Posiciones ordenadas por tipo y tiempo ascendente:")
    for tipo in sorted(bicicletas_por_tipo.keys()):  # Ordenar tipos alfabéticamente
        print(f"Tipo: {tipo}")
        for index, ciclista in enumerate(bicicletas_por_tipo[tipo], start=1):
            print(f"Posición {index}: {ciclista['nombre']} - Tiempo: {ciclista['tiempo']} segundos")


def guardar_posiciones_json(lista):
    """
    Guarda las posiciones de los ciclistas en un archivo JSON ordenado por tipo y tiempo descendente.

    Args:
    - lista (list): Lista de diccionarios representando a los ciclistas.
    """
    # Agrupar bicicletas por tipo
    bicicletas_por_tipo = {}
    for ciclista in lista:
        tipo = ciclista["tipo"]
        if tipo not in bicicletas_por_tipo:
            bicicletas_por_tipo[tipo] = []
        bicicletas_por_tipo[tipo].append(ciclista)

    # Ordenar cada grupo por tiempo descendente
    for tipo in bicicletas_por_tipo:
        bicicletas_por_tipo[tipo].sort(key=lambda x: x["tiempo"], reverse=True)

    # Crear estructura para guardar en JSON
    data_to_save = []
    for tipo in sorted(bicicletas_por_tipo.keys()):
        tipo_data = {
            "Tipo": tipo,
            "Posiciones": []
        }
        for index, ciclista in enumerate(bicicletas_por_tipo[tipo], start=1):
            posicion = {
                "Posicion": index,  
                "Nombre": ciclista["nombre"],
                "Tiempo": ciclista["tiempo"]
            }
            tipo_data["Posiciones"].append(posicion)
        data_to_save.append(tipo_data)

    # Obtener el nombre del archivo y la ruta completa
    nombre_archivo = "posiciones.json"
    ruta_completa = get_path_actual(nombre_archivo)

    # Guardar en archivo JSON
    with open(ruta_completa, "w", encoding="utf-8") as archivo:
        json.dump(data_to_save, archivo, indent=4, ensure_ascii=False)  

    print(f"Se ha guardado el listado de posiciones en '{ruta_completa}'.")