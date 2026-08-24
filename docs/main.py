from app.eventos.factory import CreadorEventoSocial, CreadorEventoAcademico, CreadorEventoFamiliar


def mostrar_menu():
    print("\n================================")
    print("           ENAGENDA")
    print("================================")
    print("Aplicación para organizar eventos pequeños.")
    print("\nTipos de evento disponibles:")
    print("1. Social")
    print("2. Académico")
    print("3. Familiar")
    print("0. Salir")


def crear_evento(opcion):
    creadores = {
        "1": CreadorEventoSocial(),
        "2": CreadorEventoAcademico(),
        "3": CreadorEventoFamiliar(),
    }

    creador = creadores.get(opcion)

    if creador is None:
        return None

    return creador.crear_evento()


def main():
    print("EnAgenda iniciado correctamente.")

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "0":
            print("Hasta luego.")
            break

        evento = crear_evento(opcion)

        if evento is None:
            print("Opción no válida.")
            continue

        evento.mostrar_informacion()


if __name__ == "__main__":
    main()
