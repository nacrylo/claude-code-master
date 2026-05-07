# Plan Técnico: Implementación UI de Rating de Cursos — Frontend

**Versión**: 1.0
**Fecha**: 2026-05-04
**Estimación**: 6–8 horas
**Alcance**: Frontend exclusivamente (Backend ya implementado y completo)

---

## Contexto

El backend de ratings está completamente implementado (modelo, migraciones, service layer, endpoints, tests). Este plan cubre únicamente las 4 tareas pendientes en el frontend para conectar la UI interactiva con la API existente.

## Estado Actual del Frontend

### Ya implementado
- `StarRating` component — visualización SVG readonly (sin interactividad)
- `ratingsApi.ts` — cliente HTTP completo (CRUD + stats + user rating)
- Tipos en `rating.ts` — `CourseRating`, `RatingRequest`, `RatingStats`, `RatingState`, `ApiError`
- `Course` card — ya muestra `average_rating` con `StarRating` readonly
- Tipo `CourseDetail` — ya incluye `average_rating?` y `total_ratings?`

### Pendiente
- `StarRating` no tiene interactividad (no hay `onClick`, hover ni `onRatingChange`)
- `CourseDetail` no muestra ratings en absoluto
- No existe widget de calificación para el usuario
- No hay gestión de identidad de usuario (sin auth)

---

## Mapa de Dependencias

```
Tarea 1 (StarRating interactivo)  ──┐
                                    ├──→  Tarea 2 (RatingWidget)  ──→  Tarea 3 (CourseDetail)
Tarea 4 (useUserId hook)          ──┘
```

Las tareas 1 y 4 son independientes y pueden ejecutarse en paralelo.

---

## Tarea 1 — Hacer `StarRating` Interactivo

**Archivo:** `Frontend/src/components/StarRating/StarRating.tsx`
**Precondición:** ninguna

### 1.1 Agregar directiva y nueva prop

Agregar `'use client'` como primera línea. Extender la interfaz de props:

```typescript
interface StarRatingProps {
  rating: number;
  totalRatings?: number;
  showCount?: boolean;
  size?: 'small' | 'medium' | 'large';
  readonly?: boolean;
  className?: string;
  onRatingChange?: (rating: number) => void; // NUEVO
}
```

### 1.2 Agregar estado de hover

```typescript
const [hoveredRating, setHoveredRating] = useState<number | null>(null);
```

### 1.3 Rating efectivo de display

```typescript
const displayRating = readonly === false ? (hoveredRating ?? rating) : rating;
```

Usar `displayRating` (en lugar de `rating`) para calcular el estado de relleno de cada estrella. Esto permite preview visual al hacer hover sin modificar el rating guardado.

### 1.4 Event handlers por estrella

Cuando `readonly === false`, adjuntar en cada elemento de estrella:

```typescript
onClick={() => onRatingChange?.(starIndex)}
onMouseEnter={() => setHoveredRating(starIndex)}
onMouseLeave={() => setHoveredRating(null)}
onKeyDown={(e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    onRatingChange?.(starIndex);
  }
}}
```

Donde `starIndex` va de 1 a 5.

### 1.5 Atributos ARIA

Contenedor del grupo de estrellas en modo interactivo:
```typescript
role="radiogroup"
aria-label="Calificar curso"
```

Cada estrella en modo interactivo:
```typescript
role="radio"
aria-checked={starIndex === rating}
aria-label={`${starIndex} ${starIndex === 1 ? 'estrella' : 'estrellas'}`}
tabIndex={starIndex === (rating || 1) ? 0 : -1}
```

Navegación con flechas: capturar `ArrowLeft`/`ArrowRight` en el contenedor para mover el foco entre estrellas (patrón radio group nativo). Solo la estrella activa tiene `tabIndex={0}`; las demás `tabIndex={-1}`.

### 1.6 Cursor

```typescript
style={{ cursor: readonly === false ? 'pointer' : 'default' }}
```

### Consideraciones técnicas

- La lógica de estrellas parciales (decimales) es solo para modo readonly — el hover y click siempre producen enteros 1–5.
- Verificar si el SVG actual es uno por estrella o un único SVG: determina dónde van los event handlers.
- Los tests existentes no deben romperse: `readonly` sigue siendo el default, el comportamiento de display sin handlers no cambia.

### Validación — Tests a agregar en `StarRating.test.tsx`

- Click en estrella 3 → llama `onRatingChange(3)`
- Hover sobre estrella 4 → display muestra 4 estrellas llenas
- Mouse leave → display vuelve al rating original
- `readonly={true}` → `onRatingChange` nunca se llama aunque haya handler
- Enter/Space en estrella 2 → llama `onRatingChange(2)`
- `role="radiogroup"` presente en modo interactivo, ausente en readonly
- `aria-checked` refleja el rating seleccionado

---

## Tarea 4 — Hook `useUserId`

**Archivo nuevo:** `Frontend/src/hooks/useUserId.ts`
**Precondición:** ninguna

### Implementación

```typescript
'use client';

import { useState, useEffect } from 'react';

const USER_ID_KEY = 'platziflix_user_id';

function generateUserId(): number {
  return Math.floor(Math.random() * 2_000_000) + 1;
}

export function useUserId(): number | null {
  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem(USER_ID_KEY);
    if (stored) {
      setUserId(parseInt(stored, 10));
    } else {
      const newId = generateUserId();
      localStorage.setItem(USER_ID_KEY, String(newId));
      setUserId(newId);
    }
  }, []);

  return userId;
}
```

### Consideraciones técnicas

- Devuelve `null` durante SSR y el primer tick del cliente — los consumidores deben manejar `null` (no renderizar el widget hasta que `userId !== null`).
- Patrón `useState(null)` + `useEffect` es obligatorio en Next.js App Router para acceso a `localStorage` sin errores de hidratación.
- Rango `1–2_000_000` para caber en `INTEGER` de PostgreSQL (límite ~2.1B). No usar UUID convertido a número (desborda el tipo).
- No usar `UUID` directo: la API espera `user_id: number`.

### Validación — Tests en `Frontend/src/hooks/useUserId.test.ts`

- Mock de `localStorage` con `vi.stubGlobal`
- Primer render: genera y persiste un `userId` numérico
- Renders subsiguientes: recupera el mismo `userId` de `localStorage`
- El `userId` es un entero positivo en rango válido

---

## Tarea 2 — Crear `RatingWidget`

**Archivos nuevos:**
- `Frontend/src/components/RatingWidget/RatingWidget.tsx`
- `Frontend/src/components/RatingWidget/RatingWidget.module.scss`
- `Frontend/src/components/RatingWidget/RatingWidget.test.tsx`

**Precondición:** Tareas 1 y 4 completas

### Props

```typescript
interface RatingWidgetProps {
  courseId: number;
  userId: number;
}
```

### Estado interno

```typescript
const [currentRating, setCurrentRating] = useState<number | null>(null);
const [hasExistingRating, setHasExistingRating] = useState<boolean>(false);
const [state, setState] = useState<RatingState>('idle');
const [error, setError] = useState<string | null>(null);
```

### Carga inicial

```typescript
useEffect(() => {
  let cancelled = false;

  async function loadExistingRating() {
    setState('loading');
    try {
      const existing = await ratingsApi.getUserRating(courseId, userId);
      if (!cancelled) {
        if (existing) {
          setCurrentRating(existing.rating);
          setHasExistingRating(true);
        }
        setState('idle');
      }
    } catch {
      if (!cancelled) setState('idle');
    }
  }

  loadExistingRating();
  return () => { cancelled = true; };
}, [courseId, userId]);
```

`getUserRating` retorna `null` cuando el backend responde 204 (sin rating previo) — no es un error, es estado normal.

### Handler de selección

```typescript
async function handleRatingChange(newRating: number) {
  if (state === 'loading') return;

  setState('loading');
  setError(null);

  try {
    if (hasExistingRating) {
      await ratingsApi.updateRating(courseId, userId, { rating: newRating });
    } else {
      await ratingsApi.createRating(courseId, { user_id: userId, rating: newRating });
    }
    setCurrentRating(newRating);
    setHasExistingRating(true);
    setState('success');
  } catch {
    setState('error');
    setError('No se pudo guardar tu calificación. Intenta de nuevo.');
  }
}
```

### Auto-dismiss del mensaje de éxito

```typescript
useEffect(() => {
  if (state === 'success') {
    const timer = setTimeout(() => setState('idle'), 3000);
    return () => clearTimeout(timer);
  }
}, [state]);
```

### Renderizado

```tsx
<div className={styles.widget}>
  <StarRating
    rating={currentRating ?? 0}
    size="large"
    readonly={state === 'loading'}
    onRatingChange={handleRatingChange}
  />
  <div
    role="status"
    aria-live="polite"
    aria-atomic="true"
    className={styles.statusMessage}
  >
    {state === 'success' && '¡Gracias por tu calificación!'}
    {state === 'error' && error}
  </div>
</div>
```

**Notas de accesibilidad:**
- El `div[role="status"]` debe estar en el DOM desde el inicio (no montado condicionalmente) para que los lectores de pantalla lo registren.
- `aria-live="polite"` anuncia el mensaje sin interrumpir al usuario.
- Durante `state === 'loading'`, `readonly={true}` bloquea clics dobles.

### Validación — Tests en `RatingWidget.test.tsx`

- Mock de `ratingsApi` con `vi.mock`
- `getUserRating` retorna rating → se muestra seleccionado al montar
- `getUserRating` retorna `null` → `StarRating` muestra 0 estrellas
- Click sin rating previo → llama `createRating`
- Click con rating previo → llama `updateRating`
- Tras éxito → muestra mensaje de confirmación
- Tras error → muestra mensaje de error
- Durante `loading` → `StarRating` en modo readonly

---

## Tarea 3 — Actualizar `CourseDetail`

**Archivos:**
- Modificar: `Frontend/src/components/CourseDetail/CourseDetail.tsx`
- Modificar: `Frontend/src/components/CourseDetail/CourseDetail.module.scss`

**Precondición:** Tarea 2 completa

### Arquitectura: preservar SSR

Mantener el fetch de datos en el Server Component y extraer la parte interactiva a un Client Component:

```
CoursePage (Server Component — fetch de /courses/{slug})
  └── CourseDetailClient ('use client' — recibe course como prop)
        ├── StarRating readonly   →  promedio global (average_rating)
        └── RatingWidget          →  calificación del usuario
```

### 3.1 Crear `CourseDetailClient`

Renombrar o extraer el componente actual como Client Component:

```typescript
'use client';

import { useUserId } from '@/hooks/useUserId';
import { StarRating } from '@/components/StarRating/StarRating';
import { RatingWidget } from '@/components/RatingWidget/RatingWidget';

export const CourseDetailClient = ({ course }: { course: CourseDetail }) => {
  const userId = useUserId();
  // ... resto del JSX actual
};
```

### 3.2 Mostrar promedio global en el header

```tsx
{course.average_rating !== undefined && (
  <StarRating
    rating={course.average_rating}
    totalRatings={course.total_ratings}
    showCount={true}
    size="medium"
    readonly={true}
  />
)}
{course.average_rating === undefined && (
  <span className={styles.noRatings}>Sin calificaciones aún</span>
)}
```

### 3.3 Integrar `RatingWidget`

```tsx
{userId !== null && (
  <div className={styles.ratingSection}>
    <h3 className={styles.ratingSectionTitle}>¿Qué te pareció este curso?</h3>
    <RatingWidget courseId={course.id} userId={userId} />
  </div>
)}
```

Mientras `userId === null` (SSR o primer tick), no renderizar el widget para evitar errores de hidratación y layout shift. Considerar un placeholder del mismo alto para evitar CLS.

### Estructura visual del header

```
[Thumbnail]   [Título del curso]
              [Profesor]
              [Descripción]
              [StarRating readonly — promedio global]   ← nuevo
              [Duración · Clases]

[Sección: "¿Qué te pareció este curso?"]
  [RatingWidget — interactivo]                          ← nuevo

[Contenido del curso]
  [Lista de clases...]
```

---

## Checklist de Validación End-to-End

| Escenario | Qué verificar |
|---|---|
| Sin rating previo | Widget muestra 0 estrellas; promedio global visible si existe |
| Crear rating | Click en 4 estrellas → `POST /courses/{id}/ratings` en network tab → confirmación visual |
| Persistencia | Recargar página → widget carga las 4 estrellas desde el servidor |
| Actualizar rating | Cambiar a 2 estrellas → `PUT` en network (no `POST`) |
| Accesibilidad teclado | Tab llega al grupo, flechas navegan entre estrellas, Enter/Space confirma |
| SSR | `curl http://localhost:3000/course/{slug}` → HTML contiene promedio pero no el widget |
| Error de red | Backend apagado → mensaje de error sin romper el resto de la página |
| Nuevo dispositivo | `localStorage` vacío → genera nuevo `userId` → puede calificar correctamente |
