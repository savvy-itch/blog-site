document.addEventListener('DOMContentLoaded', () => {
  const article = document.querySelector('.article-wrapper');

  if (article) {
    const text = article.textContent;
    const words = [...text.matchAll(/\S+/g)];
    const readingTime = Math.round(words.length / 200);
    const badge = document.getElementById('time-to-read');
    if (badge) {
      badge.textContent = `${readingTime} ${readingTime === 1 ? 'minute' : 'minutes'}`;
    }
  }
})