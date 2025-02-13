const collapseBtn = document.getElementById('sidebar-collapse-btn');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.overlay');

collapseBtn.addEventListener('click', () => {
  sidebar.classList.toggle('show');
  overlay.classList.toggle('show-overlay');
  document.body.classList.toggle('inactive-body');
});

overlay.addEventListener('click', (e) => {
  if (overlay.classList.contains('show-overlay')) {
    e.stopPropagation();
    sidebar.classList.toggle('show');
    overlay.classList.toggle('show-overlay');
    document.body.classList.toggle('inactive-body');
  }
})
