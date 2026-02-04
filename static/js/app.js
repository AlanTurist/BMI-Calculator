(function(){
  const htmlEl = document.documentElement;

  const safeGet = (k) => {
    try { return window.localStorage ? localStorage.getItem(k) : null; } catch(e){ return null; }
  };
  const safeSet = (k,v) => {
    try { if(window.localStorage) localStorage.setItem(k,v); } catch(e){}
  };

  const stored = safeGet('theme');

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
      safeSet('theme', isDark ? 'dark' : 'light');
      setIcons();
    });
  }
})();