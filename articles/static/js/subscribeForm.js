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
