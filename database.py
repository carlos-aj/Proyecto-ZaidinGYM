from sqlalchemy import create_engine, and_, func
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from typing import List, Optional, Dict, Any
import os

# Importar modelos ORM
from models import (
    Base, PersonaModel, SocioModel, SocioPremiumModel, MonitorModel, 
    EspecialidadMonitorModel, ActividadModel, VotoActividadModel,
    create_database_engine, create_session
)

# Importar clases originales de dominio
from persona import Persona
from socio import Socio
from socioPremium import SocioPremium
from monitor import Monitor
from actividad import Actividad, Especialidad
from valorable import Valorable

class DatabaseManager:
    """Gestiona todas las operaciones de base de datos usando SQLAlchemy ORM"""
    
    def __init__(self, db_path: str = "zaidinGym_orm.db"):
        """Inicializa el gestor de base de datos con SQLAlchemy
        
        Args:
            db_path (str): Ruta al archivo de la base de datos
        """
        self.db_path = db_path
        self.engine = create_database_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        print("Base de datos SQLAlchemy inicializada correctamente.")
        
    def _get_session(self):
        """Obtiene una nueva sesión de SQLAlchemy"""
        return self.Session()

    def cargar_datos_iniciales(self) -> None:
        """Carga datos iniciales si la base de datos está vacía"""
        session = self._get_session()
        try:
            # Verificar si ya hay datos
            persona_count = session.query(PersonaModel).count()
            if persona_count > 0:
                print("La base de datos ya contiene datos. Saltando carga inicial.")
                return
            
            print("Cargando datos iniciales...")
            
            # Crear actividades
            actividades_datos = [
                ("Yoga Matutino", 60, 250, "CORE", False),
                ("Aqua Aeróbicos", 45, 300, "PISCINA", True),
                ("CrossFit Intensivo", 50, 450, "FITNESS", True),
                ("Spinning", 45, 400, "CICLISMO", False),
                ("HIIT Cardio", 30, 350, "HIIT", False),
                ("Zumba", 55, 320, "BAILE", False),
                ("Pilates", 50, 200, "CORE", False),
                ("Body Pump", 60, 380, "FITNESS", False),
                ("Aqua Zumba", 45, 280, "PISCINA", True),
                ("Stretching", 30, 150, "BODYCARE", False),
                ("Cardio Dance", 40, 300, "CARDIO", False),
                ("Natación Libre", 60, 400, "PISCINA", True)
            ]
            
            for nombre, duracion, calorias, categoria, premium in actividades_datos:
                actividad_obj = Actividad(nombre, duracion, calorias, Especialidad[categoria], premium, [])
                
                actividad_model = ActividadModel(
                    nombre=nombre,
                    duracion=duracion,
                    calorias=calorias,
                    categoria=categoria,
                    es_premium=premium
                )
                session.add(actividad_model)
                
                # Agregar algunos votos de ejemplo
                votos_ejemplo = [8, 9, 7, 8, 9, 10, 7, 8] if premium else [7, 8, 6, 7, 8]
                for voto in votos_ejemplo:
                    voto_model = VotoActividadModel(actividad=actividad_model, voto=voto)
                    session.add(voto_model)
            
            # Crear monitores
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
            
            for nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, especialidades, sueldo, pos, neg in monitores_datos:
                monitor_model = MonitorModel(
                    nombre=nombre, dni=dni, direccion=direccion, localidad=localidad,
                    provincia=provincia, codigo_postal=codigo, telefono=telefono,
                    fecha_nacimiento=fecha_nac, sueldo=sueldo,
                    votos_positivos=pos, votos_negativos=neg
                )
                session.add(monitor_model)
                session.flush()  # Para obtener el ID
                
                # Agregar especialidades
                for esp in especialidades:
                    especialidad_model = EspecialidadMonitorModel(
                        monitor_id=monitor_model.id,
                        especialidad=esp
                    )
                    session.add(especialidad_model)
            
            # Crear socios regulares
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
            
            for nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo in socios_datos:
                socio_model = SocioModel(
                    nombre=nombre, dni=dni, direccion=direccion, localidad=localidad,
                    provincia=provincia, codigo_postal=codigo, telefono=telefono,
                    fecha_nacimiento=fecha_nac, fecha_registro=fecha_reg,
                    ultimo_acceso=ultimo_acc, esta_activo=activo
                )
                session.add(socio_model)
            
            # Crear socios premium  
            socios_premium_datos = [
                ("Elena Vázquez Herrera", "77889900D", "Calle Alhambra 88", "Granada", "Granada", "18011",
                 "666333555", date(1989, 6, 25), date(2023, 1, 20), date(2026, 3, 8), True),
                ("Francisco Molina Reyes", "88990011K", "Avenida Andalucía 150", "Granada", "Granada", "18012",
                 "666444777", date(1983, 3, 14), date(2023, 2, 15), date(2026, 3, 9), True),
                ("Rocío Castillo Navarro", "99001122Z", "Calle San Jerónimo 35", "Granada", "Granada", "18013",
                 "666555888", date(1991, 9, 7), date(2023, 3, 25), date(2026, 2, 25), True)
            ]
            
            for nombre, dni, direccion, localidad, provincia, codigo, telefono, fecha_nac, fecha_reg, ultimo_acc, activo in socios_premium_datos:
                socio_premium_model = SocioPremiumModel(
                    nombre=nombre, dni=dni, direccion=direccion, localidad=localidad,
                    provincia=provincia, codigo_postal=codigo, telefono=telefono,
                    fecha_nacimiento=fecha_nac, fecha_registro=fecha_reg,
                    ultimo_acceso=ultimo_acc, esta_activo=activo
                )
                session.add(socio_premium_model)
            
            session.commit()
            
            # Asignar actividades a socios
            self._asignar_actividades_iniciales(session)
            
            print("✅ Datos iniciales cargados correctamente")
            
        except Exception as e:
            session.rollback()
            print(f"Error cargando datos iniciales: {e}")
        finally:
            session.close()
    
    def _asignar_actividades_iniciales(self, session):
        """Asigna actividades iniciales a los socios"""
        try:
            # Obtener actividades
            yoga = session.query(ActividadModel).filter_by(nombre="Yoga Matutino").first()
            hiit = session.query(ActividadModel).filter_by(nombre="HIIT Cardio").first()
            aqua_aerobicos = session.query(ActividadModel).filter_by(nombre="Aqua Aeróbicos").first()
            crossfit = session.query(ActividadModel).filter_by(nombre="CrossFit Intensivo").first()
            pilates = session.query(ActividadModel).filter_by(nombre="Pilates").first()
            
            # Obtener socios
            socios = session.query(SocioModel).all()
            socios_premium = session.query(SocioPremiumModel).all()
            
            # Asignar a socios regulares
            for i, socio in enumerate(socios):
                if i < 3 and yoga:
                    socio.actividades.append(yoga)
                if i < 2 and hiit:
                    socio.actividades.append(hiit)
            
            # Asignar a socios premium (pueden acceder a actividades premium)
            for i, socio in enumerate(socios_premium):
                if aqua_aerobicos:
                    socio.actividades.append(aqua_aerobicos)
                if crossfit and i < 2:
                    socio.actividades.append(crossfit)
                if pilates:
                    socio.actividades.append(pilates)
            
            session.commit()
        except Exception as e:
            print(f"Error asignando actividades iniciales: {e}")

    def obtener_todas_actividades(self) -> List[Actividad]:
        """Obtiene todas las actividades de la base de datos usando ORM"""
        session = self._get_session()
        try:
            actividad_models = session.query(ActividadModel).all()
            actividades = []
            
            for model in actividad_models:
                # Convertir votos
                votos = [voto.voto for voto in model.votos]
                # Crear objeto dominio
                actividad = Actividad(
                    model.nombre, model.duracion, model.calorias,
                    Especialidad[model.categoria], model.es_premium, votos
                )
                actividades.append(actividad)
            
            return actividades
        finally:
            session.close()

    def obtener_todos_socios(self) -> List[Socio]:
        """Obtiene todos los socios de la base de datos usando ORM"""
        session = self._get_session()
        try:
            socio_models = session.query(SocioModel).all()
            socios = []
            
            for model in socio_models:
                # Determinar tipo de socio
                if model.tipo_persona == 'socio_premium':
                    socio = SocioPremium(
                        model.nombre, model.dni, model.direccion, model.localidad,
                        model.provincia, model.codigo_postal, model.telefono,
                        model.fecha_nacimiento, model.fecha_registro,
                        model.ultimo_acceso, model.esta_activo
                    )
                else:
                    socio = Socio(
                        model.nombre, model.dni, model.direccion, model.localidad,
                        model.provincia, model.codigo_postal, model.telefono,
                        model.fecha_nacimiento, model.fecha_registro,
                        model.ultimo_acceso, model.esta_activo
                    )
                
                # Cargar actividades asignadas
                for actividad_model in model.actividades:
                    votos = [voto.voto for voto in actividad_model.votos]
                    actividad = Actividad(
                        actividad_model.nombre, actividad_model.duracion,
                        actividad_model.calorias, Especialidad[actividad_model.categoria],
                        actividad_model.es_premium, votos
                    )
                    socio._Socio__lista_actividades.append(actividad)
                
                socios.append(socio)
            
            return socios
        finally:
            session.close()
            
    def obtener_todos_monitores(self) -> List[Monitor]:
        """Obtiene todos los monitores de la base de datos usando ORM"""
        session = self._get_session()
        try:
            monitor_models = session.query(MonitorModel).all()
            monitores = []
            
            for model in monitor_models:
                # Obtener especialidades
                especialidades = [esp.especialidad for esp in model.especialidades]
                
                monitor = Monitor(
                    model.nombre, model.dni, model.direccion, model.localidad,
                    model.provincia, model.codigo_postal, model.telefono,
                    model.fecha_nacimiento, especialidades, model.sueldo,
                    model.votos_positivos, model.votos_negativos
                )
                monitores.append(monitor)
            
            return monitores
        finally:
            session.close()
    
    def insertar_socio(self, socio: Socio) -> bool:
        """Inserta un nuevo socio en la base de datos usando ORM"""
        session = self._get_session()
        try:
            # Determinar tipo de modelo
            if isinstance(socio, SocioPremium):
                socio_model = SocioPremiumModel(
                    nombre=socio.nombre, dni=socio.dni, direccion=socio.direccion,
                    localidad=socio.localidad, provincia=socio.provincia,
                    codigo_postal=socio.codigo_postal, telefono=socio.telefono,
                    fecha_nacimiento=socio.fecha_nacimiento, fecha_registro=socio.fecha_registro,
                    ultimo_acceso=socio.ultimo_acceso, esta_activo=socio.esta_activo
                )
            else:
                socio_model = SocioModel(
                    nombre=socio.nombre, dni=socio.dni, direccion=socio.direccion,
                    localidad=socio.localidad, provincia=socio.provincia,
                    codigo_postal=socio.codigo_postal, telefono=socio.telefono,
                    fecha_nacimiento=socio.fecha_nacimiento, fecha_registro=socio.fecha_registro,
                    ultimo_acceso=socio.ultimo_acceso, esta_activo=socio.esta_activo
                )
            
            session.add(socio_model)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error insertando socio: {e}")
            return False
        finally:
            session.close()
        
    def insertar_monitor(self, monitor: Monitor) -> bool:
        """Inserta un nuevo monitor en la base de datos usando ORM"""
        session = self._get_session()
        try:
            monitor_model = MonitorModel(
                nombre=monitor.nombre, dni=monitor.dni, direccion=monitor.direccion,
                localidad=monitor.localidad, provincia=monitor.provincia,
                codigo_postal=monitor.codigo_postal, telefono=monitor.telefono,
                fecha_nacimiento=monitor.fecha_nacimiento, sueldo=monitor.sueldo,
                votos_positivos=monitor.votos_positivos, votos_negativos=monitor.votos_negativos
            )
            
            session.add(monitor_model)
            session.flush()  # Para obtener el ID
            
            # Agregar especialidades
            for esp in monitor.especialidad:
                especialidad_model = EspecialidadMonitorModel(
                    monitor_id=monitor_model.id,
                    especialidad=esp
                )
                session.add(especialidad_model)
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error insertando monitor: {e}")
            return False
        finally:
            session.close()
    
    def insertar_actividad(self, actividad: Actividad) -> bool:
        """Inserta una nueva actividad en la base de datos usando ORM"""
        session = self._get_session()
        try:
            actividad_model = ActividadModel(
                nombre=actividad.nombre,
                duracion=actividad.duracion,
                calorias=actividad.calorias,
                categoria=actividad.categoria.name,
                es_premium=actividad.es_premium
            )
            
            session.add(actividad_model)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"Error insertando actividad: {e}")
            return False
        finally:
            session.close()

    def agregar_socio_actividad(self, dni_socio: str, nombre_actividad: str) -> bool:
        """Agrega una actividad a un socio usando ORM"""
        session = self._get_session()
        try:
            socio_model = session.query(SocioModel).filter(SocioModel.dni == dni_socio).first()
            actividad_model = session.query(ActividadModel).filter_by(nombre=nombre_actividad).first()
            
            if socio_model and actividad_model:
                if actividad_model not in socio_model.actividades:
                    socio_model.actividades.append(actividad_model)
                    session.commit()
                    return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error agregando actividad a socio: {e}")
            return False
        finally:
            session.close()

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la base de datos usando ORM"""
        session = self._get_session()
        try:
            stats = {}
            
            # Contar socios regulares, premium y monitores
            stats['total_socios'] = session.query(SocioModel).count()
            stats['total_monitores'] = session.query(MonitorModel).count()
            stats['total_actividades'] = session.query(ActividadModel).count()
            stats['socios_activos'] = session.query(SocioModel).filter_by(esta_activo=True).count()
            stats['socios_premium'] = session.query(SocioPremiumModel).count()
            
            return stats
            
        finally:
            session.close()

    # Métodos adicionales para mantener compatibilidad con funcionalidades existentes
    def actualizar_ultimo_acceso_socio(self, dni: str) -> bool:
        """Actualiza el último acceso del socio usando ORM"""
        session = self._get_session()
        try:
            socio_model = session.query(SocioModel).filter(SocioModel.dni == dni).first()
            if socio_model:
                socio_model.ultimo_acceso = date.today()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error actualizando último acceso: {e}")
            return False
        finally:
            session.close()

    def eliminar_actividad_socio(self, dni_socio: str, nombre_actividad: str) -> bool:
        """Elimina una actividad de un socio usando ORM"""
        session = self._get_session()
        try:
            socio_model = session.query(SocioModel).join(PersonaModel).filter(PersonaModel.dni == dni_socio).first()
            actividad_model = session.query(ActividadModel).filter_by(nombre=nombre_actividad).first()
            
            if socio_model and actividad_model and actividad_model in socio_model.actividades:
                socio_model.actividades.remove(actividad_model)
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error eliminando actividad de socio: {e}")
            return False
        finally:
            session.close()

    def agregar_voto_actividad(self, nombre_actividad: str, voto: int) -> bool:
        """Agrega un voto a una actividad usando ORM"""
        session = self._get_session()
        try:
            actividad_model = session.query(ActividadModel).filter_by(nombre=nombre_actividad).first()
            if actividad_model:
                voto_model = VotoActividadModel(actividad=actividad_model, voto=voto)
                session.add(voto_model)
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error agregando voto: {e}")
            return False
        finally:
            session.close()

    def convertir_socio_a_premium(self, dni: str) -> bool:
        """Convierte un socio regular a premium usando ORM"""
        session = self._get_session()
        try:
            socio_model = session.query(SocioModel).join(PersonaModel).filter(
                and_(PersonaModel.dni == dni, PersonaModel.tipo_persona == 'socio')
            ).first()
            
            if socio_model:
                # Cambiar tipo en PersonaModel
                persona_model = session.query(PersonaModel).filter_by(dni=dni).first()
                persona_model.tipo_persona = 'socio_premium'
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error convirtiendo socio a premium: {e}")
            return False
        finally:
            session.close()

    def eliminar_usuario(self, dni: str) -> bool:
        """Elimina un usuario de la base de datos usando ORM"""
        session = self._get_session()
        try:
            persona_model = session.query(PersonaModel).filter_by(dni=dni).first()
            if persona_model:
                session.delete(persona_model)
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error eliminando usuario: {e}")
            return False
        finally:
            session.close()

    def invalidar_socio(self, dni: str) -> bool:
        """Invalida un socio usando ORM"""
        session = self._get_session()
        try:
            socio_model = session.query(SocioModel).join(PersonaModel).filter(PersonaModel.dni == dni).first()
            if socio_model:
                socio_model.esta_activo = False
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error invalidando socio: {e}")
            return False
        finally:
            session.close()

    def actualizar_sueldo_monitor(self, nombre: str, nuevo_sueldo: float) -> bool:
        """Actualiza el sueldo de un monitor usando ORM"""
        session = self._get_session()
        try:
            monitor_model = session.query(MonitorModel).join(PersonaModel).filter(PersonaModel.nombre == nombre).first()
            if monitor_model:
                monitor_model.sueldo = nuevo_sueldo
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error actualizando sueldo: {e}")
            return False
        finally:
            session.close()

    def actualizar_especialidades_monitor(self, nombre: str, especialidades: List[str]) -> bool:
        """Actualiza las especialidades de un monitor usando ORM"""
        session = self._get_session()
        try:
            monitor_model = session.query(MonitorModel).join(PersonaModel).filter(PersonaModel.nombre == nombre).first()
            if monitor_model:
                # Eliminar especialidades actuales
                for esp in monitor_model.especialidades:
                    session.delete(esp)
                
                # Agregar nuevas especialidades
                for esp_nombre in especialidades:
                    esp_model = EspecialidadMonitorModel(monitor_id=monitor_model.id, especialidad=esp_nombre)
                    session.add(esp_model)
                
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error actualizando especialidades: {e}")
            return False
        finally:
            session.close()

    def actualizar_votos_monitor(self, nombre: str, voto_positivo: bool) -> bool:
        """Actualiza los votos de un monitor usando ORM"""
        session = self._get_session()
        try:
            monitor_model = session.query(MonitorModel).join(PersonaModel).filter(PersonaModel.nombre == nombre).first()
            if monitor_model:
                if voto_positivo:
                    monitor_model.votos_positivos += 1
                else:
                    monitor_model.votos_negativos += 1
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error actualizando votos: {e}")
            return False
        finally:
            session.close()

    def eliminar_actividad(self, nombre: str) -> bool:
        """Elimina una actividad de la base de datos usando ORM"""
        session = self._get_session()
        try:
            actividad_model = session.query(ActividadModel).filter_by(nombre=nombre).first()
            if actividad_model:
                session.delete(actividad_model)
                session.commit()
                return True
            return False
            
        except Exception as e:
            session.rollback()
            print(f"Error eliminando actividad: {e}")
            return False
        finally:
            session.close()

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos (para compatibilidad)"""
        # Con SQLAlchemy ORM, las sesiones se manejan automáticamente
        pass