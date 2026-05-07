# FASE 1 — Database Layer

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Base de datos (PostgreSQL + Alembic)
**Estimación**: 30 min
**Prerequisito**: Docker corriendo (`make start`), leer `00_sistema_ratings_cursos.md`

---

## Objetivo

Aplicar el schema de `course_ratings` en la base de datos y verificar que constraints e índices estén activos.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Backend/app/alembic/versions/0e3a8766f785_add_course_ratings_table.py` | Verificar — ya existe |
| `Backend/` | Ejecutar `make migrate` |

---

## Checklist de Verificación

### Migración existente debe contener

- `CREATE TABLE course_ratings` con columnas: `id`, `course_id`, `user_id`, `rating`, `created_at`, `updated_at`, `deleted_at`
- `ForeignKeyConstraint(['course_id'], ['courses.id'])`
- `CheckConstraint('rating >= 1 AND rating <= 5', name='ck_course_ratings_rating_range')`
- `UniqueConstraint('course_id', 'user_id', 'deleted_at', name='uq_course_ratings_user_course_deleted')`
- `downgrade()` que elimina índices y tabla en orden inverso

### Índices requeridos

- `ix_course_ratings_id`
- `ix_course_ratings_course_id`
- `ix_course_ratings_user_id`

---

## Comandos de Ejecución

```bash
cd Backend
make migrate
```

---

## Criterios de Aceptación

- [ ] `make migrate` ejecuta sin errores
- [ ] Tabla `course_ratings` visible en la DB con `\d course_ratings` (psql)
- [ ] CHECK constraint rechaza `rating = 0` y `rating = 6`
- [ ] UNIQUE constraint impide dos ratings activos del mismo usuario para el mismo curso
