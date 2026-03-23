from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date
from typing import List

# Base declarativa
Base = declarative_base()

# Tabla intermedia para la relación muchos-a-muchos entre socios y actividades
socio_actividades = Table(
    'socio_actividades',
    Base.metadata,
    Column('socio_id', Integer, ForeignKey('socios.id'), primary_key=True),
    Column('actividad_id', Integer, ForeignKey('actividades.id'), primary_key=True)
)

# Tabla intermedia para especialidades de monitores
monitor_especialidades = Table(
    'monitor_especialidades', 
    Base.metadata,
    Column('monitor_id', Integer, ForeignKey('monitores.id'), primary_key=True),
    Column('especialidad', String(50), primary_key=True)
)

class PersonaModel(Base):
    """Modelo base para personas (socios y monitores)"""
    __tablename__ = 'personas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    dni = Column(String(9), unique=True, nullable=False)
    direccion = Column(String(200), nullable=False)
    localidad = Column(String(100), nullable=False)
    provincia = Column(String(100), nullable=False)
    codigo_postal = Column(String(5), nullable=False)
    telefono = Column(String(15), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    tipo_persona = Column(String(20), nullable=False)  # 'socio', 'socio_premium', 'monitor'
    
    # Relaciones polimórficas
    __mapper_args__ = {
        'polymorphic_identity': 'persona',
        'polymorphic_on': tipo_persona
    }

class SocioModel(PersonaModel):
    """Modelo para socios"""
    __tablename__ = 'socios'
    
    id = Column(Integer, ForeignKey('personas.id'), primary_key=True)
    fecha_registro = Column(Date, nullable=False)
    ultimo_acceso = Column(Date, nullable=False)
    esta_activo = Column(Boolean, nullable=False, default=True)
    
    # Relación con actividades
    actividades = relationship('ActividadModel', secondary=socio_actividades, back_populates='socios')
    
    __mapper_args__ = {
        'polymorphic_identity': 'socio',
        'inherit_condition': id == PersonaModel.id
    }

class SocioPremiumModel(SocioModel):
    """Modelo para socios premium"""
    __mapper_args__ = {
        'polymorphic_identity': 'socio_premium'
    }

class MonitorModel(PersonaModel):
    """Modelo para monitores"""
    __tablename__ = 'monitores'
    
    id = Column(Integer, ForeignKey('personas.id'), primary_key=True)
    sueldo = Column(Float, nullable=False)
    votos_positivos = Column(Integer, nullable=False, default=0)
    votos_negativos = Column(Integer, nullable=False, default=0)
    
    # Relación con especialidades (tabla intermedia)
    especialidades = relationship('EspecialidadMonitorModel', back_populates='monitor', cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity': 'monitor',
        'inherit_condition': id == PersonaModel.id
    }

class EspecialidadMonitorModel(Base):
    """Modelo para especialidades de monitores"""
    __tablename__ = 'especialidades_monitor'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    monitor_id = Column(Integer, ForeignKey('monitores.id'), nullable=False)
    especialidad = Column(String(50), nullable=False)
    
    # Relación con monitor
    monitor = relationship('MonitorModel', back_populates='especialidades')

class ActividadModel(Base):
    """Modelo para actividades"""
    __tablename__ = 'actividades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    duracion = Column(Integer, nullable=False)
    calorias = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=False)
    es_premium = Column(Boolean, nullable=False, default=False)
    
    # Relaciones
    socios = relationship('SocioModel', secondary=socio_actividades, back_populates='actividades')
    votos = relationship('VotoActividadModel', back_populates='actividad', cascade="all, delete-orphan")

class VotoActividadModel(Base):
    """Modelo para votos de actividades"""
    __tablename__ = 'votos_actividades'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    actividad_id = Column(Integer, ForeignKey('actividades.id'), nullable=False)
    voto = Column(Integer, nullable=False)  # Valoración de 0-10
    
    # Relación con actividad
    actividad = relationship('ActividadModel', back_populates='votos')

# Configuración del motor y sesión
def create_database_engine(db_path: str = "zaidinGym_orm.db"):
    """Crea el motor de base de datos SQLAlchemy"""
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    return engine

def create_session(engine):
    """Crea una sesión SQLAlchemy"""
    Session = sessionmaker(bind=engine)
    return Session()