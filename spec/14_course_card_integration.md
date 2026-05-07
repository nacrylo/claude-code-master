# FASE 10 — Integración en Course Card

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Componente Course (card del listado)
**Estimación**: 30 min
**Prerequisito**: FASE 9 completada

---

## Objetivo

Mostrar el rating promedio del curso (readonly) en cada card del listado de cursos, conectado con los datos que retorna `GET /courses`.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Frontend/src/components/Course/Course.tsx` | Verificar integración de StarRating |
| `Frontend/src/app/page.tsx` | Verificar que pasa `average_rating` y `total_ratings` |

---

## `Course.tsx` — Requisitos

### Props

```typescript
type CourseProps = Omit<CourseType, "slug">;
// Incluye: id, name, description, thumbnail, average_rating?, total_ratings?
```

### Renderizado de rating (condicional)

```tsx
{typeof average_rating === 'number' && (
  <div className={styles.ratingContainer}>
    <StarRating
      rating={average_rating}
      totalRatings={total_ratings}
      showCount={true}
      size="small"
      readonly={true}
    />
  </div>
)}
```

- La condición `typeof average_rating === 'number'` evita renderizar si el campo es `undefined`
- `total_ratings` puede ser `undefined` — `StarRating` debe manejarlo (default 0)
- Posición: debajo de la descripción, antes del borde inferior de la card

### SCSS

- Clase `.ratingContainer` en `Course.module.scss`
- `margin-top: 8px` para separar de la descripción
- No debe romper el layout actual de la card

---

## `page.tsx` (Home) — Verificación

`GET /courses` debe retornar `average_rating` y `total_ratings` para que lleguen al componente:

```typescript
// El fetch ya existe, verificar que los campos llegan:
const courses = await getCourses(); // Course[]
// courses[0].average_rating debe estar disponible si el curso tiene ratings
```

Si el backend no incluye estos campos en `GET /courses`, coordinar con FASE 4 para que `get_all_courses()` los incluya.

---

## Criterios de Aceptación

- [ ] Card muestra estrellas si `average_rating` está definido
- [ ] Card NO muestra sección de rating si `average_rating` es `undefined`
- [ ] `size="small"` y `readonly={true}` siempre en la card
- [ ] No hay error de TypeScript en `CourseProps`
- [ ] Layout de la card no se rompe con o sin rating
