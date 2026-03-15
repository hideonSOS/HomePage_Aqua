document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.g-fade');
  if (!items.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('g-visible');
        observer.unobserve(entry.target); // 1回のみ発火
      }
    });
  }, { threshold: 0.15 });

  items.forEach(el => observer.observe(el));
});
