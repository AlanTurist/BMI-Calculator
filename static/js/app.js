(function(){
  const htmlEl = document.documentElement;
  const stored = localStorage.getItem('theme');
  const setIcons = () => {
    const sun = document.getElementById('icon-sun');
    const moon = document.getElementById('icon-moon');
    if(!sun || !moon) return;
    const isDark = htmlEl.classList.contains('dark');
    sun.classList.toggle('hidden', !isDark);
    moon.classList.toggle('hidden', isDark);
  };

  if (stored === 'dark') htmlEl.classList.add('dark');
  setIcons();

  const btn = document.getElementById('theme-toggle');
  if(btn){
    btn.addEventListener('click', () => {
      const isDark = htmlEl.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      setIcons();
    });
  }
})();
