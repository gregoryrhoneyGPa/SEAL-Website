// Lightweight GA event helper — safe no-op if analytics not loaded
(function(){
  function sendGAEvent(category, action, label) {
    try {
      if (window.gtag) {
        window.gtag('event', action, { 'event_category': category, 'event_label': label });
        return;
      }
      if (window.ga && window.ga.getAll) {
        // Universal Analytics
        var trackers = window.ga.getAll();
        trackers.forEach(function(t){ t.send('event', category, action, label); });
        return;
      }
      if (window.dataLayer && Array.isArray(window.dataLayer)) {
        window.dataLayer.push({ event: 'custom_event', eventCategory: category, eventAction: action, eventLabel: label });
        return;
      }
    } catch (e) { /* fail silently */ }
  }

  function onClick(e){
    var el = e.currentTarget;
    var cat = el.getAttribute('data-ga-category') || 'Interaction';
    var act = el.getAttribute('data-ga-action') || 'click';
    var lab = el.getAttribute('data-ga-label') || (el.getAttribute('href') || el.textContent).trim();
    sendGAEvent(cat, act, lab);
  }

  document.addEventListener('DOMContentLoaded', function(){
    var els = document.querySelectorAll('[data-ga-category]');
    els.forEach(function(el){ el.addEventListener('click', onClick, {passive:true}); });
  });

  window.__sendGAEvent = sendGAEvent;
})();
