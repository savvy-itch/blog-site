import { handleReadingList } from "./main.js";

const savedArticles = JSON.parse(localStorage.getItem('saved-articles')) ?? [];
const listContainer = document.getElementById('saved-articles-list');

if (!savedArticles || savedArticles.length === 0) {
  listContainer.innerHTML = `<p>No saved articles yet :(</p>`;
} else {
  fetchArticles();
}

async function fetchArticles() {
  try {
    const res = await fetch('/home/articles/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({ ids: savedArticles })
    });

    if (res.ok) {
      const data = await res.json();
      populateSavedList(data.saved_articles);
    }
  } catch (error) {
    console.error(error);
  }
}

function getCSRFToken() {
  return document.querySelector('[name="csrfmiddlewaretoken"]').value;
}

function populateSavedList(list) {
  list.map(article => {
    const listItem = document.createElement('article');
    listItem.classList.add('saved-article');
    listItem.innerHTML = `
      <div>
        <a class="saved-article-link" href="${article.url}" target="_blank">${article.title}</a>
        <p class="saved-article-desc">${article.desc}</p>
      </div>
      <button class="save-btn" data-id="${article.id}" type="button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bookmark"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>
        <span>Saved</span>
      </button>
      `;
    listContainer.appendChild(listItem);
    const saveBtn = listItem.querySelector('.save-btn');
    saveBtn.addEventListener('click', (e) => {
      const articleId = e.currentTarget.dataset.id;
      if (articleId) {
        handleReadingList(articleId);
        listContainer.removeChild(listItem);
      }
    })
  });
}
