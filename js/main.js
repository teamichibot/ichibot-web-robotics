/* =========================================================
   ICHIBOT ROBOTICS — main.js
   Nav scroll · Hamburger · Counters · Map arcs · Reveals
   ========================================================= */

(function () {
  'use strict';

  /* ── Helpers ─────────────────────────────────────────── */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

  /* ── Active nav link ──────────────────────────────────── */
  const currentPage = location.pathname.split('/').pop() || 'index.html';
  $$('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === currentPage || (currentPage === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });

  /* ── Nav scroll effect ────────────────────────────────── */
  const nav = $('.nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── Hamburger menu ───────────────────────────────────── */
  const hamburger = $('.nav-hamburger');
  const navLinks  = $('.nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      hamburger.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', open);
    });
    // Close on outside click
    document.addEventListener('click', e => {
      if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ── Scroll reveal (IntersectionObserver) ─────────────── */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  $$('.reveal, .pillar-card').forEach(el => revealObserver.observe(el));

  /* ── Animated counters ────────────────────────────────── */
  function animateCounter(el, target, suffix, duration = 2000) {
    const start = performance.now();
    const update = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.round(eased * target);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(update);
      else {
        el.textContent = target + suffix;
        el.classList.add('popped');
        setTimeout(() => el.classList.remove('popped'), 400);
      }
    };
    requestAnimationFrame(update);
  }

  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        $$('[data-count]', entry.target).forEach(el => {
          const target = parseInt(el.dataset.count, 10);
          const suffix = el.dataset.suffix || '';
          animateCounter(el, target, suffix);
        });
        statsObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  const statsBar = $('.stats-bar');
  if (statsBar) statsObserver.observe(statsBar);

  /* ── World Export Map ─────────────────────────────────── */
  const DESTINATIONS = [
    { name: 'Malaysia',       lng: 109.7, lat:   3.1 },
    { name: 'Philippines',    lng: 121.8, lat:  12.9 },
    { name: 'Thailand',       lng: 100.5, lat:  13.8 },
    { name: 'Vietnam',        lng: 106.7, lat:  10.8 },
    { name: 'Singapore',      lng: 103.8, lat:   1.3 },
    { name: 'Myanmar',        lng:  96.2, lat:  16.9 },
    { name: 'Australia',      lng: 133.8, lat: -25.3 },
    { name: 'Japan',          lng: 138.3, lat:  36.2 },
    { name: 'South Korea',    lng: 127.8, lat:  36.5 },
    { name: 'Taiwan',         lng: 120.9, lat:  23.7 },
    { name: 'Saudi Arabia',   lng:  45.1, lat:  24.7 },
    { name: 'UAE',            lng:  54.4, lat:  24.0 },
    { name: 'Nigeria',        lng:   8.7, lat:   9.1 },
    { name: 'United States',  lng: -95.7, lat:  37.1 },
    { name: 'United Kingdom', lng:  -1.5, lat:  51.5 },
    { name: 'Germany',        lng:  10.5, lat:  51.2 },
    { name: 'Netherlands',    lng:   5.3, lat:  52.1 },
  ];

  async function initMap() {
    const svg = $('#world-map-svg');
    if (!svg) return;

    const W = 1000, H = 500;
    const d3Ready = typeof d3 !== 'undefined' && typeof topojson !== 'undefined';

    // ── Projection setup ────────────────────────────────
    let project;
    if (d3Ready) {
      const proj = d3.geoNaturalEarth1().scale(162).translate([W / 2, H / 2]);
      project = (lng, lat) => proj([lng, lat]);

      // ── Render graticule (subtle grid) ────────────────
      const gratGroup = $('#map-graticule');
      if (gratGroup) {
        const gratPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        gratPath.setAttribute('d', d3.geoPath().projection(proj)(d3.geoGraticule()()) || '');
        gratPath.setAttribute('fill', 'none');
        gratPath.setAttribute('stroke', 'rgba(255,255,255,0.025)');
        gratPath.setAttribute('stroke-width', '0.3');
        gratGroup.appendChild(gratPath);
      }

      // ── Render country shapes from world-atlas ─────────
      try {
        const world = await fetch(
          'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json'
        ).then(r => r.json());

        const pathGen   = d3.geoPath().projection(proj);
        const countries = topojson.feature(world, world.objects.countries);
        const borders   = topojson.mesh(world, world.objects.countries, (a, b) => a !== b);
        const land      = $('#map-land');

        if (land) {
          countries.features.forEach(feat => {
            const d = pathGen(feat);
            if (!d) return;
            const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            p.setAttribute('d', d);
            p.setAttribute('fill', '#181818');
            p.setAttribute('stroke', 'rgba(255,255,255,0.06)');
            p.setAttribute('stroke-width', '0.5');
            land.appendChild(p);
          });

          // interior country borders (subtler than coast lines)
          const bp = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          bp.setAttribute('d', pathGen(borders) || '');
          bp.setAttribute('fill', 'none');
          bp.setAttribute('stroke', 'rgba(255,255,255,0.04)');
          bp.setAttribute('stroke-width', '0.4');
          land.appendChild(bp);
        }
      } catch (e) {
        console.warn('World atlas fetch failed — arcs will still render');
      }
    } else {
      // Fallback equirectangular (no D3)
      project = (lng, lat) => {
        const x = ((lng + 180) / 360) * W;
        const r = (lat * Math.PI) / 180;
        const y = H / 2 - (H * Math.log(Math.tan(Math.PI / 4 + r / 2))) / (2 * Math.PI);
        return [x, y];
      };
    }

    // ── Origin dot position (Yogyakarta) ─────────────────
    const [ox, oy] = project(110.37, -7.8);
    ['#map-origin-pulse', '#map-origin-core'].forEach(id => {
      const el = $(id);
      if (el) { el.setAttribute('cx', ox); el.setAttribute('cy', oy); }
    });

    const arcsGroup = $('#map-arcs');
    const dotsGroup = $('#map-dots');
    if (!arcsGroup || !dotsGroup) return;

    const defs   = svg.querySelector('defs');
    const arcEls = [];
    const dotEls = [];

    DESTINATIONS.forEach((dest, i) => {
      const [dx, dy] = project(dest.lng, dest.lat);

      // Gradient: red at origin → transparent at destination
      const gradId = `arcGrad${i}`;
      const grad = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
      grad.id = gradId;
      grad.setAttribute('gradientUnits', 'userSpaceOnUse');
      grad.setAttribute('x1', ox); grad.setAttribute('y1', oy);
      grad.setAttribute('x2', dx); grad.setAttribute('y2', dy);
      grad.innerHTML =
        '<stop offset="0%"   stop-color="#dc1e1e" stop-opacity="0.95"/>' +
        '<stop offset="100%" stop-color="#dc1e1e" stop-opacity="0.1"/>';
      defs.appendChild(grad);

      // Quadratic bezier arc — control point pulled upward
      const mx = (ox + dx) / 2;
      const my = Math.min(oy, dy) - Math.abs(dx - ox) * 0.2 - 18;
      const arc = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      arc.setAttribute('d', `M ${ox},${oy} Q ${mx},${my} ${dx},${dy}`);
      arc.setAttribute('fill', 'none');
      arc.setAttribute('stroke', `url(#${gradId})`);
      arc.setAttribute('stroke-width', '1.2');
      arc.setAttribute('stroke-linecap', 'round');
      arc.classList.add('map-arc');
      arcsGroup.appendChild(arc);
      const len = arc.getTotalLength() || 600;
      arc.style.setProperty('--arc-len', len);
      arc.setAttribute('stroke-dasharray', len);
      arc.setAttribute('stroke-dashoffset', len);
      arcEls.push(arc);

      // Destination dot
      const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      dot.setAttribute('cx', dx);  dot.setAttribute('cy', dy);
      dot.setAttribute('r', '3.5');
      dot.setAttribute('fill', '#dc1e1e');
      dot.setAttribute('filter', 'url(#dotGlow)');
      dot.classList.add('map-dest-dot');
      dot.setAttribute('aria-label', dest.name);
      dotsGroup.appendChild(dot);
      dotEls.push(dot);
    });

    function triggerArcs() {
      arcEls.forEach((arc, i) => {
        setTimeout(() => {
          arc.classList.add('drawing');
          setTimeout(() => dotEls[i].classList.add('drawn'), 1100);
        }, i * 140);
      });
    }

    const mapSection = $('.map-section');
    if (mapSection) {
      const mapObs = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) { triggerArcs(); mapObs.unobserve(entry.target); }
        });
      }, { threshold: 0.15 });
      mapObs.observe(mapSection);
    }
  }

  /* ── Smooth footer year ───────────────────────────────── */
  $$('.current-year').forEach(el => { el.textContent = new Date().getFullYear(); });

  /* ── Init ─────────────────────────────────────────────── */
  document.addEventListener('DOMContentLoaded', () => {
    initMap();
  });

  // Also try immediately in case DOM already ready
  if (document.readyState !== 'loading') initMap();

})();
