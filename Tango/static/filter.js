
(function () {
  // ---- Helpers to safely get elements that may not exist ----
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  // Checkboxes (some IDs varied earlier, so support either spelling)
  const controls = {
    catCompetitive: $('#cat-competitive'),
    catCasual: $('#cat-casual'),
    catSocial: $('#cat-social'),

    availAvailable: $('#avail-available'),
    availLow: $('#avail-low'),
    availSold: $('#avail-sold') || $('#avail-soldout'), // support either id
  };

  // All event cards we want to filter
  const cards = $$('.card.card-main');

  // --- Normalise strings ---
  const norm = (s) => (s || '').toString().trim().toLowerCase();

  // Try to infer category from id if no data attribute present
  function inferCategoryFromId(id) {
    const s = norm(id);
    if (!s) return null;
    if (s.includes('compet')) return 'competitive';   // catches "competative" too
    if (s.includes('casual')) return 'casual';
    if (s.includes('social') || s.includes('scoial')) return 'social';
    return null;
  }

  // Try to infer availability by reading the list-group text
  function inferStatusFromText(cardEl) {
    // look for the element that has the status line
    const li = cardEl.querySelector('.list-group-item-main') || cardEl.querySelector('.list-group-item');
    const text = norm(li ? li.textContent : '');
    if (!text) return null;
    if (text.includes('sold')) return 'sold out';
    if (text.includes('low')) return 'low';
    // default if it mentions available
    if (text.includes('avail')) return 'available';
    return null;
  }

  // Extract a card's category + status (prefer data-attrs if present)
  function getCardMeta(cardEl) {
    const cat =
      norm(cardEl.dataset?.category) ||
      inferCategoryFromId(cardEl.id) ||
      null;

    const status =
      norm(cardEl.dataset?.status) ||
      inferStatusFromText(cardEl) ||
      null;

    return { cat, status };
  }

  // Toggle visibility: keep Bootstrap collapse happy + hard hide
  function setVisible(cardEl, visible) {
    cardEl.classList.toggle('show', visible);  // for .collapse
    cardEl.classList.toggle('d-none', !visible); // hard hide to remove space
    // optional: aria for accessibility
    cardEl.setAttribute('aria-hidden', visible ? 'false' : 'true');
  }

  function selectedCategories() {
    const out = [];
    if (controls.catCompetitive?.checked) out.push('competitive');
    if (controls.catCasual?.checked) out.push('casual');
    if (controls.catSocial?.checked) out.push('social');
    return out;
  }

  function selectedStatuses() {
    const out = [];
    if (controls.availAvailable?.checked) out.push('available');
    if (controls.availLow?.checked) out.push('low');
    if (controls.availSold?.checked) out.push('sold out');
    return out;
  }

  function applyFilters() {
    const cats = selectedCategories();
    const stats = selectedStatuses();

    const filterByCat = cats.length > 0;    // if none selected, don't filter by category
    const filterByStat = stats.length > 0;  // if none selected, don't filter by status

    cards.forEach((card) => {
      const { cat, status } = getCardMeta(card);

      // default to visible unless a filter excludes it
      let visible = true;

      if (filterByCat) {
        // if we can't infer a category, treat as not matching
        visible = visible && !!cat && cats.includes(cat);
      }

      if (filterByStat) {
        // if we cant infer a status, treat as not matching
        visible = visible && !!status && stats.includes(status);
      }

      setVisible(card, visible);
    });
  }

  // --- Wire up events ---
  Object.values(controls).forEach((el) => {
    if (el) el.addEventListener('change', applyFilters, { passive: true });
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyFilters, { once: true });
  } else {
    applyFilters();
  }
})();
