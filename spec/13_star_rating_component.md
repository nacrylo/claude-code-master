# FASE 9 — Componente StarRating

**Versión**: 1.0
**Fecha**: 2026-05-04
**Alcance**: Componente React reutilizable (readonly + interactivo)
**Estimación**: 1.5 horas
**Prerequisito**: FASE 7 completada

---

## Objetivo

Completar `StarRating` para que soporte dos modos: readonly (visualización) e interactivo (permite al usuario seleccionar un rating). El componente debe ser accesible y responsive a las 3 variantes de tamaño.

---

## Archivos Involucrados

| Archivo | Acción |
|---------|--------|
| `Frontend/src/components/StarRating/StarRating.tsx` | Verificar/completar |
| `Frontend/src/components/StarRating/StarRating.module.scss` | Verificar estilos de los 3 tamaños |

---

## Interface de Props Requerida

```typescript
interface StarRatingProps {
  rating: number;              // 0.0–5.0
  totalRatings?: number;       // mostrado entre paréntesis si showCount=true
  showCount?: boolean;         // default: false
  size?: 'small' | 'medium' | 'large';  // default: 'medium'
  readonly?: boolean;          // default: false — si true, sin interactividad
  className?: string;
  onRatingChange?: (rating: number) => void;  // solo se llama si !readonly
}
```

---

## Comportamiento Requerido

### Modo readonly (`readonly={true}`)

- Renderiza estrellas SVG con fill proporcional a `rating`
- `role="img"` con `aria-label="Rating: {rating} out of 5 stars"`
- Sin handlers de mouse/keyboard para interactividad
- Muestra `({totalRatings})` al lado si `showCount={true}`

### Modo interactivo (`readonly={false}` o sin prop)

- `'use client'` como primera línea del archivo
- Estado local `hoverRating: number` para efecto hover
- `onClick` en cada estrella llama `onRatingChange(starIndex)`
- `onMouseEnter`/`onMouseLeave` actualiza `hoverRating`
- Keyboard: `onKeyDown` en Enter/Space llama `onRatingChange`
- `tabIndex={0}` y `role="radio"` por estrella para navegación con teclado

### Variantes de tamaño

| Size | Clase CSS | Tamaño estrella sugerido |
|------|-----------|--------------------------|
| `small` | `.small` | 16px |
| `medium` | `.medium` | 24px |
| `large` | `.large` | 36px |

---

## SCSS — Verificaciones

- Importa variables via `@import '../../styles/vars.scss'` (o auto-prepend de next.config.ts)
- Clase `.small`, `.medium`, `.large` aplicadas al contenedor raíz
- Transición en estrellas: `transition: transform 0.1s, opacity 0.1s`
- Color activo: `color('primary')` (`#ff2d2d`)
- Color inactivo: `color('light-gray')`

---

## Criterios de Aceptación

- [ ] Componente renderiza 5 estrellas para cualquier `rating` entre 0 y 5
- [ ] `role="img"` con aria-label correcto en modo readonly
- [ ] `onRatingChange` no se llama si `readonly={true}`
- [ ] Hover cambia visualización antes de click en modo interactivo
- [ ] `size="small"` aplica clase `.small` al contenedor raíz
- [ ] `showCount={true}` con `totalRatings={42}` muestra texto `(42)`
