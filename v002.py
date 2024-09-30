from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Base de datos simulada
cursos_db = []

# Funciones auxiliares
def buscar_curso_por_id(curso_id: str) -> Optional[Curso]:
    """Busca un curso en la base de datos por su ID."""
    return next((curso for curso in cursos_db if curso.id == curso_id), None)

def manejar_error_curso_no_encontrado(curso_id: str):
    """Lanza una excepción si el curso no es encontrado."""
    raise HTTPException(status_code=404, detail=f"Curso con ID {curso_id} no encontrado")

def actualizar_datos_curso(curso_actual: Curso, curso_actualizado: Curso) -> Curso:
    """Actualiza los datos de un curso actual con los del curso actualizado."""
    curso_actual.nombre = curso_actualizado.nombre
    curso_actual.descripcion = curso_actualizado.descripcion
    curso_actual.nivel = curso_actualizado.nivel
    curso_actual.duracion = curso_actualizado.duracion
    return curso_actual

# Rutas
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    """Obtiene todos los cursos disponibles."""
    return cursos_db

@app.post("/cursos/", response_model=Curso)
def crear_curso(curso: Curso):
    """Crea un nuevo curso."""
    curso.id = str(uuid.uuid4())  # Genera un ID único
    cursos_db.append(curso)
    return curso

@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id: str):
    """Obtiene un curso específico por su ID."""
    curso = buscar_curso_por_id(curso_id)
    if curso is None:
        manejar_error_curso_no_encontrado(curso_id)
    return curso

@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id: str, curso_actualizado: Curso):
    """Actualiza los detalles de un curso existente."""
    curso_actual = buscar_curso_por_id(curso_id)
    if curso_actual is None:
        manejar_error_curso_no_encontrado(curso_id)
    
    # Actualiza los datos del curso
    curso_actualizado.id = curso_id
    curso_actual = actualizar_datos_curso(curso_actual, curso_actualizado)
    return curso_actual

@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id: str):
    """Elimina un curso específico por su ID."""
    curso = buscar_curso_por_id(curso_id)
    if curso is None:
        manejar_error_curso_no_encontrado(curso_id)
    
    cursos_db.remove(curso)
    return curso