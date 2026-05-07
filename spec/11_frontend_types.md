# FASE 7 — Frontend Types

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: TypeScript type definitions
**Estimación**: 20 min
**Prerequisito**: FASE 5 completada (API endpoints definidos)

---

## Objetivo

Confirmar que los tipos TypeScript reflejan exactamente los contratos del API backend — mismos nombres de campo (snake_case del JSON), mismas opcionalidades.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Frontend/src/types/index.ts` | Verificar campos de rating en `Course` y `CourseDetail` |
| `Frontend/src/types/rating.ts` | Verificar todos los tipos e interfaces de rating |

---

## `index.ts` — Requisitos sobre `Course`

```typescript
export interface Course {
  id: number;
  name: string;
  description: string;
  thumbnail: string;
  slug: string;
  average_rating?: number;  // snake_case — coincide con JSON del API
  total_ratings?: number;   // snake_case — coincide con JSON del API
}
```

`CourseDetail extends Course` debe heredar los campos opcionales de rating.

---

## `rating.ts` — Requisitos

### Interfaces de datos

```typescript
CourseRating {
  id: number;
  course_id: number;
  user_id: number;
  rating: number;       // 1-5
  created_at: string;   // ISO 8601
  updated_at: string;
}

RatingRequest {
  user_id: number;
  rating: number;
}

RatingStats {
  average_rating: number;
  total_ratings: number;
}
```

### Type alias de estado

```typescript
type RatingState = 'idle' | 'loading' | 'success' | 'error';
```

### Type guards (funciones de runtime)

```typescript
isValidRating(rating: number): rating is number   // verifica 1 <= rating <= 5
isCourseRating(obj: unknown): obj is CourseRating // verifica shape del objeto
isRatingStats(obj: unknown): obj is RatingStats   // verifica shape del objeto
```

### Clase de error

```typescript
class ApiError extends Error {
  constructor(message: string, public status: number, public code?: string, public details?: Record<string, unknown>)
}
```

---

## Verificaciones Clave

- `average_rating` y `total_ratings` en `Course` deben ser **opcionales** (`?`) porque `GET /courses` puede no incluirlos para cursos sin ratings
- Los campos de `CourseRating` deben ser `snake_case` para coincidir con el JSON que devuelve FastAPI
- `RatingState` como union type literal (no enum) para evitar overhead en bundle

---

## Criterios de Aceptación

- [ ] `npx tsc --noEmit` sin errores relacionados a tipos de rating
- [ ] `Course.average_rating` es opcional y acepta `undefined`
- [ ] `ApiError` puede instanciarse con `new ApiError("msg", 404)`
- [ ] Type guards retornan boolean y actúan como narrowing guards de TypeScript
