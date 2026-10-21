/* BiznorX Realty — scroll journey, header, menu, reveals and WhatsApp forms. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const ss = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
  const lerp = (a, b, t) => a + (b - a) * t;

  const header = $('[data-header]');
  const journey = $('.journey');
  const themed = $$('[data-theme]');
  const mbar = $('[data-mbar]');
  const waFloat = $('.wa-float');
  const parallax = reduced ? [] : $$('[data-parallax]');

  /* ---------------------------------------------- header theme, mobile bar */
  let ticking = false;
  function chrome() {
    ticking = false;
    const y = scrollY;
    const hh = header.offsetHeight;
    const inJourney = journey && y < journey.offsetTop + journey.offsetHeight - hh;
    header.classList.toggle('is-scrolled', y > 10 && !inJourney);
    let light = false;
    for (const s of themed) {
      const r = s.getBoundingClientRect();
      if (r.top <= hh / 2 && r.bottom > hh / 2) { light = s.dataset.theme === 'light'; break; }
    }
    header.classList.toggle('is-light', light && !document.body.classList.contains('menu-open'));
    // gentle parallax on full-bleed photos
    for (const el of parallax) {
      const r = el.parentElement.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight) el.style.transform = `translate3d(0,${(r.top * -0.12).toFixed(1)}px,0)`;
    }
    const showAfter = journey ? journey.offsetTop + journey.offsetHeight - innerHeight * 0.5 : innerHeight * 0.5;
    const nearEnd = y + innerHeight > document.documentElement.scrollHeight - 140;
    const show = y > showAfter && !nearEnd;
    mbar && mbar.classList.toggle('on', show);
    waFloat && waFloat.classList.toggle('on', show);
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(chrome); } }, { passive: true });
  addEventListener('resize', chrome);
  chrome();

  /* ---------------------------------------------- mobile menu */
  const menuBtn = $('[data-menu-btn]');
  const menu = $('[data-menu]');
  const MENU_D = 'M4 7h16M4 12h16M4 17h10';
  const CLOSE_D = 'M6 6l12 12M18 6 6 18';
  function setMenu(open) {
    if (!menu) return;
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    $('path', menuBtn).setAttribute('d', open ? CLOSE_D : MENU_D);
    document.body.classList.toggle('menu-open', open);
    if (open) {
      menu.hidden = false;
      requestAnimationFrame(() => menu.classList.add('open'));
    } else {
      menu.classList.remove('open');
      setTimeout(() => { if (!menu.classList.contains('open')) menu.hidden = true; }, 350);
    }
    chrome();
  }
  menuBtn && menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
  menu && menu.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
  addEventListener('keydown', e => { if (e.key === 'Escape' && document.body.classList.contains('menu-open')) setMenu(false); });

  /* ---------------------------------------------- reveals */
  const groups = new Map();
  $$('.reveal').forEach(el => {
    const list = groups.get(el.parentElement) || [];
    list.push(el);
    groups.set(el.parentElement, list);
  });
  groups.forEach(list => list.forEach((el, i) => el.style.setProperty('--rd', Math.min(i * 0.08, 0.4) + 's')));
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
    $$('.reveal, [data-steps]').forEach(el => io.observe(el));
  } else {
    $$('.reveal, [data-steps]').forEach(el => el.classList.add('in'));
  }

  /* ---------------------------------------------- enquiry: preselect + WhatsApp */
  const form = $('[data-wa-form]');
  $$('[data-interest]').forEach(a => a.addEventListener('click', () => {
    const sel = form && $('[data-interest-select]', form);
    if (sel) sel.selectedIndex = +a.dataset.interest;
  }));
  $$('[data-want]').forEach(a => a.addEventListener('click', () => {
    const box = form && form.querySelector(`input[name="Send me"][value="${a.dataset.want}"]`);
    if (box) box.checked = true;
  }));
  $$('[data-wa-form]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    const name = f.elements.Name;
    const phone = f.elements.Phone;
    const okName = name.value.trim().length > 1;
    const okPhone = phone.value.replace(/\D/g, '').length >= 7;
    name.classList.toggle('err', !okName);
    phone.classList.toggle('err', !okPhone);
    const err = $('[data-form-error]', f);
    err.hidden = okName && okPhone;
    if (!err.hidden) { (okName ? phone : name).focus(); return; }
    const data = new FormData(f);
    const lines = ['Hi BiznorX Realty, I would like to enquire.', ''];
    for (const [k, v] of data.entries()) {
      if (k === 'Send me' || !String(v).trim()) continue;
      lines.push(`${k}: ${String(v).trim()}`);
    }
    const wants = data.getAll('Send me');
    if (wants.length) lines.push(`Please send: ${wants.join(', ')}`);
    window.open(`https://wa.me/${f.dataset.waForm}?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
  }));

  /* ---------------------------------------------- lightbox for project renders */
  const shots = $$('[data-lightbox]');
  if (shots.length) {
    let lb = null, idx = 0;
    const show = i => {
      idx = (i + shots.length) % shots.length;
      const el = shots[idx];
      const im = $('img', lb);
      im.src = el.dataset.lightbox;
      im.alt = $('img', el).alt;
      $('p', lb).textContent = (el.querySelector('figcaption') || {}).textContent || im.alt;
    };
    const close = () => { lb.classList.remove('open'); document.body.style.overflow = ''; setTimeout(() => { lb.hidden = true; }, 300); };
    const open = i => {
      if (!lb) {
        lb = document.createElement('div');
        lb.className = 'lb';
        lb.setAttribute('role', 'dialog');
        lb.setAttribute('aria-modal', 'true');
        lb.innerHTML = '<img alt=""><p></p><button class="lb-x" type="button" aria-label="Close">&times;</button><button class="lb-prev" type="button" aria-label="Previous image">&#8249;</button><button class="lb-next" type="button" aria-label="Next image">&#8250;</button>';
        document.body.appendChild(lb);
        lb.addEventListener('click', e => {
          if (e.target.closest('.lb-prev')) show(idx - 1);
          else if (e.target.closest('.lb-next')) show(idx + 1);
          else if (e.target === lb || e.target.closest('.lb-x')) close();
        });
        addEventListener('keydown', e => {
          if (!lb || lb.hidden) return;
          if (e.key === 'Escape') close();
          if (e.key === 'ArrowRight') show(idx + 1);
          if (e.key === 'ArrowLeft') show(idx - 1);
        });
      }
      lb.hidden = false;
      show(i);
      document.body.style.overflow = 'hidden';
      requestAnimationFrame(() => lb.classList.add('open'));
      $('.lb-x', lb).focus();
    };
    shots.forEach((el, i) => {
      el.tabIndex = 0;
      el.setAttribute('role', 'button');
      el.addEventListener('click', () => open(i));
      el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
    });
  }

  /* ---------------------------------------------- the Mumbai journey */
  const pin = $('[data-journey]');
  if (!pin || reduced) return;
  document.documentElement.classList.add('j-on');

  const layers = $$('[data-layer]', pin);
  const mid = $('[data-mid]', pin);
  const midIdx = layers.indexOf(mid);
  const skies = [2, 3, 4].map(n => $(`[data-sky="${n}"]`, pin));
  const stars = $('[data-stars]', pin);
  const moon = $('[data-moon]', pin);
  const sun = $('[data-sun]', pin);
  const glint = $('[data-glint]', pin);
  const clouds = $('[data-clouds]', pin);
  const lights = $('[data-lights]', pin);
  const intro = $('[data-intro]', pin);
  const cue = $('[data-cue]', pin);
  const prog = $('[data-progress]', pin);
  const bar = $('[data-bar]', pin);
  const skip = $('.j-skip', pin);
  const chs = $$('.j-ch', pin);
  const steps = $$('[data-step]', pin);
  const plane = $('[data-plane]', pin);
  const birds = $('[data-birds]', pin);
  const beam = $('.j-aura-beam', pin);
  const sunwrap = $('.j-sunwrap', pin);
  // world-anchored labels fade out when they slide under the chapter copy on the left
  const tags = $$('.j-label, .j-aura', pin).map(el => ({ el, fade: el.classList.contains('j-aura') ? $('.j-aura-card', el) : el, wx: parseFloat(el.style.left) / 100 * 6000 }));
  const WORLD = 6000;
  const BOUNDS = [2150, 3800, 4580, 5140]; // camera x (world units) where each chapter hands over to the next

  let W = 0, H = 0, top = 0, len = 1, sizes = [], cur = 0, tgt = 0, raf = 0, last = 0, chapter = -2;

  function measure() {
    W = pin.clientWidth;
    H = pin.clientHeight;
    sizes = layers.map(l => l.offsetWidth);
    top = journey.offsetTop;
    len = Math.max(1, journey.offsetHeight - H);
    tgt = clamp((scrollY - top) / len, 0, 1);
  }

  function render(p) {
    // hold on the intro for a moment, then glide (ease in-out) across the city
    const t = clamp((p - 0.035) / 0.95, 0, 1);
    const q = 0.5 - 0.5 * Math.cos(Math.PI * t);
    for (let i = 0; i < layers.length; i++) {
      layers[i].style.transform = `translate3d(${(-q * (sizes[i] - W)).toFixed(1)}px,0,0)`;
    }
    // golden hour -> dusk -> blue hour -> night
    skies[0].style.opacity = ss(0.04, 0.36, q);
    skies[1].style.opacity = ss(0.3, 0.64, q);
    skies[2].style.opacity = ss(0.58, 0.9, q);
    stars.style.opacity = ss(0.45, 0.92, q);
    moon.style.opacity = ss(0.62, 0.95, q);
    sun.style.transform = `translate3d(0,${(ss(0, 0.34, q) * sunwrap.clientHeight * 0.62).toFixed(1)}px,0)`;
    sun.style.opacity = 1 - ss(0.24, 0.36, q);
    glint.style.opacity = 1 - ss(0.06, 0.28, q);
    clouds.style.transform = `translate3d(${(-q * W * 0.3).toFixed(1)}px,0,0)`;
    clouds.style.opacity = 1 - ss(0.25, 0.7, q) * 0.9;
    lights.style.opacity = (0.28 + 0.72 * ss(0.1, 0.68, q)).toFixed(3);
    beam.style.opacity = (0.3 + 0.7 * ss(0.4, 0.66, q)).toFixed(3);

    // intro copy leaves as soon as the camera starts moving
    const io = 1 - ss(0, 0.032, p);
    intro.style.opacity = io;
    intro.style.transform = `translate3d(0,${((1 - io) * -50).toFixed(1)}px,0)`;
    intro.style.visibility = io < 0.01 ? 'hidden' : '';
    cue.style.opacity = 1 - ss(0, 0.015, p);
    prog.classList.toggle('on', p > 0.03 && p < 0.985);
    skip.style.opacity = 1 - ss(0.96, 0.99, p);
    skip.style.visibility = p > 0.99 ? 'hidden' : '';
    bar.style.transform = `scaleX(${q.toFixed(4)})`;

    // which part of the city is in the middle of the screen
    const scale = sizes[midIdx] / WORLD;
    const midX = -q * (sizes[midIdx] - W);
    const shown = ss(0.02, 0.05, p);
    for (const t of tags) {
      let o = shown;
      if (W > 900) o *= ss(W * 0.34, W * 0.47, t.wx * scale + midX);
      t.fade.style.opacity = o.toFixed(3);
    }
    const cx = (q * (sizes[midIdx] - W) + W / 2) / scale;
    let c = BOUNDS.findIndex(b => cx < b);
    if (c === -1) c = 4;
    if (p < 0.04) c = -1;
    if (c !== chapter) {
      chapter = c;
      chs.forEach((el, i) => el.classList.toggle('on', i === c));
      steps.forEach((el, i) => el.classList.toggle('on', i <= c));
    }

    // a flight takes off from the new airport as we arrive
    const f = ss(0.72, 1, q);
    if (f > 0) {
      const wx = 5440 + f * 440;
      const wy = 812 - Math.pow(f, 1.5) * 270;
      plane.style.opacity = Math.min(1, f * 6);
      plane.style.transform = `translate3d(${(wx * scale).toFixed(1)}px,${(wy * scale - plane.offsetHeight).toFixed(1)}px,0) rotate(${(-f * 14).toFixed(2)}deg)`;
    } else {
      plane.style.opacity = 0;
    }

    // a few birds over the bay at the start
    const b = clamp(p / 0.28, 0, 1);
    birds.style.opacity = 1 - ss(0.7, 1, b);
    birds.style.transform = `translate3d(${lerp(W * 0.56, W * 1.05, b).toFixed(1)}px,${(H * 0.27 - b * H * 0.1).toFixed(1)}px,0)`;
  }

  function tick(now) {
    const dt = last ? Math.min(64, now - last) : 16.7;
    last = now;
    const k = 1 - Math.pow(1 - 0.085, dt / 16.7);
    cur += (tgt - cur) * k;
    if (Math.abs(tgt - cur) < 0.00008) cur = tgt;
    render(cur);
    if (cur !== tgt) raf = requestAnimationFrame(tick);
    else { raf = 0; last = 0; }
  }
  function onScroll() {
    tgt = clamp((scrollY - top) / len, 0, 1);
    if (!raf) raf = requestAnimationFrame(tick);
  }
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', () => { measure(); cur = tgt; render(cur); });
  measure();
  cur = tgt;
  render(cur);
  // fonts/images can shift the page height after load
  addEventListener('load', () => { measure(); render(cur); });
})();
