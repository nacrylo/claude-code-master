# FASE 12 — Frontend Tests

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Tests frontend (Vitest + React Testing Library)
**Estimación**: 1 hora
**Prerequisito**: FASE 9, FASE 10 y FASE 11 completadas

---

## Objetivo

Verificar cobertura de los componentes de rating: `StarRating` (rendering y accesibilidad), `Course` card (integración condicional), y `RatingWidget` (flujo de submission con API mockeada).

---

## Archivos Involucrados

| Archivo | Componente cubierto |
|---------|-------------------|
| `Frontend/src/components/StarRating/__tests__/StarRating.test.tsx` | `StarRating` |
| `Frontend/src/components/Course/__test__/Course.test.tsx` | `Course` card |
| `Frontend/src/components/CourseDetail/RatingWidget.test.tsx` | `RatingWidget` |

---

## Tests de `StarRating`

**Casos requeridos**:

| Test | Assertion |
|------|-----------|
| `renders 5 stars` | 5 elementos SVG/star en el DOM |
| `readonly has correct aria-label` | `getByRole('img')` con `aria-label="Rating: 3.0 out of 5 stars"` |
| `showCount renders total` | `getByText('(42)')` visible |
| `size="small" applies class` | `container.firstChild` tiene clase `small` |
| `size="large" applies class` | `container.firstChild` tiene clase `large` |
| `onRatingChange called on click` | `fireEvent.click(star)` → callback con valor correcto |
| `onRatingChange not called if readonly` | `fireEvent.click(star)` → callback no llamado |

**Setup**:

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { StarRating } from '../StarRating';
```

---

## Tests de `Course` card

**Casos requeridos**:

| Test | Assertion |
|------|-----------|
| `shows rating when average_rating defined` | `StarRating` aparece en el DOM |
| `hides rating when average_rating undefined` | sección de rating no renderizada |
| `passes correct props to StarRating` | `readonly={true}`, `size="small"` |

---

## Tests de `RatingWidget`

**Setup de mock**:

```typescript
vi.mock('@/services/ratingsApi', () => ({
  ratingsApi: {
    getUserRating: vi.fn().mockResolvedValue(null),
    createRating: vi.fn().mockResolvedValue({ id: 1, rating: 4, ... }),
    updateRating: vi.fn().mockResolvedValue({ id: 1, rating: 5, ... }),
  }
}));
```

**Casos requeridos**:

| Test | Assertion |
|------|-----------|
| `shows loading state on submit` | Texto "Guardando..." aparece durante la llamada |
| `shows success after rating` | Texto "¡Gracias por tu calificación!" aparece |
| `shows error on API failure` | Mock rechaza → mensaje de error visible |
| `disables stars during loading` | `StarRating` recibe `readonly={true}` mientras carga |
| `calls createRating when no previous rating` | `getUserRating` retorna `null` → `createRating` llamado |
| `calls updateRating when rating exists` | `getUserRating` retorna rating → `updateRating` llamado |

---

## Comandos de Ejecución

```bash
cd Frontend

# Todos los tests
npx vitest run

# Solo StarRating
npx vitest run src/components/StarRating/__tests__/StarRating.test.tsx

# Solo RatingWidget
npx vitest run src/components/CourseDetail/RatingWidget.test.tsx

# Con cobertura
npx vitest run --coverage
```

---

## Criterios de Aceptación

- [ ] Todos los tests pasan sin errores ni warnings
- [ ] No se hacen llamadas HTTP reales en ningún test (todo mockeado)
- [ ] `cleanup()` del setup.ts limpia el DOM entre tests
- [ ] Tests de accesibilidad usan queries por `role` (no por clase o id)
- [ ] `vi.mock` limpia mocks entre tests si se usa `beforeEach`
