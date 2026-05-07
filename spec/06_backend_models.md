# FASE 2 — Backend Models

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: ORM SQLAlchemy (modelos Python)
**Estimación**: 45 min
**Prerequisito**: FASE 1 completada, migración aplicada

---

## Objetivo

Confirmar y completar los modelos ORM con relaciones bidireccionales, propiedades calculadas y serialización a dict.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Backend/app/models/course_rating.py` | Verificar/completar |
| `Backend/app/models/course.py` | Verificar/completar |
| `Backend/app/models/__init__.py` | Verificar exports |

---

## `course_rating.py` — Requisitos

```
CourseRating(BaseModel)
  __tablename__ = 'course_ratings'
  course_id: Integer, ForeignKey('courses.id'), nullable=False
  user_id: Integer, nullable=False
  rating: Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False
  course: relationship("Course", back_populates="ratings")
  to_dict() → retorna dict con id, course_id, user_id, rating, created_at (str ISO), updated_at (str ISO)
```

## `course.py` — Requisitos

```
Course(BaseModel)
  ratings: relationship("CourseRating", back_populates="course", cascade="all, delete-orphan")
  
  @property average_rating → float
    - Filtra deleted_at is None
    - Retorna 0.0 si no hay ratings activos
    - Redondea a 2 decimales
  
  @property total_ratings → int
    - Cuenta ratings con deleted_at is None
```

## `__init__.py` — Requisitos

```python
from app.models.course_rating import CourseRating  # debe estar exportado
```

Alembic importa desde `__init__.py` para detectar modelos en autogenerate.

---

## Criterios de Aceptación

- [ ] `CourseRating` importa sin errores desde `app.models`
- [ ] `course.average_rating` retorna `0.0` cuando no hay ratings
- [ ] `course.average_rating` retorna promedio correcto con ratings activos
- [ ] `course.total_ratings` excluye ratings con `deleted_at` no nulo
- [ ] `to_dict()` en `CourseRating` retorna fechas como strings ISO 8601
