import sqlite3
import os
from datetime import date, datetime
from typing import List, Optional, Dict, Any, Tuple
from persona import Persona
from socio import Socio
from socioPremium import SocioPremium
from monitor import Monitor
from actividad import Actividad, Especialidad
from valorable import Valorable

class DatabaseManager:
    """Gestiona todas las operaciones de base de datos SQLite3 para ZaidinGym"""
    
    def __init__(self, db_path: str = "zaidinGym.db"):
        """Inicializa el gestor de base de datos
        
        Args:
            db_path (str): Ruta al archivo de la base de datos
        """
        self.db_path = db_path
        self._create_tables()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos con configuración optimizada"""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
        conn.execute("PRAGMA foreign_keys = ON")  # Habilitar claves foráneas
        return conn
    
    def _convertir_fecha(self, fecha_str: str) -> date:
        """Convierte una fecha en formato string a objeto date"""
        if isinstance(fecha_str, date):
            return fecha_str
        try:
            return datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return date.today()
    
    def _create_tables(self) -> None:
        """Crea todas las tablas necesarias para la aplicación"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de personas (base para socios y monitores)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    dni TEXT UNIQUE NOT NULL,
                    direccion TEXT NOT NULL,
                    localidad TEXT NOT NULL,
                    provincia TEXT NOT NULL,
                    codigo_postal TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    fecha_nacimiento DATE NOT NULL,
                    tipo_persona TEXT NOT NULL CHECK (tipo_persona IN ('socio', 'socio_premium', 'monitor')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de socios (información específica de socios)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS socios (
                    id INTEGER PRIMARY KEY,
                    fecha_registro DATE NOT NULL,
                    ultimo_acceso DATE NOT NULL,
                    esta_activo BOOLEAN NOT NULL,
                    cuota REAL NOT NULL,
                    FOREIGN KEY (id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            # Tabla de monitores (información específica de monitores)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitores (
                    id INTEGER PRIMARY KEY,
                    sueldo REAL NOT NULL,
                    votos_positivos INTEGER DEFAULT 0,
                    votos_negativos INTEGER DEFAULT 0,
                    FOREIGN KEY (id) REFERENCES personas(id) ON DELETE CASCADE
                )
            """)
            
            # Tabla de especialidades de monitores
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS especialidades_monitor (
                    monitor_id INTEGER,
                    especialidad TEXT NOT NULL,
                    PRIMARY KEY (monitor_id, especialidad),
                    FOREIGN KEY (monitor_id) REFERENCES monitores(id) ON DELETE CASCADE
                )
            """)
            
            # Tabla de actividades
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS actividades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    duracion INTEGER NOT NULL,
                    calorias INTEGER NOT NULL,
                    categoria TEXT NOT NULL,
                    es_premium BOOLEAN NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de votos de actividades
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votos_actividades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actividad_id INTEGER NOT NULL,
                    voto INTEGER NOT NULL,
                    fecha_voto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE
                )
            """)
            
            # Tabla de relación socio-actividad
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS socio_actividades (
                    socio_id INTEGER,
                    actividad_id INTEGER,
                    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (socio_id, actividad_id),
                    FOREIGN KEY (socio_id) REFERENCES personas(id) ON DELETE CASCADE,
                    FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()
            print("Base de datos inicialized correctamente.")
    
    # ==================== CRUD PERSONAS ====================
    
    def insertar_socio(self, socio: Socio) -> Optional[int]:
        """Inserta un nuevo socio en la base de datos
        
        Args:
            socio (Socio): Objeto socio a insertar
            
        Returns:
            Optional[int]: ID del socio insertado o None si hay error
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Determinar tipo de socio
                tipo = "socio_premium" if isinstance(socio, SocioPremium) else "socio"
                
                # Insertar en tabla personas
                cursor.execute("""
                    INSERT INTO personas (nombre, dni, direccion, localidad, provincia, 
                                        codigo_postal, telefono, fecha_nacimiento, tipo_persona)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (socio.nombre, socio.dni, socio.direccion, socio.localidad, 
                    socio.provincia, socio.codigo_postal, socio.telefono, 
                    socio.fecha_nacimiento, tipo))
                
                persona_id = cursor.lastrowid
                
                # Insertar en tabla socios
                cursor.execute("""
                    INSERT INTO socios (id, fecha_registro, ultimo_acceso, esta_activo, cuota)
                    VALUES (?, ?, ?, ?, ?)
                """, (persona_id, socio.fecha_registro, socio.ultimo_acceso, 
                    socio.esta_activo, socio.cuota))
                
                # Insertar actividades del socio si las tiene
                if hasattr(socio, '_Socio__lista_actividades'):
                    for actividad in socio._Socio__lista_actividades:
                        actividad_id = self._get_actividad_id_by_name(actividad.nombre)
                        if actividad_id:
                            cursor.execute("""
                                INSERT OR IGNORE INTO socio_actividades (socio_id, actividad_id)
                                VALUES (?, ?)
                            """, (persona_id, actividad_id))
                
                conn.commit()
                return persona_id
                
        except sqlite3.Error as e:
            print(f"Error insertando socio: {e}")
            return None
    
    def insertar_monitor(self, monitor: Monitor) -> Optional[int]:
        """Inserta un nuevo monitor en la base de datos
        
        Args:
            monitor (Monitor): Objeto monitor a insertar
            
        Returns:
            Optional[int]: ID del monitor insertado o None si hay error
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Insertar en tabla personas
                cursor.execute("""
                    INSERT INTO personas (nombre, dni, direccion, localidad, provincia,
                                        codigo_postal, telefono, fecha_nacimiento, tipo_persona)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (monitor.nombre, monitor.dni, monitor.direccion, monitor.localidad,
                    monitor.provincia, monitor.codigo_postal, monitor.telefono,
                    monitor.fecha_nacimiento, "monitor"))
                
                persona_id = cursor.lastrowid
                
                # Insertar en tabla monitores
                cursor.execute("""
                    INSERT INTO monitores (id, sueldo, votos_positivos, votos_negativos)
                    VALUES (?, ?, ?, ?)
                """, (persona_id, monitor.sueldo, monitor.votos_positivos, monitor.votos_negativos))
                
                # Insertar especialidades del monitor
                for especialidad in monitor.especialidad:
                    cursor.execute("""
                        INSERT INTO especialidades_monitor (monitor_id, especialidad)
                        VALUES (?, ?)
                    """, (persona_id, especialidad))
                
                conn.commit()
                return persona_id
                
        except sqlite3.Error as e:
            print(f"Error insertando monitor: {e}")
            return None
    
    def obtener_todos_socios(self) -> List[Socio]:
        """Obtiene todos los socios de la base de datos
        
        Returns:
            List[Socio]: Lista de objetos Socio
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT p.*, s.fecha_registro, s.ultimo_acceso, s.esta_activo, s.cuota
                    FROM personas p
                    JOIN socios s ON p.id = s.id
                    WHERE p.tipo_persona IN ('socio', 'socio_premium')
                """)
                
                socios = []
                for row in cursor.fetchall():
                    # Crear objeto apropiado según el tipo
                    if row['tipo_persona'] == 'socio_premium':
                        socio = SocioPremium(
                            row['nombre'], row['dni'], row['direccion'],
                            row['localidad'], row['provincia'], row['codigo_postal'],
                            row['telefono'], self._convertir_fecha(row['fecha_nacimiento']), 
                            self._convertir_fecha(row['fecha_registro']),
                            self._convertir_fecha(row['ultimo_acceso']), bool(row['esta_activo'])
                        )
                    else:
                        socio = Socio(
                            row['nombre'], row['dni'], row['direccion'],
                            row['localidad'], row['provincia'], row['codigo_postal'],
                            row['telefono'], self._convertir_fecha(row['fecha_nacimiento']), 
                            self._convertir_fecha(row['fecha_registro']),
                            self._convertir_fecha(row['ultimo_acceso']), bool(row['esta_activo'])
                        )
                    
                    # Cargar actividades del socio
                    actividades = self._get_actividades_socio(row['id'])
                    for actividad in actividades:
                        socio._Socio__lista_actividades.append(actividad)
                    
                    socios.append(socio)
                
                return socios
                
        except sqlite3.Error as e:
            print(f"Error obteniendo socios: {e}")
            return []
    
    def obtener_todos_monitores(self) -> List[Monitor]:
        """Obtiene todos los monitores de la base de datos
        
        Returns:
            List[Monitor]: Lista de objetos Monitor
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT p.*, m.sueldo, m.votos_positivos, m.votos_negativos
                    FROM personas p
                    JOIN monitores m ON p.id = m.id
                    WHERE p.tipo_persona = 'monitor'
                """)
                
                monitores = []
                for row in cursor.fetchall():
                    # Obtener especialidades del monitor
                    especialidades = self._get_especialidades_monitor(row['id'])
                    
                    monitor = Monitor(
                        row['nombre'], row['dni'], row['direccion'],
                        row['localidad'], row['provincia'], row['codigo_postal'],
                        row['telefono'], self._convertir_fecha(row['fecha_nacimiento']), especialidades,
                        row['sueldo'], row['votos_positivos'], row['votos_negativos']
                    )
                    
                    monitores.append(monitor)
                
                return monitores
                
        except sqlite3.Error as e:
            print(f"Error obteniendo monitores: {e}")
            return []
    
    # ==================== CRUD ACTIVIDADES ====================
    
    def insertar_actividad(self, actividad: Actividad) -> Optional[int]:
        """Inserta una nueva actividad en la base de datos
        
        Args:
            actividad (Actividad): Objeto actividad a insertar
            
        Returns:
            Optional[int]: ID de la actividad insertada o None si hay error
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Insertar actividad
                cursor.execute("""
                    INSERT INTO actividades (nombre, duracion, calorias, categoria, es_premium)
                    VALUES (?, ?, ?, ?, ?)
                """, (actividad.nombre, actividad.duracion, actividad.calorias,
                    actividad.categoria.value, actividad.es_premium))
                
                actividad_id = cursor.lastrowid
                
                # Insertar votos si los hay
                for voto in actividad._votos:
                    cursor.execute("""
                        INSERT INTO votos_actividades (actividad_id, voto)
                        VALUES (?, ?)
                    """, (actividad_id, voto))
                
                conn.commit()
                return actividad_id
                
        except sqlite3.Error as e:
            print(f"Error insertando actividad: {e}")
            return None
    
    def obtener_todas_actividades(self) -> List[Actividad]:
        """Obtiene todas las actividades de la base de datos
        
        Returns:
            List[Actividad]: Lista de objetos Actividad
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM actividades")
                actividades = []
                
                for row in cursor.fetchall():
                    # Obtener votos de la actividad
                    cursor.execute("""
                        SELECT voto FROM votos_actividades 
                        WHERE actividad_id = ?
                    """, (row['id'],))
                    votos = [voto_row['voto'] for voto_row in cursor.fetchall()]
                    
                    # Crear objeto actividad
                    actividad = Actividad(
                        row['nombre'], row['duracion'], row['calorias'],
                        Especialidad(row['categoria']), bool(row['es_premium']), votos
                    )
                    
                    actividades.append(actividad)
                
                return actividades
                
        except sqlite3.Error as e:
            print(f"Error obteniendo actividades: {e}")
            return []
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _get_especialidades_monitor(self, monitor_id: int) -> List[str]:
        """Obtiene las especialidades de un monitor específico"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT especialidad FROM especialidades_monitor 
                    WHERE monitor_id = ?
                """, (monitor_id,))
                return [row['especialidad'] for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
    
    def _get_actividades_socio(self, socio_id: int) -> List[Actividad]:
        """Obtiene las actividades de un socio específico"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT a.* FROM actividades a
                    JOIN socio_actividades sa ON a.id = sa.actividad_id
                    WHERE sa.socio_id = ?
                """, (socio_id,))
                
                actividades = []
                for row in cursor.fetchall():
                    # Obtener votos de la actividad
                    cursor.execute("""
                        SELECT voto FROM votos_actividades 
                        WHERE actividad_id = ?
                    """, (row['id'],))
                    votos = [voto_row['voto'] for voto_row in cursor.fetchall()]
                    
                    actividad = Actividad(
                        row['nombre'], row['duracion'], row['calorias'],
                        Especialidad(row['categoria']), bool(row['es_premium']), votos
                    )
                    actividades.append(actividad)
                
                return actividades
        except sqlite3.Error:
            return []
    
    def _get_actividad_id_by_name(self, nombre: str) -> Optional[int]:
        """Obtiene el ID de una actividad por su nombre"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM actividades WHERE nombre = ?", (nombre,))
                result = cursor.fetchone()
                return result['id'] if result else None
        except sqlite3.Error:
            return None
    
    def agregar_socio_actividad(self, socio_dni: str, actividad_nombre: str) -> bool:
        """Agrega una actividad a un socio
        
        Args:
            socio_dni (str): DNI del socio
            actividad_nombre (str): Nombre de la actividad
            
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del socio
                cursor.execute("SELECT id FROM personas WHERE dni = ?", (socio_dni,))
                socio_result = cursor.fetchone()
                if not socio_result:
                    return False
                
                socio_id = socio_result['id']
                
                # Obtener ID de la actividad
                actividad_id = self._get_actividad_id_by_name(actividad_nombre)
                if not actividad_id:
                    return False
                
                # Insertar relación
                cursor.execute("""
                    INSERT OR IGNORE INTO socio_actividades (socio_id, actividad_id)
                    VALUES (?, ?)
                """, (socio_id, actividad_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error agregando actividad a socio: {e}")
            return False
    
    def cargar_datos_iniciales(self) -> None:
        """Carga datos iniciales de prueba en la base de datos"""
        # Verificar si ya hay datos
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) as count FROM personas")
                if cursor.fetchone()['count'] > 0:
                    print("La base de datos ya contiene datos. Saltando carga inicial.")
                    return
        except sqlite3.Error:
            pass
        
        print("Cargando datos iniciales en la base de datos...")
        
        # Crear y insertar actividades
        actividades_datos = [
            ("Yoga Matutino", 60, 250, Especialidad.CORE, False, [8, 9, 7, 8, 9]),
            ("Aqua Aeróbicos", 45, 300, Especialidad.PISCINA, True, [9, 8, 10, 7]),
            ("CrossFit Intensivo", 50, 450, Especialidad.FITNESS, True, [10, 9, 8, 9, 10]),
            ("Spinning", 45, 400, Especialidad.CICLISMO, False, [8, 7, 9, 8]),
            ("HIIT Cardio", 30, 350, Especialidad.HIIT, False, [9, 8, 7, 9, 8]),
            ("Zumba", 55, 320, Especialidad.BAILE, False, [10, 9, 8, 9]),
            ("Pilates", 50, 200, Especialidad.CORE, False, [8, 9, 7, 8]),
            ("Body Pump", 60, 380, Especialidad.FITNESS, False, [9, 8, 9, 7]),
            ("Aqua Zumba", 45, 280, Especialidad.PISCINA, True, [8, 9, 10]),
            ("Stretching", 30, 150, Especialidad.BODYCARE, False, [7, 8, 9]),
            ("Cardio Dance", 40, 300, Especialidad.CARDIO, False, [9, 8, 7, 8]),
            ("Natación Libre", 60, 400, Especialidad.PISCINA, True, [9, 10, 8])
        ]
        
        for nombre, duracion, calorias, categoria, premium, votos in actividades_datos:
            actividad = Actividad(nombre, duracion, calorias, categoria, premium, votos)
            self.insertar_actividad(actividad)
        
        # Crear y insertar monitores
        monitores_datos = [
            ("Ana García López", "12345678Z", "Calle Granada 15", "Granada", "Granada", "18001", 
            "666111222", date(1985, 3, 20), ["FITNESS", "CORE"], 2200.0, 15, 2),
            ("Carlos Ruiz Martín", "87654321X", "Avenida Constitución 45", "Granada", "Granada", "18002", 
            "666333444", date(1990, 7, 12), ["PISCINA"], 2000.0, 20, 1),
            ("María Fernández Gil", "11223344B", "Plaza Nueva 8", "Granada", "Granada", "18003", 
            "666555777", date(1988, 11, 5), ["BAILE", "CARDIO"], 2100.0, 18, 3),
            ("Pedro Sánchez Vega", "55667788Z", "Calle Recogidas 23", "Granada", "Granada", "18004", 
            "666888999", date(1982, 2, 28), ["CICLISMO", "HIIT"], 2300.0, 12, 0),
            ("Laura Jiménez Ramos", "99887766P", "Paseo del Salón 12", "Granada", "Granada", "18005", 
            "666222333", date(1992, 9, 18), ["BODYCARE"], 1900.0, 10, 1)
        ]
        
        for datos in monitores_datos:
            nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, especialidades, sueldo, pos, neg = datos
            monitor = Monitor(nombre, dni, direccion, localidad, provincia, codigo, telefono, 
                            fecha_nac, especialidades, sueldo, pos, neg)
            self.insertar_monitor(monitor)
        
        # Crear y insertar socios regulares
        socios_datos = [
            ("Juan Pérez Morales", "22334455Y", "Calle Albaicín 30", "Granada", "Granada", "18006", 
            "666444555", date(1995, 5, 10), date(2023, 1, 15), date(2026, 3, 5), True),
            ("Carmen López Silva", "33445566R", "Avenida Madrid 67", "Granada", "Granada", "18007", 
            "666777888", date(1987, 8, 22), date(2023, 2, 20), date(2026, 2, 28), True),
            ("Roberto García Díaz", "44556677L", "Calle Elvira 45", "Granada", "Granada", "18008", 
            "666999000", date(1993, 12, 8), date(2023, 3, 10), date(2025, 12, 20), False),
            ("Isabel Martín Cruz", "56789012B", "Plaza Trinidad 18", "Granada", "Granada", "18009", 
            "666111333", date(1990, 4, 15), date(2023, 4, 5), date(2026, 3, 1), True),
            ("Miguel Rodríguez Font", "66778899D", "Calle Mesones 22", "Granada", "Granada", "18010", 
            "666222444", date(1985, 10, 30), date(2023, 5, 12), date(2026, 1, 15), True)
        ]
        
        for datos in socios_datos:
            nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo = datos
            socio = Socio(nombre, dni, direccion, localidad, provincia, codigo, telefono, 
                        fecha_nac, fecha_reg, ultimo_acc, activo)
            socio_id = self.insertar_socio(socio)
            
            # Agregar algunas actividades
            if socio_id:
                self.agregar_socio_actividad(dni, "Yoga Matutino")
                self.agregar_socio_actividad(dni, "HIIT Cardio")
        
        # Crear y insertar socios premium
        socios_premium_datos = [
            ("Elena Vázquez Herrera", "77889900D", "Calle Alhambra 88", "Granada", "Granada", "18011", 
            "666333555", date(1989, 6, 25), date(2023, 1, 20), date(2026, 3, 8), True),
            ("Francisco Molina Reyes", "88990011K", "Avenida Andalucía 150", "Granada", "Granada", "18012", 
            "666444777", date(1983, 3, 14), date(2023, 2, 15), date(2026, 3, 9), True),
            ("Rocío Castillo Navarro", "99001122Z", "Calle San Jerónimo 35", "Granada", "Granada", "18013", 
            "666555888", date(1991, 9, 7), date(2023, 3, 25), date(2026, 2, 25), True)
        ]
        
        for datos in socios_premium_datos:
            nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo = datos
            socio_premium = SocioPremium(nombre, dni, direccion, localidad, provincia, codigo, telefono, 
                                        fecha_nac, fecha_reg, ultimo_acc, activo)
            socio_id = self.insertar_socio(socio_premium)
            
            # Los socios premium pueden tener actividades premium
            if socio_id:
                self.agregar_socio_actividad(dni, "Aqua Aeróbicos")
                self.agregar_socio_actividad(dni, "CrossFit Intensivo")
                self.agregar_socio_actividad(dni, "Pilates")
        
        print("Datos iniciales cargados exitosamente en la base de datos.")
    
    def cerrar_conexion(self) -> None:
        """Método para cerrar la conexión (no es necesario con context manager, pero útil para limpieza)"""
        # Con el patrón que estamos usando (context managers), las conexiones se cierran automáticamente
        pass
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales de la base de datos
        
        Returns:
            Dict[str, Any]: Diccionario con estadísticas
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                estadisticas = {}
                
                # Total de socios
                cursor.execute("SELECT COUNT(*) as total FROM socios")
                estadisticas['total_socios'] = cursor.fetchone()['total']
                
                # Total de monitores
                cursor.execute("SELECT COUNT(*) as total FROM monitores")
                estadisticas['total_monitores'] = cursor.fetchone()['total']
                
                # Total de actividades
                cursor.execute("SELECT COUNT(*) as total FROM actividades")
                estadisticas['total_actividades'] = cursor.fetchone()['total']
                
                # Socios activos
                cursor.execute("SELECT COUNT(*) as total FROM socios WHERE esta_activo = 1")
                estadisticas['socios_activos'] = cursor.fetchone()['total']
                
                # Socios premium
                cursor.execute("""
                    SELECT COUNT(*) as total FROM personas 
                    WHERE tipo_persona = 'socio_premium'
                """)
                estadisticas['socios_premium'] = cursor.fetchone()['total']
                
                return estadisticas
                
        except sqlite3.Error as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}

    def actualizar_ultimo_acceso_socio(self, dni: str) -> bool:
        """Actualiza la fecha de último acceso de un socio
        
        Args:
            dni (str): DNI del socio
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del socio
                cursor.execute("SELECT id FROM personas WHERE dni = ? AND tipo_persona IN ('socio', 'socio_premium')", (dni,))
                socio_result = cursor.fetchone()
                if not socio_result:
                    return False
                
                # Actualizar último acceso
                cursor.execute("""
                    UPDATE socios 
                    SET ultimo_acceso = CURRENT_DATE
                    WHERE id = ?
                """, (socio_result['id'],))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error actualizando último acceso: {e}")
            return False
    
    def eliminar_actividad_socio(self, socio_dni: str, actividad_nombre: str) -> bool:
        """Elimina una actividad de un socio
        
        Args:
            socio_dni (str): DNI del socio
            actividad_nombre (str): Nombre de la actividad
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del socio
                cursor.execute("SELECT id FROM personas WHERE dni = ?", (socio_dni,))
                socio_result = cursor.fetchone()
                if not socio_result:
                    return False
                
                socio_id = socio_result['id']
                
                # Obtener ID de la actividad
                actividad_id = self._get_actividad_id_by_name(actividad_nombre)
                if not actividad_id:
                    return False
                
                # Eliminar relación
                cursor.execute("""
                    DELETE FROM socio_actividades 
                    WHERE socio_id = ? AND actividad_id = ?
                """, (socio_id, actividad_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error eliminando actividad de socio: {e}")
            return False
    
    def agregar_voto_actividad(self, actividad_nombre: str, voto: int) -> bool:
        """Agrega un voto a una actividad
        
        Args:
            actividad_nombre (str): Nombre de la actividad
            voto (int): Voto (0-10)
            
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        try:
            if not (0 <= voto <= 10):
                return False
                
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID de la actividad
                actividad_id = self._get_actividad_id_by_name(actividad_nombre)
                if not actividad_id:
                    return False
                
                # Insertar voto
                cursor.execute("""
                    INSERT INTO votos_actividades (actividad_id, voto)
                    VALUES (?, ?)
                """, (actividad_id, voto))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error agregando voto: {e}")
            return False
    
    def convertir_socio_a_premium(self, socio_dni: str) -> bool:
        """Convierte un socio regular a socio premium
        
        Args:
            socio_dni (str): DNI del socio
            
        Returns:
            bool: True si se convirtió correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar que es un socio regular (no premium)
                cursor.execute("""
                    SELECT id FROM personas 
                    WHERE dni = ? AND tipo_persona = 'socio'
                """, (socio_dni,))
                socio_result = cursor.fetchone()
                if not socio_result:
                    return False
                
                # Actualizar tipo de persona
                cursor.execute("""
                    UPDATE personas 
                    SET tipo_persona = 'socio_premium'
                    WHERE id = ?
                """, (socio_result['id'],))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error convirtiendo a socio premium: {e}")
            return False
    
    def eliminar_usuario(self, dni: str) -> bool:
        """Elimina un usuario (socio o monitor) por su DNI
        
        Args:
            dni (str): DNI del usuario
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Verificar que el usuario existe
                cursor.execute("SELECT id FROM personas WHERE dni = ?", (dni,))
                usuario_result = cursor.fetchone()
                if not usuario_result:
                    return False
                
                # Eliminar usuario (las claves foráneas en CASCADE se encargarán del resto)
                cursor.execute("DELETE FROM personas WHERE dni = ?", (dni,))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error eliminando usuario: {e}")
            return False
    
    def invalidar_socio(self, dni: str) -> bool:
        """Invalida un socio (marca como inactivo)
        
        Args:
            dni (str): DNI del socio
            
        Returns:
            bool: True si se invalidó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del socio
                cursor.execute("SELECT id FROM personas WHERE dni = ? AND tipo_persona IN ('socio', 'socio_premium')", (dni,))
                socio_result = cursor.fetchone()
                if not socio_result:
                    return False
                
                # Invalidar socio
                cursor.execute("""
                    UPDATE socios 
                    SET esta_activo = 0
                    WHERE id = ?
                """, (socio_result['id'],))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error invalidando socio: {e}")
            return False
    
    def actualizar_sueldo_monitor(self, nombre_monitor: str, nuevo_sueldo: float) -> bool:
        """Actualiza el sueldo de un monitor
        
        Args:
            nombre_monitor (str): Nombre del monitor
            nuevo_sueldo (float): Nuevo sueldo
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del monitor
                cursor.execute("""
                    SELECT id FROM personas 
                    WHERE LOWER(nombre) = LOWER(?) AND tipo_persona = 'monitor'
                """, (nombre_monitor,))
                monitor_result = cursor.fetchone()
                if not monitor_result:
                    return False
                
                # Actualizar sueldo
                cursor.execute("""
                    UPDATE monitores 
                    SET sueldo = ?
                    WHERE id = ?
                """, (nuevo_sueldo, monitor_result['id']))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error actualizando sueldo de monitor: {e}")
            return False
    
    def actualizar_especialidades_monitor(self, nombre_monitor: str, nuevas_especialidades: List[str]) -> bool:
        """Actualiza las especialidades de un monitor
        
        Args:
            nombre_monitor (str): Nombre del monitor
            nuevas_especialidades (List[str]): Lista de nuevas especialidades
            
        Returns:
            bool: True si se actualizado correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del monitor
                cursor.execute("""
                    SELECT id FROM personas 
                    WHERE LOWER(nombre) = LOWER(?) AND tipo_persona = 'monitor'
                """, (nombre_monitor,))
                monitor_result = cursor.fetchone()
                if not monitor_result:
                    return False
                
                monitor_id = monitor_result['id']
                
                # Eliminar especialidades actuales
                cursor.execute("DELETE FROM especialidades_monitor WHERE monitor_id = ?", (monitor_id,))
                
                # Insertar nuevas especialidades
                for especialidad in nuevas_especialidades:
                    cursor.execute("""
                        INSERT INTO especialidades_monitor (monitor_id, especialidad)
                        VALUES (?, ?)
                    """, (monitor_id, especialidad.strip()))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            print(f"Error actualizando especialidades de monitor: {e}")
            return False
    
    def actualizar_votos_monitor(self, nombre_monitor: str, voto_positivo: bool) -> bool:
        """Actualiza los votos de un monitor
        
        Args:
            nombre_monitor (str): Nombre del monitor
            voto_positivo (bool): True para voto positivo, False para negativo
            
        Returns:
            bool: True si se actualizó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID del monitor
                cursor.execute("""
                    SELECT id FROM personas 
                    WHERE LOWER(nombre) = LOWER(?) AND tipo_persona = 'monitor'
                """, (nombre_monitor,))
                monitor_result = cursor.fetchone()
                if not monitor_result:
                    return False
                
                # Actualizar votos
                if voto_positivo:
                    cursor.execute("""
                        UPDATE monitores 
                        SET votos_positivos = votos_positivos + 1
                        WHERE id = ?
                    """, (monitor_result['id'],))
                else:
                    cursor.execute("""
                        UPDATE monitores 
                        SET votos_negativos = votos_negativos + 1
                        WHERE id = ?
                    """, (monitor_result['id'],))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error actualizando votos de monitor: {e}")
            return False
    
    def eliminar_actividad(self, actividad_nombre: str) -> bool:
        """Elimina una actividad de la base de datos
        
        Args:
            actividad_nombre (str): Nombre de la actividad
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Obtener ID de la actividad
                actividad_id = self._get_actividad_id_by_name(actividad_nombre)
                if not actividad_id:
                    return False
                
                # Verificar que no hay socios con esta actividad
                cursor.execute("""
                    SELECT COUNT(*) as count FROM socio_actividades 
                    WHERE actividad_id = ?
                """, (actividad_id,))
                if cursor.fetchone()['count'] > 0:
                    print(f"No se puede eliminar la actividad '{actividad_nombre}' porque hay socios inscritos.")
                    return False
                
                # Eliminar la actividad (las claves foráneas en CASCADE eliminarán los votos)
                cursor.execute("DELETE FROM actividades WHERE id = ?", (actividad_id,))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            print(f"Error eliminando actividad: {e}")
            return False