# FASE 8 — Frontend API Service

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Capa de acceso al API (cliente HTTP)
**Estimación**: 30 min
**Prerequisito**: FASE 7 completada

---

## Objetivo

Confirmar que `ratingsApi.ts` cubre todos los endpoints del backend con timeout, manejo graceful de 404, y tipado estricto.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Frontend/src/services/ratingsApi.ts` | Verificar/completar |

---

## Requisitos del Módulo

### Configuración base

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

### Helper de timeout (requerido)

```typescript
async function fetchWithTimeout(url: string, options?: RequestInit, timeoutMs = 10000): Promise<Response>
```

- Usa `AbortController` para cancelar tras `timeoutMs`
- Lanza `ApiError` con status 408 en timeout

### Handler de respuesta (requerido)

```typescript
async function handleApiResponse<T>(response: Response): Promise<T>
```

- Lanza `ApiError(message, response.status)` si `!response.ok`
- Parsea JSON y retorna tipado como `T`

### Funciones exportadas

| Función | Endpoint | Comportamiento especial |
|---------|----------|------------------------|
| `getRatingStats(courseId)` | `GET /courses/{id}/ratings/stats` | — |
| `getCourseRatings(courseId)` | `GET /courses/{id}/ratings` | — |
| `getUserRating(courseId, userId)` | `GET /courses/{id}/ratings/user/{uid}` | Retorna `null` en 404, no lanza |
| `createRating(courseId, request)` | `POST /courses/{id}/ratings` | — |
| `updateRating(courseId, userId, request)` | `PUT /courses/{id}/ratings/{uid}` | — |
| `deleteRating(courseId, userId)` | `DELETE /courses/{id}/ratings/{uid}` | Retorna `void` (status 204) |

### Export

```typescript
export const ratingsApi = {
  getRatingStats,
  getCourseRatings,
  getUserRating,
  createRating,
  updateRating,
  deleteRating,
} as const;

export { ApiError };
```

---

## Reglas Críticas

- `getUserRating` **no lanza** en 404 — retorna `null`. Es el único endpoint con este comportamiento
- `deleteRating` no intenta parsear body (respuesta 204 no tiene body)
- Todas las funciones son `async` y retornan `Promise<T>`
- No usar `fetch` directamente — siempre pasar por `fetchWithTimeout`

---

## Criterios de Aceptación

- [ ] `import { ratingsApi } from '@/services/ratingsApi'` sin errores de tipo
- [ ] `getUserRating` retorna `null` cuando el API devuelve 404
- [ ] Timeout de 10s activo en todas las llamadas
- [ ] `ApiError` propagado correctamente en respuestas no-2xx (excepto 404 en getUserRating)
- [ ] `deleteRating` no falla al parsear respuesta 204 vacía
