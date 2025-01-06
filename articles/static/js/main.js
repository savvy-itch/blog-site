const themePicker = document.getElementById('color-theme-selector');

document.addEventListener('DOMContentLoaded', () => {
  const article = document.querySelector('.article-wrapper');

  if (article) {
    const text = article.textContent;
    const words = [...text.matchAll(/\S+/g)];
    const readingTime = Math.round(words.length / 180);
    const badge = document.getElementById('time-to-read');
    if (badge) {
      badge.textContent = `${readingTime} ${readingTime === 1 ? 'minute' : 'minutes'}`;
    }
  }

  const selectedTheme = localStorage.getItem('theme');
  if (selectedTheme) {
    themePicker.value = selectedTheme;
  }
});

themePicker.addEventListener('change', () => {
  localStorage.removeItem('theme');
  if (themePicker.value !== 'system') {
    localStorage.setItem('theme', themePicker.value);
  }
});
