class Evento:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.invitados = []
        self.tareas = []
        self.elementos = []
        self.agenda = []
        self.gastos = []

    # Gestión de invitados
    def agregar_invitado(self, invitado):
        self.invitados.append(invitado)

    def confirmar_asistencia(self, invitado):
        print(f"{invitado} confirmó su asistencia.")

    # Gestión de tareas
    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def completar_tarea(self, tarea):
        print(f"Tarea completada: {tarea}")

    # Gestión de elementos
    def agregar_elemento(self, elemento):
        self.elementos.append(elemento)

    # Gestión de agenda
    def agregar_actividad(self, actividad):
        self.agenda.append(actividad)

    # Gestión de gastos
    def agregar_gasto(self, descripcion, valor):
        self.gastos.append({
            "descripcion": descripcion,
            "valor": valor
        })

    # Mostrar información
    def mostrar_informacion(self):
        print(f"\nEvento: {self.nombre}")
        print(f"Fecha: {self.fecha}")
        print(f"Invitados: {self.invitados}")
        print(f"Tareas: {self.tareas}")
        print(f"Elementos: {self.elementos}")
        print(f"Agenda: {self.agenda}")
        print(f"Gastos: {self.gastos}")


# Crear un evento
evento = Evento("Cumpleaños", "15/09/2026")

# Agregar información
evento.agregar_invitado("Carlos")
evento.agregar_invitado("María")

evento.confirmar_asistencia("Carlos")

evento.agregar_tarea("Comprar decoración")
evento.agregar_tarea("Preparar comida")

evento.agregar_elemento("Globos")
evento.agregar_elemento("Mesa")

evento.agregar_actividad("6:00 PM - Llegada de invitados")

evento.agregar_gasto("Decoración", 80000)

# Mostrar información del evento
evento.mostrar_informacion()