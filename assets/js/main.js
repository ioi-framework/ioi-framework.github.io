// ── Filter bar (cases, rules, instantiators) ───────────────
document.addEventListener('DOMContentLoaded', () => {

  // Shared filter logic for any page that has .filter-btn + a grid with [data-category] cards
  document.querySelectorAll('.filter-bar').forEach(bar => {
    const gridId = bar.nextElementSibling?.id;
    const grid = gridId ? document.getElementById(gridId) : null;
    if (!grid) return;

    bar.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        bar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active-filter'));
        btn.classList.add('active-filter');

        const f = btn.dataset.filter;
        grid.querySelectorAll('.card').forEach(card => {
          const cat    = card.dataset.category || '';
          const status = card.dataset.status   || '';
          const show =
            f === 'all'       ? true :
            f === 'validated' ? status === 'validated' :
                                cat === f;
          card.style.display = show ? '' : 'none';
        });
      });
    });
  });

  // ── Nav active state ──────────────────────────────────────
  const path = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = (a.getAttribute('href') || '').replace(/\/$/, '') || '/';
    if (href === path || (href !== '/' && path.startsWith(href))) {
      a.classList.add('active');
    }
  });

});

// ── Citation copy ─────────────────────────────────────────
function copyCitation() {
  const raw = `@article{ioi-framework-2025,
  title   = {Indicator of Inconsistency (IoI): A SPARQL-Based Framework for Cross-Artifact Contradiction Detection in Digital Forensics},
  journal = {Forensic Science International: Digital Investigation},
  year    = {2025},
  note    = {Under review},
  url     = {https://ioi-framework.github.io}
}`;
  navigator.clipboard.writeText(raw).then(() => {
    const btn = document.querySelector('.citation-copy');
    if (!btn) return;
    const orig = btn.textContent;
    btn.textContent = 'Copied ✓';
    btn.style.background = '#1a6640';
    btn.style.color = '#fff';
    btn.style.borderColor = '#1a6640';
    setTimeout(() => {
      btn.textContent = orig;
      btn.style.background = btn.style.color = btn.style.borderColor = '';
    }, 2000);
  });
}
