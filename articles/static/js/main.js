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

const saveBtns = document.querySelectorAll('.save-btn');

document.addEventListener('DOMContentLoaded', () => {
  const savedArticles = JSON.parse(localStorage.getItem('saved-articles'));
  saveBtns.forEach(btn => {
    const isSaved = savedArticles.some(el => el === btn.dataset.id);
      if (isSaved) {
        btn.querySelector('svg').style.fill = 'currentColor';
        btn.querySelector('span').textContent = 'Saved';
      }
  });
});

saveBtns.forEach(btn => {
  btn.addEventListener('click', (e) => {
    const articleId = e.currentTarget.dataset.id;
    if (articleId) {
      const isSaved = btn.querySelector('svg').style.fill === 'currentcolor';
      if (isSaved) {
        btn.querySelector('svg').style.fill = 'none';
        btn.querySelector('span').textContent = 'Save';
      } else {
        btn.querySelector('svg').style.fill = 'currentColor';
        btn.querySelector('span').textContent = 'Saved';
      }
      handleReadingList(articleId);
    }
  });
});

export function handleReadingList(id) {
  let savedArticles = JSON.parse(localStorage.getItem('saved-articles')) ?? [];
  const article = savedArticles.find(a => a === id);

  if (article) {
    savedArticles = savedArticles.filter(a => a !== id);
  } else {
    savedArticles.push(id);
  }

  localStorage.removeItem('saved-articles');
  localStorage.setItem('saved-articles', JSON.stringify(savedArticles.sort((a,b) => a-b)));
}
