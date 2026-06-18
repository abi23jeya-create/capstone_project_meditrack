(() => {
  const btn = document.querySelector('[data-theme-toggle]');
  let mode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', mode);
  if (btn) {
    btn.addEventListener('click', () => {
      mode = mode === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', mode);
    });
  }
})();
