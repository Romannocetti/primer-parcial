from fun import *
import os

#funcion para borrar la pantalla al continuar
def clear_screen():
    if os.name == 'nt':
        os.system('cls') 
    else:
        os.system('clear')  

# Función para mostrar el menú
def menu():
    print("Menu:")
    print("1. cargar archivo")
    print("2. imprimir lista")
    print("3. asignar tiempos ")
    print("4. informar ganador")
    print("5. Filtrar por tipo (BMX, PLAYERA, MTB, PASEO)")
    print("6. promediar por tipos: BMX, PLAYERA, MTB, PASEO")
    print("7. mostrar pocisiones de cada ciclista")
    print("8. pasar las pocisiones a un archivo json")
    print("9. cerrar el programa")

    opcion = input("Opción: ")
    return opcion

# Función principal del programa
while True:
    clear_screen()
    opcion = menu()

    if opcion == "1":
        cargar_archivo()
    elif opcion == "2":
        for ciclista in lista:
            print(ciclista)
    elif opcion == "3":
        asignar_tiempos(ciclista)
    elif opcion == "4":
        ganador_o_empate(lista)
    elif opcion == "5":
        tipo = input("Ingrese el tipo a filtrar (BMX, PLAYERA, MTB, PASEO): ").upper()
        if tipo in ["BMX", "PLAYERA", "MTB", "PASEO"]:
            filtrar_por_tipo(tipo)
        else:
            print("Tipo inválido. Por favor, ingrese uno de los tipos válidos.")
    elif opcion == "6":
        tipo = input("Ingrese el tipo a promediar (BMX, PLAYERA, MTB, PASEO): ").upper()
        if tipo in ["BMX", "PLAYERA", "MTB", "PASEO"]:
            # Filtrar la lista por el tipo seleccionado antes de calcular el promedio
            ciclistas_tipo = [ciclista for ciclista in lista if ciclista["tipo"] == tipo]
            if ciclistas_tipo:
                calcular_promedio_por_tipo(ciclistas_tipo)
    elif opcion == "7":
        mostrar_posiciones(lista)
    elif opcion == "8":
        guardar_posiciones_json(lista)
    elif opcion == "9":
        print("cerrar el programa")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")

    input("Presione Enter para continuar...")








