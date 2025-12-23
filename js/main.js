document.addEventListener('DOMContentLoaded', function(){
  // Mobile nav toggle
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('main-nav');
  if(toggle && nav){
    toggle.addEventListener('click', ()=>{
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('open');
    });
  }

  // Enhanced accessible carousel
  const carousel = document.querySelector('.featured-cruises .carousel');
  const track = carousel ? carousel.querySelector('.carousel-track') : null;
  const cards = track ? Array.from(track.querySelectorAll('.cruise-card')) : [];
  let idx = cards.findIndex(c=>c.classList.contains('active'));
  if(idx < 0) idx = 0;
  let autoPlayInterval = null;
  const AUTOPLAY_MS = 4000;

  function updateSlides(newIndex){
    if(!cards.length) return;
    cards.forEach((c,i)=>{
      const isActive = i === newIndex;
      c.classList.toggle('active', isActive);
      c.setAttribute('aria-hidden', String(!isActive));
      c.setAttribute('tabindex', isActive ? '0' : '-1');
      const label = `Slide ${i+1} of ${cards.length}`;
      c.setAttribute('aria-label', label);
    });
    idx = newIndex;
    const status = carousel.querySelector('.carousel-status');
    if(status) status.textContent = `Showing ${idx+1} of ${cards.length}`;
  }

  function showNext(){ updateSlides((idx + 1) % cards.length); }
  function showPrev(){ updateSlides((idx - 1 + cards.length) % cards.length); }

  function startCarousel(){
    if(autoPlayInterval || cards.length <= 1) return;
    autoPlayInterval = setInterval(()=>{
      showNext();
    }, AUTOPLAY_MS);
  }
  function stopCarousel(){
    if(autoPlayInterval){
      clearInterval(autoPlayInterval);
      autoPlayInterval = null;
    }
  }

  // Delay autoplay until after load and a short idle/window settles period so LCP can stabilize.
    if(cards.length > 1){
    // wire controls
    const btnNext = carousel.querySelector('.carousel-control.next');
    const btnPrev = carousel.querySelector('.carousel-control.prev');
    if(btnNext) btnNext.addEventListener('click', ()=>{ stopCarousel(); showNext(); });
    if(btnPrev) btnPrev.addEventListener('click', ()=>{ stopCarousel(); showPrev(); });

    // keyboard navigation for the carousel region
    carousel.addEventListener('keydown', (e)=>{
      if(e.key === 'ArrowRight') { stopCarousel(); showNext(); }
      if(e.key === 'ArrowLeft') { stopCarousel(); showPrev(); }
    });

    // initialize aria-hidden/tabindex labels
    updateSlides(idx);

    // Delay autoplay until after load and idle
    if(document.readyState === 'complete'){
      if('requestIdleCallback' in window){
        requestIdleCallback(()=>setTimeout(startCarousel, 800), {timeout:1500});
      } else {
        setTimeout(startCarousel, 1200);
      }
    } else {
      window.addEventListener('load', ()=>{
        if('requestIdleCallback' in window){
          requestIdleCallback(()=>setTimeout(startCarousel, 800), {timeout:1500});
        } else {
          setTimeout(startCarousel, 1200);
        }
      }, {once:true});
    }

    // Pause autoplay on focus/visibility change to be polite
    document.addEventListener('visibilitychange', ()=>{
      if(document.hidden) stopCarousel(); else startCarousel();
    });
    window.addEventListener('focus', startCarousel);
    window.addEventListener('blur', stopCarousel);
  }

  // Signup form handler (placeholder)
  const form = document.getElementById('signup-form');
  if(form){
    form.addEventListener('submit', (e)=>{
      e.preventDefault();
      const email = form.querySelector('input[type="email"]').value;
      console.log('Lead captured:', email);
      alert('Thanks! Check your inbox for the guide.');
      form.reset();
    });
  }
});
