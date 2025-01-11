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
    baseUrl += `${i === 0 ? '' : '&'}tags=${encodeURIComponent(tag)}`;
    i++;
  });
  return baseUrl;
}

// Subscribe form
const subscribeForm = document.getElementById('subscribe-form');
const emailInput = subscribeForm.querySelector("input[type='email']")
const resMsgPara = document.getElementById('res-msg');

subscribeForm.addEventListener('submit', (e) => handleSubscribeFormSubmit(e));

async function handleSubscribeFormSubmit(e) {
  e.preventDefault();
  const data = new FormData(subscribeForm).get('email');
  if (data) {
    try {
      const res = await fetch('/home/subscribe/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ email: data })
      });

      const resMsg = await res.json();
      resMsgPara.classList.remove('success-msg');
      resMsgPara.classList.remove('error-msg');
      
      if (res.ok) {
        console.log(resMsg.success_msg);
        resMsgPara.classList.add('success-msg');
        resMsgPara.textContent = resMsg.success_msg;
      } else {
        console.log(resMsg.error_msg);
        resMsgPara.classList.add('error-msg');
        resMsgPara.textContent = resMsg.error_msg;
      }
    } catch (error) {
      console.error(error);
    } finally {
      emailInput.value = '';
    }
  }
}

function getCSRFToken() {
  return document.querySelector('[name="csrfmiddlewaretoken"]').value;
}
