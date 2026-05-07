# FASE 6 — Backend Tests

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Tests backend (unit + integración + DB constraints)
**Estimación**: 1.5 horas
**Prerequisito**: FASE 4 y FASE 5 completadas

---

## Objetivo

Verificar cobertura completa con las 3 capas de testing del backend. Cada capa testea en aislamiento una responsabilidad diferente.

---

## Archivos Involucrados

| Archivo | Tipo | Descripción |
|---------|------|-------------|
| `Backend/app/tests/test_course_rating_service.py` | Unit | Servicio con DB mockeada |
| `Backend/app/tests/test_main.py` | Integración | HTTP con servicio mockeado |
| `Backend/app/tests/test_rating_db_constraints.py` | DB | Constraints en DB real |

---

## Capa 1 — Unit Tests (servicio, DB mockeada)

**Archivo**: `test_course_rating_service.py`

**Fixtures**:
```python
@pytest.fixture
def mock_db(): return Mock()

@pytest.fixture
def service(mock_db): return CourseService(db=mock_db)
```

**Casos requeridos**:

| Test | Descripción |
|------|-------------|
| `test_get_ratings_returns_list` | Mock retorna 2 ratings → resultado tiene 2 elementos |
| `test_get_ratings_empty_course` | Mock retorna `[]` → resultado es lista vacía |
| `test_add_rating_creates_new` | No existe rating previo → crea y retorna dict |
| `test_add_rating_updates_existing` | Existe rating previo → actualiza, no duplica |
| `test_update_rating_not_found` | Mock retorna `None` → `ValueError` |
| `test_delete_rating_sets_deleted_at` | Soft delete → `deleted_at` se asigna |
| `test_get_user_rating_returns_none` | No existe → retorna `None` (no lanza) |
| `test_stats_uses_sql_aggregation` | `func.avg` llamado, no cálculo Python |

---

## Capa 2 — Integration Tests (HTTP, servicio mockeado)

**Archivo**: `test_main.py` (sección ratings)

**Fixture**:
```python
@pytest.fixture
def client(mock_service):
    app.dependency_overrides[get_course_service] = lambda: mock_service
    yield TestClient(app)
    app.dependency_overrides.clear()
```

**Casos requeridos**:

| Test | Status esperado |
|------|----------------|
| `test_post_rating_success` | 201, body con `id`, `rating`, `course_id` |
| `test_post_rating_invalid_body` | 422 (Pydantic validation) |
| `test_post_rating_course_not_found` | 404 |
| `test_get_ratings_success` | 200, lista |
| `test_get_stats_success` | 200, `average_rating`, `total_ratings`, `rating_distribution` |
| `test_put_rating_success` | 200 |
| `test_delete_rating_success` | 204, sin body |
| `test_delete_rating_not_found` | 404 |

---

## Capa 3 — DB Constraint Tests (DB real)

**Archivo**: `test_rating_db_constraints.py`

**Fixture**:
```python
@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
```

**Casos requeridos**:

| Test | Constraint verificado |
|------|----------------------|
| `test_rating_below_min` | CHECK rechaza `rating=0` con `IntegrityError` |
| `test_rating_above_max` | CHECK rechaza `rating=6` con `IntegrityError` |
| `test_unique_active_rating` | UNIQUE impide 2 ratings activos mismo user+curso |
| `test_soft_delete_allows_rerate` | Tras soft delete, el usuario puede volver a calificar |
| `test_fk_course_required` | FK rechaza `course_id` inexistente |

---

## Comandos de Ejecución

```bash
# Todos los tests
docker-compose exec api bash -c "cd /app && uv run pytest"

# Solo ratings
docker-compose exec api bash -c "cd /app && uv run pytest app/tests/test_course_rating_service.py app/tests/test_rating_db_constraints.py -v"

# Un test específico
docker-compose exec api bash -c "cd /app && uv run pytest -k test_add_rating_creates_new"
```

---

## Criterios de Aceptación

- [ ] Todos los tests pasan (`pytest` sin errores)
- [ ] No hay warnings de deprecación en SQLAlchemy
- [ ] `dependency_overrides` se limpia en teardown (sin contaminación entre tests)
- [ ] Los constraint tests usan `SessionLocal` real (no mock)
