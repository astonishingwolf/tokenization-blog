document.querySelector('#print').addEventListener('click', () => window.print());
function progress() {
  const distance = document.documentElement.scrollHeight - innerHeight;
  document.querySelector('.reading-progress').style.width = `${distance > 0 ? scrollY / distance * 100 : 0}%`;
  const sections = [...document.querySelectorAll('article section')];
  const current = sections.filter(section => section.getBoundingClientRect().top <= 140).at(-1) || sections[0];
  document.querySelectorAll('nav a').forEach(link => {
    const active = link.hash === `#${current.id}`;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
window.addEventListener('scroll', progress, {passive:true});
window.addEventListener('resize', progress);
progress();
