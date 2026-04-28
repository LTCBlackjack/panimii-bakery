# Layout Base — Panimii Bakery

## Resultado Visual

````carousel
![Vista desktop: navbar sticky, secciones alternas surface/neutral, footer negro](C:\Users\leona\.gemini\antigravity\brain\e4ecbda2-7da7-49ea-872e-f44ace31517a\artifacts\desktop_layout.png)
<!-- slide -->
![Vista móvil (375px): menú hamburguesa, secciones apiladas, footer responsive](C:\Users\leona\.gemini\antigravity\brain\e4ecbda2-7da7-49ea-872e-f44ace31517a\artifacts\mobile_layout.png)
````

---

## Mapeo DESIGN.md → Tailwind

Cada token se configuró en `tailwind.config` dentro del `<script>` del `base.html`:

| Token DESIGN.md | Valor | Clase Tailwind resultante |
|---|---|---|
| `colors.primary` | `#000000` | `text-primary`, `bg-primary` |
| `colors.secondary` | `#4A4A4A` | `text-secondary` |
| `colors.neutral` | `#F9F9F9` | `bg-neutral`, `border-neutral` |
| `colors.surface` | `#FFFFFF` | `bg-surface` |
| `typography.h1.fontFamily` | Playfair Display | `font-serif` |
| `typography.h1.fontSize` | 48px / 700 | `text-display` |
| `typography.body.fontFamily` | Inter | `font-sans` |
| `typography.body.fontSize` | 16px / 1.6 | `text-body` |
| `rounded.sm` | 0px | `rounded-editorial-none` |
| `rounded.md` | 4px | `rounded-editorial-sm` |
| `spacing.section` | 80px | `py-section` |
| `spacing.container` | 24px | `px-container` |

## Clases Utilitarias Creadas

```css
.section-surface  →  bg-surface + py-section    /* Fondo blanco */
.section-neutral  →  bg-neutral + py-section    /* Fondo gris alterno */
.btn-editorial    →  bg-primary + text-white + rounded-editorial-sm + tracking-wider
```

> [!TIP]
> Para implementar el patrón de secciones alternas, simplemente alterna `section-surface` y `section-neutral` en cada `<section>` dentro del bloque `{% block content %}`.

---

## Archivos Creados / Modificados

| Archivo | Acción |
|---|---|
| [base.html](file:///c:/Users/leona/panimii-bakery/templates/base.html) | **Creado** — Layout base con Tailwind, Google Fonts, navbar, footer |
| [home.html](file:///c:/Users/leona/panimii-bakery/templates/home.html) | **Creado** — Página demo con secciones alternas |
| [settings.py](file:///c:/Users/leona/panimii-bakery/panimii/settings.py) | **Modificado** — TEMPLATES DIRS apunta a `templates/` |
| [urls.py](file:///c:/Users/leona/panimii-bakery/panimii/urls.py) | **Modificado** — Ruta raíz `/` para previsualizar |
