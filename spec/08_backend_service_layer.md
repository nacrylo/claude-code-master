# FASE 4 — Backend Service Layer

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Lógica de negocio (CourseService)
**Estimación**: 1.5 horas
**Prerequisito**: FASE 2 y FASE 3 completadas

---

## Objetivo

Verificar y completar los 6 métodos de rating en `CourseService`, asegurando manejo correcto de soft deletes, upsert, SQL aggregation y errores.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Backend/app/services/course_service.py` | Verificar/completar los 6 métodos |

---

## Métodos Requeridos

### `get_course_ratings(course_id: int) → List[Dict]`

- Query con `.filter(CourseRating.course_id == course_id, CourseRating.deleted_at.is_(None))`
- Retorna lista de `to_dict()` (vacía si no hay ratings, no lanza)
- Lanza `ValueError("Course with id {id} not found")` si el curso no existe

### `add_course_rating(course_id: int, user_id: int, rating: int) → Dict`

- Verifica curso existe (activo, `deleted_at is None`)
- Busca rating existente del mismo user+curso con `deleted_at is None`
- **Upsert**: si existe → actualiza `rating` y `updated_at = datetime.utcnow()`; si no → crea nuevo
- Hace `db.commit()` y `db.refresh()` antes de retornar
- Lanza `ValueError` para curso no encontrado

### `update_course_rating(course_id: int, user_id: int, rating: int) → Dict`

- Busca rating activo; lanza `ValueError("Rating not found")` si no existe
- Actualiza `rating` y `updated_at = datetime.utcnow()`
- `db.commit()` → retorna `to_dict()`

### `delete_course_rating(course_id: int, user_id: int) → bool`

- Soft delete: `rating.deleted_at = datetime.utcnow()`
- `db.commit()` → retorna `True`
- Lanza `ValueError("Rating not found")` si no existe rating activo

### `get_user_course_rating(course_id: int, user_id: int) → Optional[Dict]`

- Retorna `None` si no existe (nunca lanza en caso 404)
- Filtra `deleted_at.is_(None)`

### `get_course_rating_stats(course_id: int) → Dict`

- Usa `func.avg()` y `func.count()` en SQL (no Python-level)
- Calcula `rating_distribution` como `{1: n, 2: n, 3: n, 4: n, 5: n}`
- Retorna `{"average_rating": float, "total_ratings": int, "rating_distribution": dict}`
- `average_rating` redondeado a 2 decimales; `0.0` si no hay ratings

---

## Reglas Invariantes

- Toda query filtra `deleted_at.is_(None)` en CourseRating y Course
- El servicio nunca hace `db.rollback()` — lo hace el contexto de la request
- Errores de negocio → `ValueError`, nunca `HTTPException` (eso lo hace la ruta)
- Retorna `dict`, no instancias ORM

---

## Criterios de Aceptación

- [ ] `add_course_rating` hace upsert (no duplica ratings)
- [ ] `delete_course_rating` no borra físicamente — solo setea `deleted_at`
- [ ] `get_course_rating_stats` consulta SQL con `func.avg` / `func.count`
- [ ] Todos los métodos retornan `dict`, no modelos SQLAlchemy
- [ ] `get_user_course_rating` retorna `None` sin lanzar cuando no hay rating
