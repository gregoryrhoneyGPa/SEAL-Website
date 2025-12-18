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

  // Simple carousel: rotate active class every 4s
  const cards = Array.from(document.querySelectorAll('.featured-cruises .cruise-card'));
  let idx = cards.findIndex(c=>c.classList.contains('active'));
  if(idx < 0) idx = 0;
  if(cards.length > 1){
    setInterval(()=>{
      cards[idx].classList.remove('active');
      idx = (idx + 1) % cards.length;
      cards[idx].classList.add('active');
    }, 4000);
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
