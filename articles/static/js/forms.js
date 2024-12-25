const filtersForm = document.getElementById('filters-form');
const filterCheckboxes = filtersForm.querySelectorAll('.filter-checkbox');
const appliedFilterBtns = document.querySelectorAll('.applied-filter-btn');
const articleTagBtns = document.querySelectorAll('.tag-btn');
const appliedFilters = new Set();

document.addEventListener('DOMContentLoaded', () => {
  filterCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', (e) => updateFilter(e.target));
    if (checkbox.checked) {
      appliedFilters.add(checkbox.value);
    }
  });

  appliedFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      appliedFilters.delete(btn.value);
      window.location.href = updateURL();
    });
  });

  articleTagBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      appliedFilters.clear();
      appliedFilters.add(btn.textContent);
      window.location.href = updateURL();
    });
  });
});

function updateFilter(checkbox) {
  if (checkbox.checked) {
    appliedFilters.add(checkbox.value);
  } else {
    appliedFilters.delete(checkbox.value);
  }
  window.location.href = updateURL();
}

function updateURL() {
  let baseUrl = '/home/';
  let i = 0;
  if (appliedFilters.size > 0) {
    baseUrl += '?';
  }

  appliedFilters.forEach(tag => {
    baseUrl += `${i === 0 ? '' : '&'}tags=${tag}`;
    i++;
  });
  return baseUrl;
}
