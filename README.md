# BiznorX Realty — website

Static site. Edit `build.py` (copy + business details) or `scene.py` (the Mumbai skyline), then:

    python3 build.py            # writes the pages into site/
    ~/.local/node/bin/node serve.js 5186   # preview at http://localhost:5186

Deploy = upload the `site/` folder to any static host / nginx.

- `site/assets/css/style.css`, `site/assets/js/main.js` — hand-written, not generated.
- Scroll journey: `scene.py` draws far / mid / lights / near SVG layers (6000×1000 world, horizon y=790);
  `main.js` pans them, crossfades the sky (golden hour → night) and switches the five chapters.
- Social image `site/assets/img/og.jpg` is rendered from `_source/og.svg` with sharp.

## Projects
- **The Aura** (`/aura/`) — details and renders come from the developer's brochure
  (almantasharealty.com/wp-content/uploads/2026/10/aura-mg-brochure.pdf); crops live in `site/assets/img/aura/`.
- **Dosti Planet North** and **Heaven's Palace II** (`/projects/<slug>/`) — data in `PROJECTS` in build.py.
  They use an illustration until official images are supplied.

## Before going live (see TODOs at the top of build.py)
- Domain (`SITE["url"]`) and `live: True` (preview is noindex until then)
- BiznorX Realty is NOT yet MahaRERA-registered as an agent (expected Dec 2026). Never write "registered channel partner".
  When the number arrives, put it in `SITE["agent_rera"]` — the footer line appears automatically.
- The Aura's MahaRERA project number (`AURA["rera"]`) — hidden until added
- Contact: +91 90043 78003 · realty@biznorx.com · B/1205, Emerald, Dosti Planet North, Shil, Thane 400612 (in SITE)
- MahaRERA number for the Dosti Planet North (ES Landmark) phase
- Official images for Dosti Planet North and Heaven's Palace II
- Confirm we may use the developers' renders on our site (normally covered by the channel-partner creative kit)
