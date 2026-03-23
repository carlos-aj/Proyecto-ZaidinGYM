from persona import Persona
from monitor import Monitor
from socio import Socio
from socioPremium import SocioPremium
from actividad import Actividad, Especialidad
from database import DatabaseManager

from datetime import date, datetime
import re

class ZaidinGym:
    """Clase que representa el programa principal del gimnasion ZaidinGYM, que gestiona las actividades, socios y monitores del gimnasio."""
    
    @staticmethod
    def main() -> None:
        # Inicializar base de datos
        db_manager = DatabaseManager()
        
        # Cargar datos iniciales si es la primera vez
        db_manager.cargar_datos_iniciales()
        
        # ============= CÓDIGO ANTERIOR =============
        # lista_usuarios_total = []
        # lista_actividades_total = []
        # 
        # # Cargar datos iniciales de prueba
        # ZaidinGym.cargar_datos_iniciales(lista_usuarios_total, lista_actividades_total)
        # =======================================================
        
        while True:
            ZaidinGym.mostrar_menu()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                ZaidinGym.menu_gestion_usuarios(db_manager)
                
            elif opcion == "2":
                ZaidinGym.menu_gestion_actividades(db_manager)
                
            elif opcion == "3":
                ZaidinGym.menu_consultas_estadisticas(db_manager)
                
            elif opcion == "4":
                print("\nGracias por usar ZaidinGYM. Hasta luego.")
                break
                
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
                input("Presione Enter para continuar...")

    # ============= CÓDIGO ANTERIOR =============
    # @staticmethod
    # def cargar_datos_iniciales(lista_usuarios_total: list, lista_actividades_total: list) -> None:
    #     """Carga datos iniciales de prueba en las listas de usuarios y actividades
    #     Args:
    #         lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
    #         lista_actividades_total (list): La lista de actividades disponibles en el gimnasio.
    #     """
    #     print("Cargando datos iniciales de prueba...")
    #     
    #     try:
    #         # Crear actividades de prueba
    #         actividades_datos = [
    #             ("Yoga Matutino", 60, 250, Especialidad.CORE, False, [8, 9, 7, 8, 9]),
    #             ("Aqua Aeróbicos", 45, 300, Especialidad.PISCINA, True, [9, 8, 10, 7]),
    #             ("CrossFit Intensivo", 50, 450, Especialidad.FITNESS, True, [10, 9, 8, 9, 10]),
    #             ("Spinning", 45, 400, Especialidad.CICLISMO, False, [8, 7, 9, 8]),
    #             ("HIIT Cardio", 30, 350, Especialidad.HIIT, False, [9, 8, 7, 9, 8]),
    #             ("Zumba", 55, 320, Especialidad.BAILE, False, [10, 9, 8, 9]),
    #             ("Pilates", 50, 200, Especialidad.CORE, False, [8, 9, 7, 8]),
    #             ("Body Pump", 60, 380, Especialidad.FITNESS, False, [9, 8, 9, 7]),
    #             ("Aqua Zumba", 45, 280, Especialidad.PISCINA, True, [8, 9, 10]),
    #             ("Stretching", 30, 150, Especialidad.BODYCARE, False, [7, 8, 9]),
    #             ("Cardio Dance", 40, 300, Especialidad.CARDIO, False, [9, 8, 7, 8]),
    #             ("Natación Libre", 60, 400, Especialidad.PISCINA, True, [9, 10, 8])
    #         ]
    #         
    #         for nombre, duracion, calorias, categoria, premium, votos in actividades_datos:
    #             actividad = Actividad(nombre, duracion, calorias, categoria, premium, votos)
    #             lista_actividades_total.append(actividad)
    #         
    #         # Crear monitores de prueba
    #         monitores_datos = [
    #             ("Ana García López", "12345678Z", "Calle Granada 15", "Granada", "Granada", "18001", "666111222", date(1985, 3, 20), ["FITNESS", "CORE"], 2200.0, 15, 2),
    #             ("Carlos Ruiz Martín", "87654321X", "Avenida Constitución 45", "Granada", "Granada", "18002", "666333444", date(1990, 7, 12), ["PISCINA"], 2000.0, 20, 1),
    #             ("María Fernández Gil", "11223344B", "Plaza Nueva 8", "Granada", "Granada", "18003", "666555777", date(1988, 11, 5), ["BAILE", "CARDIO"], 2100.0, 18, 3),
    #             ("Pedro Sánchez Vega", "55667788Z", "Calle Recogidas 23", "Granada", "Granada", "18004", "666888999", date(1982, 2, 28), ["CICLISMO", "HIIT"], 2300.0, 12, 0),
    #             ("Laura Jiménez Ramos", "99887766P", "Paseo del Salón 12", "Granada", "Granada", "18005", "666222333", date(1992, 9, 18), ["BODYCARE"], 1900.0, 10, 1)
    #         ]
    #         
    #         for nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, especialidades, sueldo, pos, neg in monitores_datos:
    #             monitor = Monitor(nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, especialidades, sueldo, pos, neg)
    #             lista_usuarios_total.append(monitor)
    #         
    #         # Crear socios regulares de prueba
    #         socios_datos = [
    #             ("Juan Pérez Morales", "22334455Y", "Calle Albaicín 30", "Granada", "Granada", "18006", "666444555", date(1995, 5, 10), date(2023, 1, 15), date(2026, 3, 5), True),
    #             ("Carmen López Silva", "33445566R", "Avenida Madrid 67", "Granada", "Granada", "18007", "666777888", date(1987, 8, 22), date(2023, 2, 20), date(2026, 2, 28), True),
    #             ("Roberto García Díaz", "44556677L", "Calle Elvira 45", "Granada", "Granada", "18008", "666999000", date(1993, 12, 8), date(2023, 3, 10), date(2025, 12, 20), False),
    #             ("Isabel Martín Cruz", "56789012B", "Plaza Trinidad 18", "Granada", "Granada", "18009", "666111333", date(1990, 4, 15), date(2023, 4, 5), date(2026, 3, 1), True),
    #             ("Miguel Rodríguez Font", "66778899D", "Calle Mesones 22", "Granada", "Granada", "18010", "666222444", date(1985, 10, 30), date(2023, 5, 12), date(2026, 1, 15), True)
    #         ]
    #         
    #         for nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo in socios_datos:
    #             socio = Socio(nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo)
    #             # Asignar algunas actividades a los socios
    #             if len(lista_actividades_total) > 0:
    #                 socio.add_actvidad(lista_actividades_total[0])  # Yoga
    #             if len(lista_actividades_total) > 4:
    #                 socio.add_actvidad(lista_actividades_total[4])  # HIIT Cardio
    #             lista_usuarios_total.append(socio)
    #         
    #         # Crear socios premium de prueba
    #         from socioPremium import SocioPremium
    #         socios_premium_datos = [
    #             ("Elena Vázquez Herrera", "77889900D", "Calle Alhambra 88", "Granada", "Granada", "18011", "666333555", date(1989, 6, 25), date(2023, 1, 20), date(2026, 3, 8), True),
    #             ("Francisco Molina Reyes", "88990011K", "Avenida Andalucía 150", "Granada", "Granada", "18012", "666444777", date(1983, 3, 14), date(2023, 2, 15), date(2026, 3, 9), True),
    #             ("Rocío Castillo Navarro", "99001122Z", "Calle San Jerónimo 35", "Granada", "Granada", "18013", "666555888", date(1991, 9, 7), date(2023, 3, 25), date(2026, 2, 25), True)
    #         ]
    #         
    #         for nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo in socios_premium_datos:
    #             socio_premium = SocioPremium(nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo)
    #             # Los socios premium pueden tener actividades premium
    #             if len(lista_actividades_total) > 1:
    #                 socio_premium.add_actvidad(lista_actividades_total[1])  # Aqua Aeróbicos (premium)
    #             if len(lista_actividades_total) > 2:
    #                 socio_premium.add_actvidad(lista_actividades_total[2])  # CrossFit Intensivo (premium)
    #             if len(lista_actividades_total) > 6:
    #                 socio_premium.add_actvidad(lista_actividades_total[6])  # Pilates
    #             lista_usuarios_total.append(socio_premium)
    #         
    #     except Exception as e:
    #         print(f"Error cargando datos iniciales: {e}")
    #         # Si hay error, crear al menos datos mínimos
    #         if not lista_actividades_total:
    #             actividad_basica = Actividad("Actividad Básica", 30, 200, Especialidad.FITNESS, False, [])
    #             lista_actividades_total.append(actividad_basica)
    # =======================================================

    @staticmethod
    def mostrar_menu() -> None:
        """Muestra el menú principal del programa."""
        print("\n" + "="*50)
        print("     BIENVENIDO A ZAIDIN GYM")
        print("="*50)
        print("1. Gestionar usuarios (socios y monitores)")
        print("2. Gestionar actividades")
        print("3. Consultas y estadísticas")
        print("4. Salir")
        print("="*50)

    @staticmethod
    def menu_gestion_usuarios(db_manager: DatabaseManager) -> None:
        """Muestra el menú de gestión de usuarios.
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
        """
        while True:
            print("\n" + "-"*40)
            print("GESTIÓN DE USUARIOS")
            print("-"*40)
            print("1. Alta personas (socio o monitor)")
            print("2. Baja personas (socio o monitor)")
            print("3. Gestionar socios")
            print("4. Gestionar monitores")
            print("5. Invalidar socios")
            print("6. Volver al menú principal")
            print("-"*40)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                creado = ZaidinGym.crear_usuario(db_manager)
                if creado:
                    stats = db_manager.obtener_estadisticas()
                    total_usuarios = stats['total_socios'] + stats['total_monitores']
                    print(f"Total de usuarios: {total_usuarios}")
                input("Presione Enter para continuar...")
            elif opcion == "2":
                eliminado = ZaidinGym.eliminar_usuario(db_manager)
                if eliminado:
                    stats = db_manager.obtener_estadisticas()
                    total_usuarios = stats['total_socios'] + stats['total_monitores']
                    print(f"Total de usuarios: {total_usuarios}")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                print(f"\n Introduzca el DNI del socio para gestionar sus actividades (formato: 12345678A):")
                dni = input().strip()
                socios = db_manager.obtener_todos_socios()
                socio_encontrado = None
                for socio in socios:
                    if socio.dni.upper() == dni.upper():
                        socio_encontrado = socio
                        break
                
                if socio_encontrado:
                    # Actualizar último acceso del socio
                    db_manager.actualizar_ultimo_acceso_socio(dni)
                    ZaidinGym.menu_gestion_socios(db_manager, dni)
                else:
                    print(f"No se encontró ningún socio con el DNI '{dni}'.")
                    input("Presione Enter para continuar...")
            elif opcion == "4":
                print(f"\n Introduzca el nombre del monitor para gestionar su perfil:")
                nombre_monitor = input().strip()
                monitores = db_manager.obtener_todos_monitores()
                monitor_encontrado = any(monitor.nombre.lower() == nombre_monitor.lower() for monitor in monitores)
                
                if monitor_encontrado:
                    ZaidinGym.menu_gestion_monitores(db_manager, nombre_monitor)
                else:
                    print(f"No se encontró ningún monitor con el nombre '{nombre_monitor}'.")
                    input("Presione Enter para continuar...")
            elif opcion == "5":
                invalidar = ZaidinGym.invalidar_socios(db_manager)
                if invalidar:
                    print("Socios invalidados correctamente.")
                    for invalido in invalidar:
                        print(f"Socio invalidado: {invalido.nombre} (DNI: {invalido.dni})")
                else:
                    print("No se encontraron socios para invalidar.")
                input("Presione Enter para continuar...")
            elif opcion == "6":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 6.")
                input("Presione Enter para continuar...")

    @staticmethod
    def menu_gestion_socios(db_manager: DatabaseManager, dni: str) -> None:
        """Muestra el menú de gestión de socios.
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            dni (str): El DNI del socio a gestionar.
        """
        while True:
            print("\n" + "-"*40)
            print("GESTIÓN DE SOCIOS")
            print("-"*40)
            print("1. Mostrar lista de actividades")
            print("2. Añadir actividad a socio")
            print("3. Eliminar actividad de socio")
            print("4. Valorar actividad")
            print("5. Convertir en socio premium")
            print("6. Volver al menú anterior")
            print("-"*40)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                socios = db_manager.obtener_todos_socios()
                socio_encontrado = None
                for socio in socios:
                    if socio.dni.upper() == dni.upper():
                        socio_encontrado = socio
                        break
                
                if socio_encontrado:
                    if len(socio_encontrado._Socio__lista_actividades) == 0:
                        print("\nEl socio no tiene actividades asignadas.")
                    else:
                        print("\nActividades asignadas al socio:")
                        for idx, actividad in enumerate(socio_encontrado._Socio__lista_actividades):
                            print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
                input("Presione Enter para continuar...")

            elif opcion == "2":
                socios = db_manager.obtener_todos_socios()
                socio_encontrado = None
                for socio in socios:
                    if socio.dni.upper() == dni.upper():
                        socio_encontrado = socio
                        break
                
                if socio_encontrado:
                    actividades = db_manager.obtener_todas_actividades()
                    print("\nActividades disponibles:")
                    for idx, actividad in enumerate(actividades):
                        print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
                    print(f"\nSeleccione una actividad para añadir al socio (1-{len(actividades)}):")
                    seleccion = input().strip()
                    if seleccion.isdigit() and 1 <= int(seleccion) <= len(actividades):
                        actividad_seleccionada = actividades[int(seleccion) - 1]
                        if db_manager.agregar_socio_actividad(dni, actividad_seleccionada.nombre):
                            print(f"Actividad '{actividad_seleccionada.nombre}' añadida al socio '{socio_encontrado.nombre}'.")
                        else:
                            print("No se pudo añadir la actividad al socio.")
                    else:
                        print("Selección no válida.")
                input("Presione Enter para continuar...")

            elif opcion == "3":
                socios = db_manager.obtener_todos_socios()
                socio_encontrado = None
                for socio in socios:
                    if socio.dni.upper() == dni.upper():
                        socio_encontrado = socio
                        break
                
                if socio_encontrado:
                    if len(socio_encontrado._Socio__lista_actividades) == 0:
                        print("\nEl socio no tiene actividades asignadas.")
                    else:
                        print("\nActividades asignadas al socio:")
                        for idx, actividad in enumerate(socio_encontrado._Socio__lista_actividades):
                            print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
                        print(f"\nSeleccione una actividad para eliminar del socio (1-{len(socio_encontrado._Socio__lista_actividades)}):")
                        seleccion = input().strip()
                        if seleccion.isdigit() and 1 <= int(seleccion) <= len(socio_encontrado._Socio__lista_actividades):
                            actividad_seleccionada = socio_encontrado._Socio__lista_actividades[int(seleccion) - 1]
                            if db_manager.eliminar_actividad_socio(dni, actividad_seleccionada.nombre):
                                print(f"Actividad '{actividad_seleccionada.nombre}' eliminada del socio '{socio_encontrado.nombre}'.")
                            else:
                                print("No se pudo eliminar la actividad del socio.")
                        else:
                            print("Selección no válida.")
                input("Presione Enter para continuar...")

            elif opcion == "4":
                actividades = db_manager.obtener_todas_actividades()
                actividad = ZaidinGym.seleccionar_actividad_para_valorar(actividades)
                if actividad:
                    print(f"\nIntroduzca una valoración para la actividad '{actividad.nombre}' (0-10):")
                    valoracion = input().strip()
                    if valoracion.isdigit() and 0 <= int(valoracion) <= 10:
                        if db_manager.agregar_voto_actividad(actividad.nombre, int(valoracion)):
                            print(f"Gracias por valorar la actividad '{actividad.nombre}' con {valoracion} puntos.")
                        else:
                            print("Error al registrar la valoración.")
                    else:
                        print("Valoración no válida. Debe ser un número entre 0 y 10.")
                input("Presione Enter para continuar...")

            elif opcion == "5":
                socios = db_manager.obtener_todos_socios()
                socio_encontrado = None
                for socio in socios:
                    if socio.dni.upper() == dni.upper():
                        socio_encontrado = socio
                        break
                
                if socio_encontrado and not isinstance(socio_encontrado, SocioPremium):
                    if db_manager.convertir_socio_a_premium(dni):
                        print(f"El socio '{socio_encontrado.nombre}' ha sido convertido en socio premium.")
                    else:
                        print("Error al convertir el socio a premium.")
                elif isinstance(socio_encontrado, SocioPremium):
                    print("El socio ya es premium.")
                else:
                    print("Socio no encontrado.")
                input("Presione Enter para continuar...")
            elif opcion == "6":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 6.")
                input("Presione Enter para continuar...")

    @staticmethod
    def menu_gestion_monitores(db_manager: DatabaseManager, nombre_monitor: str) -> None:
        """Muestra el menú de gestión de monitores.
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            nombre_monitor (str): El nombre del monitor a gestionar.
        """
        while True:
            print("\n" + "-"*40)
            print("GESTIÓN DE MONITORES")
            print("-"*40)
            print("1. Actualizar sueldo")
            print("2. Actualizar especialidad")
            print("3. Valorar monitor")
            print("4. Volver al menú anterior")
            print("-"*40)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                actualizado = ZaidinGym.actualizar_sueldo_monitor(db_manager, nombre_monitor)
                if actualizado:
                    print(f"Sueldo del monitor '{nombre_monitor}' actualizado correctamente.")
                else:
                    print(f"No se pudo actualizar el sueldo del monitor '{nombre_monitor}'.")
                input("Presione Enter para continuar...")
            elif opcion == "2":
                actualizado = ZaidinGym.actualizar_especialidad_monitor(db_manager, nombre_monitor)
                if actualizado:
                    print(f"Especialidad del monitor '{nombre_monitor}' actualizada correctamente.")
                else:
                    print(f"No se pudo actualizar la especialidad del monitor '{nombre_monitor}'.")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                valorado = ZaidinGym.valorar_monitor(db_manager, nombre_monitor)
                if valorado:
                    print(f"Gracias por valorar al monitor '{nombre_monitor}'.")
                else:
                    print(f"No se pudo valorar al monitor '{nombre_monitor}'.")
                input("Presione Enter para continuar...")
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 4.")
                input("Presione Enter para continuar...")

    @staticmethod
    def menu_gestion_actividades(db_manager: DatabaseManager) -> None:
        """Muestra el menú de gestión de actividades.
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
        """
        while True:
            print("\n" + "-"*40)
            print("GESTIÓN DE ACTIVIDADES")
            print("-"*40)
            print("1. Crear actividad")
            print("2. Eliminar actividad")
            print("3. Volver al menú principal")
            print("-"*40)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                creada = ZaidinGym.crear_actividad(db_manager)
                if creada:
                    stats = db_manager.obtener_estadisticas()
                    print(f"Total de actividades: {stats['total_actividades']}")
                input("Presione Enter para continuar...")
            elif opcion == "2":
                eliminada = ZaidinGym.eliminar_actividad(db_manager)
                if eliminada:
                    stats = db_manager.obtener_estadisticas()
                    print(f"Total de actividades: {stats['total_actividades']}")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 3.")
                input("Presione Enter para continuar...")

    @staticmethod
    def menu_consultas_estadisticas(db_manager: DatabaseManager) -> None:
        """Muestra el menú de consultas y estadísticas.
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
        """
        while True:
            print("\n" + "-"*40)
            print("CONSULTAS Y ESTADÍSTICAS")
            print("-"*40)
            print("1. Listar personas existentes")
            print("2. Listar las n mejores actividades")
            print("3. Listar las n mejores actividades por categoría")
            print("4. Listar las n mejores actividades por kcal")
            print("5. Listar los n mejores monitores")
            print("6. Volver al menú principal")
            print("-"*40)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                print("\nPersonas existentes en el gimnasio:")
                socios = db_manager.obtener_todos_socios()
                monitores = db_manager.obtener_todos_monitores()
                
                for socio in socios:
                    tipo = "Socio Premium" if isinstance(socio, SocioPremium) else "Socio"
                    print(f"- {socio.nombre} (DNI: {socio.dni}, Tipo: {tipo})")
                
                for monitor in monitores:
                    print(f"- {monitor.nombre} (DNI: {monitor.dni}, Tipo: Monitor)")
                
                input("Presione Enter para continuar...")
            elif opcion == "2":
                print("Cuantas actividades desea listar?")
                n_str = input().strip()
                if n_str.isdigit() and int(n_str) > 0:
                    n = int(n_str)
                    actividades = db_manager.obtener_todas_actividades()
                    actividades_ordenadas = sorted(actividades, key=lambda a: a.calcular_valoracion(), reverse=True)
                    print(f"\nLas {n} mejores actividades:")
                    for idx, actividad in enumerate(actividades_ordenadas[:n]):
                        print(f"{idx + 1}. {actividad.nombre} (Valoración: {actividad.calcular_valoracion()}, Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
                else:
                    print("Número no válido. Debe ser un entero positivo.")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                print("Cuantas actividades por categoría desea listar?")
                n_str = input().strip()
                if n_str.isdigit() and int(n_str) > 0:
                    n = int(n_str)
                    actividades = db_manager.obtener_todas_actividades()
                    categorias = set(actividad.categoria for actividad in actividades)
                    for categoria in categorias:
                        actividades_categoria = [a for a in actividades if a.categoria == categoria]
                        actividades_ordenadas = sorted(actividades_categoria, key=lambda a: a.calcular_valoracion(), reverse=True)
                        print(f"\nLas {n} mejores actividades de la categoría '{categoria.value}':")
                        for idx, actividad in enumerate(actividades_ordenadas[:n]):
                            print(f"{idx + 1}. {actividad.nombre} (Valoración: {actividad.calcular_valoracion()}, Kcal: {actividad.calorias})")
                else:
                    print("Número no válido. Debe ser un entero positivo.")
                input("Presione Enter para continuar...")
            elif opcion == "4":
                print("Cuantas actividades por kcal desea listar?")
                n_str = input().strip()
                if n_str.isdigit() and int(n_str) > 0:
                    n = int(n_str)
                    actividades = db_manager.obtener_todas_actividades()
                    actividades_ordenadas = sorted(actividades, key=lambda a: a.calorias, reverse=True)
                    print(f"\nLas {n} mejores actividades por kcal:")
                    for idx, actividad in enumerate(actividades_ordenadas[:n]):
                        print(f"{idx + 1}. {actividad.nombre} (Kcal: {actividad.calorias}, Valoración: {actividad.calcular_valoracion()}, Categoría: {actividad.categoria.value})")
                else:
                    print("Número no válido. Debe ser un entero positivo.")
                input("Presione Enter para continuar...")
            elif opcion == "5":
                print("Cuantos monitores desea listar?")
                n_str = input().strip()
                if n_str.isdigit() and int(n_str) > 0:
                    n = int(n_str)
                    monitores = db_manager.obtener_todos_monitores()
                    monitores_ordenados = sorted(monitores, key=lambda m: m.calcular_valoracion(), reverse=True)
                    print(f"\nLos {n} mejores monitores:")
                    for idx, monitor in enumerate(monitores_ordenados[:n]):
                        print(f"{idx + 1}. {monitor.nombre} (Valoración: {monitor.calcular_valoracion()}, Especialidades: {', '.join(monitor.especialidad)}, Sueldo: {monitor.sueldo})")
                else:
                    print("Número no válido. Debe ser un entero positivo.")
                input("Presione Enter para continuar...")
            elif opcion == "6":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 6.")
                input("Presione Enter para continuar...")

    @staticmethod
    def validar_campo_vacio(valor: str, nombre_campo: str) -> bool:
        """Valida que un campo no esté vacío
        Args:
            valor (str): El valor del campo a validar.
            nombre_campo (str): El nombre del campo, para mostrar en el mensaje de error.
        
        Returns:
            bool: True si el campo no está vacío, False en caso contrario."""
        if not valor or valor.strip() == "":
            print(f"Error: {nombre_campo} no puede estar vacío.")
            return False
        return True

    @staticmethod
    def validar_dni(dni: str) -> bool:
        """Valida el formato del DNI (8 dígitos + 1 letra)
        Args:
            dni (str): El DNI a validar.
        
        Returns:
            bool: True si el DNI es válido, False en caso contrario.
        """
        if not dni:
            return False
        dni = dni.upper().strip()
        patron = r'^[0-9]{8}[A-Z]$'
        if not re.match(patron, dni):
            print("Error: DNI debe tener formato 12345678A (8 dígitos + 1 letra)")
            return False
        return True

    @staticmethod
    def validar_telefono(telefono: str) -> bool:
        """Valida el formato del teléfono
        Args:
            telefono (str): El teléfono a validar.
        
        Returns:
            bool: True si el teléfono es válido, False en caso contrario.
        """
        if not telefono:
            return False
        telefono = telefono.strip().replace(" ", "").replace("-", "")
        if len(telefono) != 9 or not telefono.isdigit():
            print("Error: Teléfono debe tener 9 dígitos")
            return False
        return True

    @staticmethod
    def validar_codigo_postal(codigo_postal: str) -> bool:
        """Valida el formato del código postal (5 dígitos)
        Args:
            codigo_postal (str): El código postal a validar.
        
        Returns:
            bool: True si el código postal es válido, False en caso contrario.
        """
        if not codigo_postal:
            return False
        codigo_postal = codigo_postal.strip()
        if len(codigo_postal) != 5 or not codigo_postal.isdigit():
            print("Error: Código postal debe tener 5 dígitos")
            return False
        return True

    @staticmethod
    def validar_sueldo(sueldo_str: str) -> tuple[bool, float | None]:
        """Valida que el sueldo sea un número positivo
        Args:
            sueldo_str (str): El sueldo a validar.
        
        Returns:
            tuple[bool, float | None]: Una tupla donde el primer valor indica si el sueldo es válido y el segundo valor es el sueldo convertido a float si es válido, o None en caso contrario.
        """
        try:
            sueldo = float(sueldo_str)
            if sueldo <= 0:
                print("Error: El sueldo debe ser un número positivo")
                return False, None
            return True, sueldo
        except ValueError:
            print("Error: El sueldo debe ser un número válido")
            return False, None

    @staticmethod
    def validar_especialidad(especialidad_lista: list[str]) -> bool:
        """Valida que la especialidad no esté vacía
        Args:
            especialidad_lista (list[str]): Lista de especialidades a validar.
        
        Returns:
            bool: True si hay al menos una especialidad válida, False en caso contrario.
        """
        if not especialidad_lista or len(especialidad_lista) == 0:
            print("Error: Debe especificar al menos una especialidad")
            return False
        # Limpiar espacios en blanco
        especialidad_limpia = [esp.strip() for esp in especialidad_lista if esp.strip()]
        if len(especialidad_limpia) == 0:
            print("Error: Debe especificar al menos una especialidad válida")
            return False
        return True

    @staticmethod
    def solicitar_dato_con_validacion(mensaje: str, validador, *args) -> str:
        """Solicita un dato al usuario y lo valida hasta que sea correcto
        Args:
            mensaje (str): El mensaje a mostrar al usuario.
            validador (callable): La función de validación a utilizar.
            *args: Argumentos adicionales para la función de validación.
        
        Returns:
            str: El valor ingresado por el usuario si es válido.
        """
        while True:
            print(mensaje)
            valor = input().strip()
            if validador(valor, *args):
                return valor
            print("Por favor, inténtelo de nuevo.")

    @staticmethod
    def crear_usuario(db_manager: DatabaseManager) -> bool:
        """Crea un nuevo usuario (socio, socio premium o monitor) y lo guarda en la base de datos
        Args:            
            db_manager (DatabaseManager): El gestor de la base de datos.
        Returns:
            bool: True si el usuario se creó correctamente, False en caso de error.
        """
        print("\n=== CREACIÓN DE NUEVO USUARIO ===")
        
        # Solicitar y validar datos básicos
        nombre = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca el nombre:", 
            ZaidinGym.validar_campo_vacio, 
            "El nombre"
        )
        
        dni = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca el DNI (formato: 12345678A):", 
            ZaidinGym.validar_dni
        )
        
        direccion = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca la dirección:", 
            ZaidinGym.validar_campo_vacio, 
            "La dirección"
        )
        
        localidad = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca la localidad:", 
            ZaidinGym.validar_campo_vacio, 
            "La localidad"
        )
        
        provincia = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca la provincia:", 
            ZaidinGym.validar_campo_vacio, 
            "La provincia"
        )
        
        codigo_postal = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca el código postal (5 dígitos):", 
            ZaidinGym.validar_codigo_postal
        )
        
        telefono = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca el teléfono (9 dígitos):", 
            ZaidinGym.validar_telefono
        )
        
        # Validar fecha de nacimiento
        while True:
            print("\nIntroduzca la fecha de nacimiento (YYYY-MM-DD):")
            fecha_nacimiento_str = input().strip()
            if not ZaidinGym.validar_campo_vacio(fecha_nacimiento_str, "La fecha de nacimiento"):
                continue
            fecha_nacimiento = ZaidinGym.convertir_fecha(fecha_nacimiento_str)
            if fecha_nacimiento is not None:
                break
            print("Por favor, inténtelo de nuevo.")
        
        fecha_registro = date.today()
        ultimo_acceso = date.today()
        esta_activo = True
        
        # Validar tipo de usuario
        while True:
            print("\nTipo de usuario:")
            print("1. Socio")
            print("2. Socio Premium") 
            print("3. Monitor")
            tipo_usuario = input("Seleccione una opción (1-3): ").strip()
            
            if tipo_usuario in ["1", "2", "3"]:
                break
            print("Error: Debe seleccionar 1, 2 o 3. Por favor, inténtelo de nuevo.")
        
        try:
            if tipo_usuario == "1":
                nuevo_usuario = Socio(nombre, dni, direccion, localidad, provincia, codigo_postal,
                                    telefono, fecha_nacimiento, fecha_registro, ultimo_acceso, esta_activo)
                resultado = db_manager.insertar_socio(nuevo_usuario)
                if resultado:
                    print("\n✓ Socio creado exitosamente.")
                    return True
                else:
                    print("\n✗ Error al crear el socio.")
                    return False
            elif tipo_usuario == "2":
                nuevo_usuario = SocioPremium(nombre, dni, direccion, localidad, provincia, codigo_postal,
                                    telefono, fecha_nacimiento, fecha_registro, ultimo_acceso, esta_activo)
                resultado = db_manager.insertar_socio(nuevo_usuario)
                if resultado:
                    print("\n✓ Socio premium creado exitosamente.")
                    return True
                else:
                    print("\n✗ Error al crear el socio premium.")
                    return False
            elif tipo_usuario == "3":
                # Validaciones específicas para Monitor
                while True:
                    print("\nIntroduzca las especialidades (separada por comas):")
                    especialidad_str = input().strip()
                    if not ZaidinGym.validar_campo_vacio(especialidad_str, "Las especialidades"):
                        continue
                    especialidad = especialidad_str.split(",")
                    if ZaidinGym.validar_especialidad(especialidad):
                        # Limpiar especialidades
                        especialidad = [esp.strip() for esp in especialidad if esp.strip()]
                        break
                    print("Por favor, inténtelo de nuevo.")
                
                # Validar sueldo
                while True:
                    print("\nIntroduzca el sueldo:")
                    sueldo_str = input().strip()
                    if not ZaidinGym.validar_campo_vacio(sueldo_str, "El sueldo"):
                        continue
                    es_valido, sueldo = ZaidinGym.validar_sueldo(sueldo_str)
                    if es_valido:
                        break
                    print("Por favor, inténtelo de nuevo.")
                
                votos_positivos = 0
                votos_negativos = 0
                
                nuevo_usuario = Monitor(nombre, dni, direccion, localidad, provincia, codigo_postal,
                                    telefono, fecha_nacimiento, especialidad, sueldo, votos_positivos, votos_negativos)
                resultado = db_manager.insertar_monitor(nuevo_usuario)
                if resultado:
                    print("\n✓ Monitor creado exitosamente.")
                    return True
                else:
                    print("\n✗ Error al crear el monitor.")
                    return False
                
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
            return False
        
    @staticmethod
    def convertir_fecha(fecha_string: str) -> date | None:
        """Convierte una fecha en formato string (YYYY-MM-DD) a un objeto date"""
        try:
            return datetime.strptime(fecha_string, "%Y-%m-%d").date()
        except ValueError:
            print("Formato de fecha inválido. Use YYYY-MM-DD (ej: 1990-05-15)")
            return None
        
    @staticmethod
    def get_usuario_por_dni(lista_usuarios_total: list, dni: str) -> Persona | None:
        """Busca un usuario en la lista por su DNI
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
            dni (str): El DNI del usuario a buscar.
        
        Returns:
            Persona | None: El usuario encontrado, o None si no se encontró ningún usuario con ese DNI.
        """
        for usuario in lista_usuarios_total:
            if usuario.dni.upper() == dni.upper():
                return usuario
        return None
    
    @staticmethod
    def get_usuario_por_nombre(lista_usuarios_total: list, nombre: str) -> Persona | None:
        """Busca un usuario en la lista por su nombre
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
            nombre (str): El nombre del usuario a buscar.
        
        Returns:
            Persona | None: El usuario encontrado, o None si no se encontró ningún usuario con ese nombre.
        """
        for usuario in lista_usuarios_total:
            if usuario.nombre.lower() == nombre.lower():
                return usuario
        return None

    @staticmethod
    def eliminar_usuario(db_manager: DatabaseManager) -> bool:
        """Elimina un usuario de la base de datos por su DNI
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
        
        Returns:
            bool: True si el usuario se eliminó correctamente, False si no se encontró el usuario o hubo un error.
        """
        print("\n=== ELIMINAR USUARIO ===")
        dni = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca el DNI del usuario a eliminar (formato: 12345678A):", 
            ZaidinGym.validar_dni
        )

        # Buscar usuario en socios
        socios = db_manager.obtener_todos_socios()
        usuario_encontrado = None
        for socio in socios:
            if socio.dni.upper() == dni.upper():
                usuario_encontrado = socio
                break
        
        # Si no se encontró en socios, buscar en monitores
        if not usuario_encontrado:
            monitores = db_manager.obtener_todos_monitores()
            for monitor in monitores:
                if monitor.dni.upper() == dni.upper():
                    usuario_encontrado = monitor
                    break

        if usuario_encontrado:
            print(f"\nUsuario encontrado: {usuario_encontrado.nombre} (DNI: {usuario_encontrado.dni})")
            confirmacion = input("¿Está seguro que desea eliminar este usuario? (s/n): ").strip().lower()
            if confirmacion == "s":
                if db_manager.eliminar_usuario(dni):
                    print(f"\nUsuario con DNI {dni} eliminado exitosamente.")
                    return True
                else:
                    print(f"\nError al eliminar el usuario con DNI {dni}.")
                    return False
            else:
                print("Eliminación cancelada.")
                return False
        
        print(f"\nError: No se encontró ningún usuario con DNI {dni}.")
        return False
    
    @staticmethod
    def invalidar_socios(db_manager: DatabaseManager) -> list[Socio] | None:
        """Invalida socios que no han accedido en el último mes
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            
        Returns:
            list[Socio] | None: Una lista de socios que fueron invalidados, o None si no se encontraron socios para invalidar.
        """
        hoy = date.today()
        socios_invalidados = []
        
        socios = db_manager.obtener_todos_socios()
        for socio in socios:
            if socio.esta_activo:
                dias_desde_ultimo_acceso = (hoy - socio.ultimo_acceso).days
                if dias_desde_ultimo_acceso > 30:
                    if db_manager.invalidar_socio(socio.dni):
                        socio.esta_activo = False  # Actualizar objeto local
                        socios_invalidados.append(socio)
        
        if socios_invalidados:
            return socios_invalidados
        else:
            return None
        
    @staticmethod
    def seleccionar_actividad_para_valorar(actividades: list) -> Actividad | None:
        """Permite al usuario seleccionar una actividad de la lista para valorar
        Args:
            actividades (list): La lista de actividades disponibles en el gimnasio.
        
        Returns:
            Actividad | None: La actividad seleccionada por el usuario, o None si no se seleccionó ninguna actividad válida.
        """
        if not actividades:
            print("No hay actividades disponibles para valorar.")
            return None
        
        print("\nActividades disponibles para valorar:")
        for idx, actividad in enumerate(actividades):
            print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
        
        while True:
            print(f"\nSeleccione una actividad para valorar (1-{len(actividades)}), o 0 para cancelar:")
            seleccion = input().strip()
            if seleccion == "0":
                print("Valoración cancelada.")
                return None
            if seleccion.isdigit() and 1 <= int(seleccion) <= len(actividades):
                actividad_seleccionada = actividades[int(seleccion) - 1]
                print(f"Has seleccionado: {actividad_seleccionada.nombre}")
                return actividad_seleccionada
            else:
                print("Selección no válida. Por favor, inténtelo de nuevo.")

    @staticmethod
    def actualizar_sueldo_monitor(db_manager: DatabaseManager, nombre_monitor: str) -> bool:
        """Actualiza el sueldo de un monitor específico
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            nombre_monitor (str): El nombre del monitor al que se le actualizará el sueldo.
        
        Returns:
            bool: True si el sueldo se actualizó correctamente, False si no se encontró el monitor o hubo un error.
        """
        monitores = db_manager.obtener_todos_monitores()
        monitor_encontrado = None
        for monitor in monitores:
            if monitor.nombre.lower() == nombre_monitor.lower():
                monitor_encontrado = monitor
                break
        
        if monitor_encontrado:
            while True:
                print(f"\nIntroduzca el nuevo sueldo para el monitor '{monitor_encontrado.nombre}':")
                sueldo_str = input().strip()
                if not ZaidinGym.validar_campo_vacio(sueldo_str, "El sueldo"):
                    continue
                es_valido, nuevo_sueldo = ZaidinGym.validar_sueldo(sueldo_str)
                if es_valido:
                    if db_manager.actualizar_sueldo_monitor(monitor_encontrado.nombre, nuevo_sueldo):
                        print(f"Sueldo del monitor '{monitor_encontrado.nombre}' actualizado a {nuevo_sueldo}.")
                        return True
                    else:
                        print("Error al actualizar el sueldo en la base de datos.")
                        return False
                print("Por favor, inténtelo de nuevo.")
        
        print(f"No se encontró ningún monitor con el nombre '{nombre_monitor}'.")
        return False

    @staticmethod
    def actualizar_especialidad_monitor(db_manager: DatabaseManager, nombre_monitor: str) -> bool:
        """Actualiza la especialidad de un monitor específico
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            nombre_monitor (str): El nombre del monitor al que se le actualizará la especialidad.
        
        Returns:
            bool: True si la especialidad se actualizó correctamente, False si no se encontró el monitor o hubo un error.
        """
        monitores = db_manager.obtener_todos_monitores()
        monitor_encontrado = None
        for monitor in monitores:
            if monitor.nombre.lower() == nombre_monitor.lower():
                monitor_encontrado = monitor
                break
        
        if monitor_encontrado:
            while True:
                print(f"\nIntroduzca las nuevas especialidades para el monitor '{monitor_encontrado.nombre}' (separadas por comas):")
                especialidad_str = input().strip()
                if not ZaidinGym.validar_campo_vacio(especialidad_str, "Las especialidades"):
                    continue
                especialidad = especialidad_str.split(",")
                if ZaidinGym.validar_especialidad(especialidad):
                    # Limpiar especialidades
                    especialidad = [esp.strip() for esp in especialidad if esp.strip()]
                    if db_manager.actualizar_especialidades_monitor(monitor_encontrado.nombre, especialidad):
                        print(f"Especialidades del monitor '{monitor_encontrado.nombre}' actualizadas a: {', '.join(especialidad)}.")
                        return True
                    else:
                        print("Error al actualizar las especialidades en la base de datos.")
                        return False
                print("Por favor, inténtelo de nuevo.")
        
        print(f"No se encontró ningún monitor con el nombre '{nombre_monitor}'.")
        return False
    
    @staticmethod
    def valorar_monitor(db_manager: DatabaseManager, nombre_monitor: str) -> bool:
        """Permite valorar a un monitor específico
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            nombre_monitor (str): El nombre del monitor a valorar.
        
        Returns:
            bool: True si el monitor se valoró correctamente, False si no se encontró el monitor o hubo un error.
        """
        monitores = db_manager.obtener_todos_monitores()
        monitor_encontrado = None
        for monitor in monitores:
            if monitor.nombre.lower() == nombre_monitor.lower():
                monitor_encontrado = monitor
                break
        
        if monitor_encontrado:
            while True:
                print(f"\nIntroduzca una valoración para el monitor '{monitor_encontrado.nombre}' (0-10):")
                valoracion_str = input().strip()
                if valoracion_str.isdigit() and 0 <= int(valoracion_str) <= 10:
                    valoracion = int(valoracion_str)
                    voto_positivo = valoracion >= 5
                    if db_manager.actualizar_votos_monitor(monitor_encontrado.nombre, voto_positivo):
                        if voto_positivo:
                            print(f"Gracias por valorar positivamente al monitor '{monitor_encontrado.nombre}'.")
                        else:
                            print(f"Gracias por valorar negativamente al monitor '{monitor_encontrado.nombre}'.")
                        return True
                    else:
                        print("Error al actualizar la valoración en la base de datos.")
                        return False
                print("Valoración no válida. Debe ser un número entre 0 y 10.")
        
        print(f"No se encontró ningún monitor con el nombre '{nombre_monitor}'.")
        return False

    @staticmethod
    def crear_actividad(db_manager: DatabaseManager) -> bool:
        """Función para crear una nueva actividad.
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            
        Returns:
            bool: True si la actividad se creó correctamente, False en caso contrario.
        """
        print("\n" + "-"*40)
        print("CREAR NUEVA ACTIVIDAD")
        print("-"*40)
        
        # Solicitar nombre de la actividad
        while True:
            nombre = input("\nIntroduzca el nombre de la actividad: ").strip()
            if not ZaidinGym.validar_campo_vacio(nombre, "El nombre de la actividad"):
                continue
            if not Actividad.validar_cadena(nombre):
                print("Error: El nombre debe contener solo letras, números, espacios y algunos signos de puntuación (máximo 50 caracteres).")
                continue
            
            # Verificar si ya existe una actividad con ese nombre
            actividades_existentes = db_manager.obtener_todas_actividades()
            if any(actividad.nombre.lower() == nombre.lower() for actividad in actividades_existentes):
                print(f"Error: Ya existe una actividad con el nombre '{nombre}'.")
                continue
            break
        
        # Solicitar duración
        while True:
            duracion_str = input("\nIntroduzca la duración de la actividad en minutos (2-120): ").strip()
            if not ZaidinGym.validar_campo_vacio(duracion_str, "La duración"):
                continue
            try:
                duracion = int(duracion_str)
                if not Actividad.validar_duracion(duracion):
                    print("Error: La duración debe ser un número entero mayor que 1 y no mayor que 120 minutos.")
                    continue
                break
            except ValueError:
                print("Error: La duración debe ser un número entero.")
        
        # Solicitar calorías
        while True:
            calorias_str = input("\nIntroduzca las calorías que se queman durante la actividad: ").strip()
            if not ZaidinGym.validar_campo_vacio(calorias_str, "Las calorías"):
                continue
            try:
                calorias = int(calorias_str)
                if not Actividad.validar_calorias(calorias):
                    print("Error: Las calorías deben ser un número entero positivo mayor que 0.")
                    continue
                break
            except ValueError:
                print("Error: Las calorías deben ser un número entero.")
        
        # Mostrar especialidades disponibles y solicitar selección
        while True:
            print("\nEspecialidades disponibles:")
            especialidades = list(Especialidad)
            for idx, esp in enumerate(especialidades, 1):
                print(f"{idx}. {esp.value}")
            
            categoria_str = input(f"\nSeleccione la categoría de la actividad (1-{len(especialidades)}): ").strip()
            if not ZaidinGym.validar_campo_vacio(categoria_str, "La categoría"):
                continue
            try:
                categoria_idx = int(categoria_str)
                if 1 <= categoria_idx <= len(especialidades):
                    categoria = especialidades[categoria_idx - 1]
                    break
                else:
                    print(f"Error: Seleccione un número entre 1 y {len(especialidades)}.")
            except ValueError:
                print("Error: Introduzca un número válido.")
        
        # Solicitar si es premium
        while True:
            es_premium_str = input("\n¿Es una actividad premium? (s/n): ").strip().lower()
            if es_premium_str in ['s', 'sí', 'si', 'y', 'yes']:
                es_premium = True
                break
            elif es_premium_str in ['n', 'no']:
                es_premium = False
                break
            else:
                print("Error: Introduzca 's' para sí o 'n' para no.")
        
        try:
            # Crear la nueva actividad (inicializar votos como lista vacía)
            nueva_actividad = Actividad(nombre, duracion, calorias, categoria, es_premium, [])
            resultado = db_manager.insertar_actividad(nueva_actividad)
            
            if resultado:
                print(f"\n¡Actividad '{nombre}' creada exitosamente!")
                print(f"Detalles: {duracion} min, {calorias} kcal, {categoria.value}, {'Premium' if es_premium else 'Regular'}")
                return True
            else:
                print(f"\nError al guardar la actividad en la base de datos.")
                return False
            
        except ValueError as e:
            print(f"\nError al crear la actividad: {e}")
            return False
    
    @staticmethod
    def eliminar_actividad(db_manager: DatabaseManager) -> bool:
        """Función para eliminar una actividad existente.
        Solo se puede eliminar si no hay socios que la tengan asignada.
        Args:
            db_manager (DatabaseManager): El gestor de la base de datos.
            
        Returns:
            bool: True si la actividad se eliminó correctamente, False en caso contrario.
        """
        actividades = db_manager.obtener_todas_actividades()
        if not actividades:
            print("\nNo hay actividades disponibles para eliminar.")
            return False
        
        print("\n" + "-"*40)
        print("ELIMINAR ACTIVIDAD")
        print("-"*40)
        
        # Mostrar lista de actividades disponibles
        print("\nActividades disponibles:")
        for idx, actividad in enumerate(actividades, 1):
            print(f"{idx}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Duración: {actividad.duracion} min, Calorías: {actividad.calorias})")
        
        # Solicitar selección de actividad
        while True:
            seleccion_str = input(f"\nSeleccione la actividad a eliminar (1-{len(actividades)}) o 0 para cancelar: ").strip()
            if not ZaidinGym.validar_campo_vacio(seleccion_str, "La selección"):
                continue
            
            try:
                seleccion = int(seleccion_str)
                if seleccion == 0:
                    print("Operación cancelada.")
                    return False
                elif 1 <= seleccion <= len(actividades):
                    actividad_seleccionada = actividades[seleccion - 1]
                    break
                else:
                    print(f"Error: Seleccione un número entre 0 y {len(actividades)}.")
            except ValueError:
                print("Error: Introduzca un número válido.")
        
        # Verificar si hay socios que tengan esta actividad asignada
        socios = db_manager.obtener_todos_socios()
        socios_con_actividad = []
        for socio in socios:
            if hasattr(socio, '_Socio__lista_actividades'):
                for actividad in socio._Socio__lista_actividades:
                    if actividad.nombre == actividad_seleccionada.nombre:
                        socios_con_actividad.append(socio)
                        break
        
        # Si hay socios con la actividad, no se puede eliminar
        if socios_con_actividad:
            print(f"\nNo se puede eliminar la actividad '{actividad_seleccionada.nombre}'.")
            print("Los siguientes socios tienen esta actividad asignada:")
            for socio in socios_con_actividad:
                print(f"  - {socio.nombre} (DNI: {socio.dni})")
            print("\nPara eliminar esta actividad, primero debe ser removida de todos los socios.")
            return False
        
        # Confirmar eliminación
        print(f"\n¿Está seguro de que desea eliminar la actividad '{actividad_seleccionada.nombre}'?")
        
        while True:
            confirmacion = input("¿Confirma la eliminación? (s/n): ").strip().lower()
            if confirmacion in ['s', 'sí', 'si', 'y', 'yes']:
                break
            elif confirmacion in ['n', 'no']:
                print("Operación cancelada.")
                return False
            else:
                print("Error: Introduzca 's' para sí o 'n' para no.")
        
        # Eliminar la actividad
        try:
            if db_manager.eliminar_actividad(actividad_seleccionada.nombre):
                print(f"\n¡Actividad '{actividad_seleccionada.nombre}' eliminada exitosamente!")
                return True
            else:
                print(f"\nError al eliminar la actividad '{actividad_seleccionada.nombre}'.")
                return False
            
        except Exception as e:
            print(f"\nError: No se pudo eliminar la actividad '{actividad_seleccionada.nombre}': {e}")
            return False
    

if __name__ == "__main__":
    ZaidinGym.main()