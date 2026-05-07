# FASE 11 — Integración en CourseDetail con Rating Interactivo

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Página de detalle de curso (rating interactivo)
**Estimación**: 2 horas
**Prerequisito**: FASE 8 y FASE 9 completadas

---

## Objetivo

Permitir al usuario calificar un curso desde la página de detalle. Esta es la fase con mayor trabajo nuevo: requiere convertir parte de la UI a Client Component y gestionar identidad de usuario sin auth.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Frontend/src/components/CourseDetail/CourseDetail.tsx` | Separar en Server + Client Component |
| `Frontend/src/app/course/[slug]/page.tsx` | Verificar que pasa `average_rating` y `total_ratings` |

---

## Decisión de Arquitectura

La página `[slug]/page.tsx` es Server Component (fetch de datos). `CourseDetail.tsx` tiene partes estáticas (Server) y partes interactivas (Client). La solución es:

```
page.tsx (Server Component)
  └── CourseDetailComponent (Server Component — recibe course, renderiza info estática)
        └── RatingWidget (Client Component — 'use client', maneja estado de rating)
```

Crear `RatingWidget` como componente separado en lugar de convertir todo `CourseDetail` a Client.

---

## Nuevo Componente: `RatingWidget`

**Archivo**: `Frontend/src/components/CourseDetail/RatingWidget.tsx`

```
'use client'

Props:
  courseId: number
  initialAverageRating: number
  initialTotalRatings: number

Estado interno:
  userRating: number | null     — rating que el usuario ha seleccionado/enviado
  ratingState: RatingState      — 'idle' | 'loading' | 'success' | 'error'
  hoverRating: number           — para preview antes de click
  errorMessage: string | null

Identidad de usuario (sin auth):
  userId: number — hardcodeado como 1 para el stub (documentar que se reemplaza con auth)
```

### Flujo de `handleRatingSubmit(newRating: number)`

1. Setear `ratingState = 'loading'`
2. Llamar `ratingsApi.getUserRating(courseId, userId)` para saber si ya existe
3. Si existe → `ratingsApi.updateRating(...)`, si no → `ratingsApi.createRating(...)`
4. En éxito → `userRating = newRating`, `ratingState = 'success'`
5. En error → `ratingState = 'error'`, mostrar `errorMessage`

### JSX del `RatingWidget`

```tsx
<section>
  <h3>Califica este curso</h3>
  <StarRating
    rating={userRating ?? 0}
    onRatingChange={handleRatingSubmit}
    size="large"
    readonly={ratingState === 'loading'}
  />
  {ratingState === 'loading' && <span>Guardando...</span>}
  {ratingState === 'success' && <span>¡Gracias por tu calificación!</span>}
  {ratingState === 'error' && <span>{errorMessage}</span>}

  <StarRating
    rating={initialAverageRating}
    totalRatings={initialTotalRatings}
    showCount={true}
    readonly={true}
  />
</section>
```

---

## `CourseDetail.tsx` — Cambios

Agregar `<RatingWidget>` al final de la sección principal:

```tsx
<RatingWidget
  courseId={course.id}
  initialAverageRating={course.average_rating ?? 0}
  initialTotalRatings={course.total_ratings ?? 0}
/>
```

---

## `page.tsx` (Course Detail) — Verificación

```typescript
const courseData = await getCourseData(params.slug);
// courseData.average_rating y courseData.total_ratings deben existir
// Verificar que GET /courses/{slug} los retorna
```

---

## Criterios de Aceptación

- [ ] `page.tsx` sigue siendo Server Component (sin `'use client'`)
- [ ] `RatingWidget` tiene `'use client'` y gestiona su propio estado
- [ ] Click en estrella llama al API y actualiza el estado
- [ ] Estado `loading` deshabilita interacción mientras se envía
- [ ] Estado `success` muestra confirmación al usuario
- [ ] Estado `error` muestra mensaje de error sin crashear
- [ ] Rating promedio del curso se muestra debajo del widget del usuario
- [ ] `userId` stub documentado con comentario indicando futura integración de auth
