# FASE 3 — Backend Schemas Pydantic

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Validación de entrada/salida (Pydantic v2)
**Estimación**: 30 min
**Prerequisito**: FASE 2 completada

---

## Objetivo

Confirmar que todos los schemas Pydantic validan correctamente la entrada del cliente y serializan la salida del servicio, con configuración para lectura desde atributos ORM.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Backend/app/schemas/rating.py` | Verificar/completar los 4 schemas |

---

## Schemas Requeridos

### `RatingRequest`

```
user_id: int  →  Field(..., gt=0)
rating: int   →  Field(..., ge=1, le=5)
@field_validator('rating') — valida rango 1-5 explícitamente
```

### `RatingResponse`

```
id: int
course_id: int
user_id: int
rating: int
created_at: str
updated_at: str
Config: from_attributes = True
```

### `RatingStatsResponse`

```
average_rating: float  →  Field(..., ge=0.0, le=5.0)
total_ratings: int     →  Field(..., ge=0)
rating_distribution: Dict[int, int]  →  claves 1-5, valores = conteo
```

### `ErrorResponse`

```
detail: str
error_code: str | None = None
```

---

## Verificaciones Clave

- `RatingRequest(user_id=0, rating=3)` debe lanzar `ValidationError`
- `RatingRequest(user_id=1, rating=6)` debe lanzar `ValidationError`
- `RatingResponse(**rating_orm.to_dict())` debe construirse sin errores
- `RatingStatsResponse` debe usarse en el endpoint `/ratings/stats`

---

## Criterios de Aceptación

- [ ] `from app.schemas.rating import RatingRequest, RatingResponse, RatingStatsResponse` sin errores
- [ ] Validación rechaza `rating=0` y `rating=6`
- [ ] Validación rechaza `user_id=0` y `user_id` negativo
- [ ] `from_attributes = True` permite construir desde dict de ORM
