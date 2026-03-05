from persona import Persona
from monitor import Monitor
from socio import Socio
from socioPremium import SocioPremium
from actividad import Actividad

from datetime import date, datetime
import re

class ZaidinGym:
    """Clase que representa el programa principal del gimnasion ZaidinGYM, que gestiona las actividades, socios y monitores del gimnasio."""
    
    @staticmethod
    def main() -> None:
        lista_usuarios_total = []
        lista_actividades_total = []
        
        while True:
            ZaidinGym.mostrar_menu()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                ZaidinGym.menu_gestion_usuarios(lista_usuarios_total, lista_actividades_total)
                
            elif opcion == "2":
                ZaidinGym.menu_gestion_actividades(lista_actividades_total)
                
            elif opcion == "3":
                ZaidinGym.menu_consultas_estadisticas(lista_usuarios_total, lista_actividades_total)
                
            elif opcion == "4":
                print("\nGracias por usar ZaidinGYM. Hasta luego.")
                break
                
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
                input("Presione Enter para continuar...")

    @staticmethod
    def cargar_datos_iniciales(lista_usuarios_total: list, lista_actividades_total: list) -> None:
        """Carga datos iniciales de prueba en las listas de usuarios y actividades"""

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
    def menu_gestion_usuarios(lista_usuarios_total : list, lista_actividades_total: list) -> None:
        """Muestra el menú de gestión de usuarios.
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
            lista_actividades_total (list): La lista de actividades disponibles en el gimnasio.
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
                creado = ZaidinGym.crear_usuario(lista_usuarios_total)
                if creado:
                    print(f"Total de usuarios: {len(lista_usuarios_total)}")
                input("Presione Enter para continuar...")
            elif opcion == "2":
                eliminado = ZaidinGym.eliminar_usuario(lista_usuarios_total)
                if eliminado:
                    print(f"Total de usuarios: {len(lista_usuarios_total)}")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                print(f"\n Introduzca el DNI del socio para gestionar sus actividades (formato: 12345678A):")
                dni = input().strip()
                if dni in [usuario.dni for usuario in lista_usuarios_total if isinstance(usuario, Socio)]:    
                    #Actualizar último acceso del socio
                    for usuario in lista_usuarios_total:
                        if usuario.dni.upper() == dni.upper() and isinstance(usuario, Socio):
                            usuario.ultimo_acceso = date.today()
                            break
                    ZaidinGym.menu_gestion_socios(lista_usuarios_total, lista_actividades_total, dni)
            elif opcion == "4":
                ZaidinGym.menu_gestion_monitores(lista_usuarios_total)
            elif opcion == "5":
                invalidar = ZaidinGym.invalidar_socios(lista_usuarios_total)
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
    def menu_gestion_socios(lista_usuarios_total, lista_actividades_total: list, dni: str) -> None:
        """Muestra el menú de gestión de socios.
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
            lista_actividades_total (list): La lista de actividades disponibles en el gimnasio.
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
                usuario = ZaidinGym.get_usuario_por_dni(lista_usuarios_total, dni)
                if usuario and isinstance(usuario, Socio):
                    if len(usuario.lista_actividades) == 0:
                        print("\nEl socio no tiene actividades asignadas.")
                    else:
                        print("\nActividades asignadas al socio:")
                        for idx, actividad in enumerate(usuario.lista_actividades):
                            print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
                input("Presione Enter para continuar...")

            elif opcion == "2":
                usuario = ZaidinGym.get_usuario_por_dni(lista_usuarios_total, dni)
                if usuario and isinstance(usuario, Socio):
                    print("\nActividades disponibles:")
                    for idx, actividad in enumerate(lista_actividades_total):
                        print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
                    print(f"\nSeleccione una actividad para añadir al socio (1-{len(lista_actividades_total)}):")
                    seleccion = input().strip()
                    if seleccion.isdigit() and 1 <= int(seleccion) <= len(lista_actividades_total):
                        actividad_seleccionada = lista_actividades_total[int(seleccion) - 1]
                        if usuario.add_actvidad(actividad_seleccionada):
                            print(f"Actividad '{actividad_seleccionada.nombre}' añadida al socio '{usuario.nombre}'.")
                        else:
                            print("No se pudo añadir la actividad al socio.")
                    else:
                        print("Selección no válida.")
                input("Presione Enter para continuar...")

            elif opcion == "3":
                usuario = ZaidinGym.get_usuario_por_dni(lista_usuarios_total, dni)
                if usuario and isinstance(usuario, Socio):
                    if len(usuario.lista_actividades) == 0:
                        print("\nEl socio no tiene actividades asignadas.")
                    else:
                        print("\nActividades asignadas al socio:")
                        for idx, actividad in enumerate(usuario.lista_actividades):
                            print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
                        print(f"\nSeleccione una actividad para eliminar del socio (1-{len(usuario.lista_actividades)}):")
                        seleccion = input().strip()
                        if seleccion.isdigit() and 1 <= int(seleccion) <= len(usuario.lista_actividades):
                            actividad_seleccionada = usuario.lista_actividades[int(seleccion) - 1]
                            if usuario.del_actividad(actividad_seleccionada):
                                print(f"Actividad '{actividad_seleccionada.nombre}' eliminada del socio '{usuario.nombre}'.")
                            else:
                                print("No se pudo eliminar la actividad del socio.")
                        else:
                            print("Selección no válida.")
                input("Presione Enter para continuar...")

            elif opcion == "4":
                actividad = ZaidinGym.seleccionar_actividad_para_valorar(lista_actividades_total)
                if actividad:
                    print(f"\nIntroduzca una valoración para la actividad '{actividad.nombre}' (0-10):")
                    valoracion = input().strip()
                    if valoracion.isdigit() and 0 <= int(valoracion) <= 10:
                        actividad.votar(int(valoracion))
                        print(f"Gracias por valorar la actividad '{actividad.nombre}' con {valoracion} puntos.")
                    else:
                        print("Valoración no válida. Debe ser un número entre 0 y 10.")
                input("Presione Enter para continuar...")

            elif opcion == "5":
                usuario = ZaidinGym.get_usuario_por_dni(lista_usuarios_total, dni)
                if usuario and isinstance(usuario, Socio) and not isinstance(usuario, SocioPremium):
                    nuevo_premium = SocioPremium(usuario.nombre, usuario.dni, usuario.direccion, usuario.localidad, usuario.provincia,
                                                usuario.codigo_postal, usuario.telefono, usuario.fecha_nacimiento, usuario.fecha_registro,
                                                usuario.ultimo_acceso, usuario.esta_activo)
                    nuevo_premium.lista_actividades = usuario.lista_actividades.copy()
                    lista_usuarios_total.remove(usuario)
                    lista_usuarios_total.append(nuevo_premium)
                    print(f"El socio '{usuario.nombre}' ha sido convertido en socio premium.")
                input("Presione Enter para continuar...")
            elif opcion == "6":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 6.")
                input("Presione Enter para continuar...")

    @staticmethod
    def menu_gestion_monitores(lista_usuarios_total: list) -> None:
        """Muestra el menú de gestión de monitores.
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
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
                print("\nFuncionalidad en desarrollo: Actualizar sueldo")
                input("Presione Enter para continuar...")
            elif opcion == "2":
                print("\nFuncionalidad en desarrollo: Actualizar especialidad")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                print("\nFuncionalidad en desarrollo: Valorar monitor")
                input("Presione Enter para continuar...")
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 4.")
                input("Presione Enter para continuar...")

    @staticmethod
    def menu_gestion_actividades(lista_actividades_total: list) -> None:
        """Muestra el menú de gestión de actividades.
        Args:
            lista_actividades_total (list): La lista de actividades del gimnasio.
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
                print("\nFuncionalidad en desarrollo: Crear actividad")
                input("Presione Enter para continuar...")
            elif opcion == "2":
                print("\nFuncionalidad en desarrollo: Eliminar actividad")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                break
            else:
                print("Opción no válida. Seleccione del 1 al 3.")
                input("Presione Enter para continuar...")

    @staticmethod
    def menu_consultas_estadisticas(lista_usuarios_total: list, lista_actividades_total: list) -> None:
        """Muestra el menú de consultas y estadísticas.
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio.
            lista_actividades_total (list): La lista de actividades del gimnasio.
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
                print("\nFuncionalidad en desarrollo: Listar personas")
                input("Presione Enter para continuar...")
            elif opcion == "2":
                print("\nFuncionalidad en desarrollo: Mejores actividades")
                input("Presione Enter para continuar...")
            elif opcion == "3":
                print("\nFuncionalidad en desarrollo: Mejores por categoría")
                input("Presione Enter para continuar...")
            elif opcion == "4":
                print("\nFuncionalidad en desarrollo: Mejores por kcal")
                input("Presione Enter para continuar...")
            elif opcion == "5":
                print("\nFuncionalidad en desarrollo: Mejores monitores")
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
    def crear_usuario(lista_usuarios: list) -> None:
        """Crea un nuevo usuario (socio, socio premium o monitor) y lo agrega a la lista
        Args:            
            lista_usuarios (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
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
                lista_usuarios.append(nuevo_usuario)
                print("\n✓ Socio creado exitosamente.")
                return True
            elif tipo_usuario == "2":
                nuevo_usuario = SocioPremium(nombre, dni, direccion, localidad, provincia, codigo_postal,
                                    telefono, fecha_nacimiento, fecha_registro, ultimo_acceso, esta_activo)
                lista_usuarios.append(nuevo_usuario)
                print("\n✓ Socio premium creado exitosamente.")
                return True
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
                lista_usuarios.append(nuevo_usuario)
                print("\n✓ Monitor creado exitosamente.")
                return True
                
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
    def eliminar_usuario(lista_usuarios_total: list) -> bool:
        """Elimina un usuario de la lista por su DNI
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
        
        Returns:
            bool: True si el usuario se eliminó correctamente, False si no se encontró el usuario o hubo un error.
        """
        print("\n=== ELIMINAR USUARIO ===")
        dni = ZaidinGym.solicitar_dato_con_validacion(
            "\nIntroduzca el DNI del usuario a eliminar (formato: 12345678A):", 
            ZaidinGym.validar_dni
        )

        for usuario in lista_usuarios_total:
            if usuario.dni.upper() == dni.upper():
                print(f"\nUsuario encontrado: {usuario.nombre} (DNI: {usuario.dni})")
                confirmacion = input("¿Está seguro que desea eliminar este usuario? (s/n): ").strip().lower()
                if confirmacion == "s":
                    break
                else:
                    print("Eliminación cancelada.")
                    return False
        
        for i, usuario in enumerate(lista_usuarios_total):
            if usuario.dni.upper() == dni.upper():
                del lista_usuarios_total[i]
                print(f"\nUsuario con DNI {dni} eliminado exitosamente.")
                return True
        
        print(f"\nError: No se encontró ningún usuario con DNI {dni}.")
        return False
    
    @staticmethod
    def invalidar_socios(lista_usuarios_total: list) -> list[Socio] | None:
        """Invalida socios que no han accedido en el último mes
        Args:
            lista_usuarios_total (list): La lista de usuarios del gimnasio, que incluye tanto socios como monitores.
            
        Returns:
            list[Socio] | None: Una lista de socios que fueron invalidados, o None si no se encontraron socios para invalidar.
        """
        hoy = date.today()
        socios_invalidados = []
        
        for usuario in lista_usuarios_total:
            if isinstance(usuario, Socio) and usuario.esta_activo:
                dias_desde_ultimo_acceso = (hoy - usuario.ultimo_acceso).days
                if dias_desde_ultimo_acceso > 30:
                    usuario.esta_activo = False
                    socios_invalidados.append(usuario)
        
        if socios_invalidados:
            return socios_invalidados
        else:
            return None
        
    @staticmethod
    def seleccionar_actividad_para_valorar(lista_actividades_total: list) -> Actividad | None:
        """Permite al usuario seleccionar una actividad de la lista para valorar
        Args:
            lista_actividades_total (list): La lista de actividades disponibles en el gimnasio.
        
        Returns:
            Actividad | None: La actividad seleccionada por el usuario, o None si no se seleccionó ninguna actividad válida.
        """
        if not lista_actividades_total:
            print("No hay actividades disponibles para valorar.")
            return None
        
        print("\nActividades disponibles para valorar:")
        for idx, actividad in enumerate(lista_actividades_total):
            print(f"{idx + 1}. {actividad.nombre} (Categoría: {actividad.categoria.value}, Kcal: {actividad.calorias})")
        
        while True:
            print(f"\nSeleccione una actividad para valorar (1-{len(lista_actividades_total)}), o 0 para cancelar:")
            seleccion = input().strip()
            if seleccion == "0":
                print("Valoración cancelada.")
                return None
            if seleccion.isdigit() and 1 <= int(seleccion) <= len(lista_actividades_total):
                actividad_seleccionada = lista_actividades_total[int(seleccion) - 1]
                print(f"Has seleccionado: {actividad_seleccionada.nombre}")
                return actividad_seleccionada
            else:
                print("Selección no válida. Por favor, inténtelo de nuevo.")


if __name__ == "__main__":
    ZaidinGym.main()