# FASE 5 — Backend API Endpoints

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Rutas FastAPI (main.py)
**Estimación**: 1 hora
**Prerequisito**: FASE 3 y FASE 4 completadas

---

## Objetivo

Registrar y verificar los 6 endpoints de ratings con los status codes correctos, dependency injection y manejo de errores.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Backend/app/main.py` | Verificar/completar los 6 endpoints |

---

## Endpoints Requeridos

| Método | Ruta | Status OK | Status Error | Body In | Body Out |
|--------|------|-----------|-------------|---------|----------|
| `POST` | `/courses/{course_id}/ratings` | 201 | 404, 400 | `RatingRequest` | `RatingResponse` |
| `GET` | `/courses/{course_id}/ratings` | 200 | 404 | — | `List[RatingResponse]` |
| `GET` | `/courses/{course_id}/ratings/stats` | 200 | 404 | — | `RatingStatsResponse` |
| `GET` | `/courses/{course_id}/ratings/user/{user_id}` | 200 | 404 | — | `RatingResponse` |
| `PUT` | `/courses/{course_id}/ratings/{user_id}` | 200 | 404, 400 | `RatingRequest` | `RatingResponse` |
| `DELETE` | `/courses/{course_id}/ratings/{user_id}` | 204 | 404 | — | — |

---

## Patrón de Cada Endpoint

```python
@app.post("/courses/{course_id}/ratings", status_code=201, tags=["ratings"])
def add_course_rating(
    course_id: int,
    rating_data: RatingRequest,
    course_service: CourseService = Depends(get_course_service)
) -> RatingResponse:
    try:
        result = course_service.add_course_rating(...)
        return RatingResponse(**result)
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))
```

## Reglas de Manejo de Errores

- `"not found"` en el mensaje → `HTTPException(404)`
- Cualquier otro `ValueError` → `HTTPException(400)`
- DELETE exitoso → `Response(status_code=204)` (sin body)

## Dependency Injection

```python
def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    return CourseService(db)
```

---

## Verificación Manual

Con el servidor corriendo (`make start`), verificar en Swagger UI `http://localhost:8000/docs`:

- [ ] Los 6 endpoints aparecen bajo la sección `ratings`
- [ ] Schemas de request/response son correctos
- [ ] POST `/courses/1/ratings` con `{"user_id": 1, "rating": 5}` retorna 201
- [ ] DELETE `/courses/1/ratings/1` retorna 204
- [ ] GET `/courses/999/ratings` retorna 404

---

## Criterios de Aceptación

- [ ] 6 endpoints registrados y funcionales
- [ ] Status codes correctos en éxito y error
- [ ] Dependency injection usa `get_course_service`
- [ ] Tags `"ratings"` agrupan endpoints en Swagger
- [ ] Validación Pydantic rechaza inputs inválidos antes de llegar al servicio
