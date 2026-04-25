# ICHIBOT ROBOTICS — Static Website Implementation Plan

> **Target**: Production-ready static site (HTML/CSS/JS only)  
> **Hosting**: cPanel shared hosting — zero build tools, zero Node.js  
> **Last updated**: 2026-04-25

---

## 1. File Structure

```
/
├── index.html
├── products.html
├── achievements.html
├── community.html
├── about.html
├── css/
│   ├── global.css       ← variables, reset, typography, glass utilities
│   ├── components.css   ← cards, buttons, nav, footer
│   └── animations.css   ← keyframes, scroll-triggered animations
├── js/
│   ├── main.js          ← nav, scroll, counter, world map, intersection observers
│   └── products.js      ← filter tab logic for products.html
└── assets/
    └── (intentionally empty — all images via URL)
```

---

## 2. Design System (global.css)

### CSS Custom Properties
```
--bg-primary:       #0a0a0a      (near-black base)
--bg-secondary:     #111111      (cards, elevated surfaces)
--glass-bg:         rgba(255,255,255,0.04)
--glass-border:     rgba(255,255,255,0.09)
--glass-border-red: rgba(220,30,30,0.55)
--accent-red:       #dc1e1e      (CTA, stats, logo mark, 1 hero word)
--accent-red-light: #ff3333
--text-primary:     #f0ece4      (warm-white / platinum)
--text-secondary:   #9a9590
--text-muted:       #5a5550
--blur-amount:      16px
--blur-amount-lg:   24px
--radius-card:      16px
--radius-btn:       8px
--transition-base:  0.28s cubic-bezier(0.4, 0, 0.2, 1)
```

### Fonts (Google Fonts CDN)
- **Display / Hero**: `Rajdhani` (weights 500, 600, 700) — technical, geometric
- **Body**: `DM Sans` (weights 400, 500) — clean, readable

### Background Texture
- Faint SVG noise grain as `::before` pseudo-element on `body`
- Opacity: 4% — depth without distraction
- Implemented as inline SVG data URI (no external file needed)

### Glass Card Utility Class
```css
.glass-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(var(--blur-amount));
  -webkit-backdrop-filter: blur(var(--blur-amount));
  border-radius: var(--radius-card);
  box-shadow: 0 0 0 1px rgba(255,255,255,0.03) inset,
              0 4px 32px rgba(0,0,0,0.4);
}
.glass-card:hover {
  border-color: var(--glass-border-red);
  box-shadow: 0 0 24px rgba(220,30,30,0.15),
              0 8px 48px rgba(0,0,0,0.5);
  transform: translateY(-4px);
}
```

---

## 3. Component Strategy (components.css)

| Component         | Key Details |
|-------------------|-------------|
| **Nav**           | Fixed, glassmorphism bar. Logo left, links center, WA CTA right. Hamburger on mobile (<768px). Active page link has red bottom underline. |
| **Buttons**       | `.btn-red` (filled, red gradient, white text). `.btn-ghost` (transparent, white border, white text). Both have hover lift + glow. |
| **Product Card**  | `.glass-card` base. Image top, badge overlay, content bottom. Strikethrough price. 2 buttons. |
| **Achievement Card** | Image full-width top, tag badge, title, date, description. |
| **Stats Bar**     | Horizontal flex strip. `.glass-card` styling. Counter `<span>` per stat. |
| **Footer**        | 4-column grid (logo+tagline, pages, products, contact). Marketplace icons row. |
| **Filter Tabs**   | Pill-style tabs. Active = red underline + brighter text. JS toggles `.active` class. |

---

## 4. Animation Plan (animations.css + main.js)

### CSS Keyframes
- `@keyframes fadeInUp` — elements slide up + fade on load
- `@keyframes pulsingDot` — map destination dots (scale + opacity loop)
- `@keyframes arcDraw` — `stroke-dashoffset` from `100%` to `0`
- `@keyframes glowPulse` — Yogyakarta origin dot radial glow
- `@keyframes grainShift` — slow noise texture subtle pan

### Scroll-triggered (IntersectionObserver in main.js)
- **Stats counters**: Observe `.stats-bar`. When visible → animate `0 → N` over 2s using `requestAnimationFrame`
- **Section reveals**: `.reveal-on-scroll` elements get `.visible` class → triggers `fadeInUp`
- **World map arcs**: Observe `.map-section`. When visible → start arc draw sequence (staggered 150ms apart)
- **Product cards**: staggered `animation-delay` on each card child

### World Map — Pure SVG Approach
- Simplified flat Mercator SVG path outlines (embedded inline)
- Countries: dark fills `#111`, border stroke `rgba(255,255,255,0.06)`
- Origin: Yogyakarta dot — large pulsing red circle
- Destination dots: 17 lat/lon coordinates pre-mapped to SVG x/y
- Arcs: `<path>` with `stroke-dasharray` + animated `stroke-dashoffset`
- Arc gradient: CSS `linearGradient` red → transparent
- JS triggers class on SVG container → CSS animation fires via class

---

## 5. Page-by-Page Build Plan

### Page 1: index.html (Home)
1. `<section class="hero">` — full-vh, headline with `<span class="red">Menang</span>`, subtext, 2 CTAs, animated SVG track background
2. `<section class="stats-bar">` — 4 counter stats in glass strip
3. `<section class="map-section">` — world export map (inline SVG + JS)
4. `<section class="featured-products">` — 4 glass product cards grid
5. `<section class="achievements-feed">` — 3-col card grid (3 placeholder cards)
6. `<section class="community-preview">` — photo wall + social links

### Page 2: products.html
- Filter tab bar (6 categories)
- Full catalog: 11 products, all with correct data
- `data-category` attribute on each card
- JS: `products.js` handles filter logic

### Page 3: achievements.html
- Filter bar: 5 categories
- Masonry-like card grid (CSS columns)
- 12+ placeholder achievement cards across all categories

### Page 4: community.html
- Hall of Champions (6 placeholder team cards)
- Submission form → WhatsApp pre-fill on submit
- Community ethos section
- Social links

### Page 5: about.html
- Brand story section
- Mission + "Mengapa Ichibot?" (4 pillars)
- Team section (4 placeholder cards)
- Store/marketplace section

---

## 6. WhatsApp Integration
- All order buttons: `https://wa.me/6281234567890?text=Halo%20Ichibot%2C%20saya%20tertarik%20dengan%20[NAMA_PRODUK]`
- Community form: builds wa.me URL from form fields on submit
- **Placeholder**: `6281234567890` — client replaces once

---

## 7. Responsive Strategy
- Breakpoints: `768px` (tablet), `480px` (mobile)
- Mobile nav: hamburger toggles `.nav-open` class
- World map: CSS media query switches to a simpler Asia-Pacific-focused SVG viewBox on mobile
- Product grid: 3-col → 2-col → 1-col
- Stats bar: 2x2 grid on mobile
- Footer: stacked column on mobile

---

## 8. Accessibility Checklist
- [ ] `<nav aria-label="Main navigation">`
- [ ] All `<button>` elements have `aria-label`
- [ ] Hamburger: `aria-expanded`, `aria-controls`
- [ ] Images: descriptive `alt` in Bahasa Indonesia
- [ ] `<main>`, `<section>`, `<footer>`, `<header>` semantic elements
- [ ] Sufficient contrast: warm-white on near-black passes WCAG AA

---

## 9. Build Order (Execution Sequence)

```
1. css/global.css
2. css/components.css
3. css/animations.css
4. js/main.js
5. js/products.js
6. index.html
7. products.html
8. achievements.html
9. community.html
10. about.html
```

---

## 10. cPanel Deployment Notes
- Upload all files via File Manager or FTP
- No `.htaccess` rewrite rules needed (pure static, no SPA routing)
- Google Fonts loaded via CDN — requires internet on client
- Font Awesome 6 via CDN — same requirement
- All SVG and animations are inline — zero external asset dependencies
- Test on Chrome + Firefox + Safari (Safari webkit-backdrop-filter support confirmed)
