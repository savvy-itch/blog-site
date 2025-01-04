const codeBlocks = document.querySelectorAll('.code-block');

codeBlocks.forEach(blockElem => {
  const copyBtn = document.createElement('button');
  copyBtn.classList.add('copy-to-clipboard-btn');
  copyBtn.innerHTML = `
    <img class="copy-to-clipboard-icon show" src="${clipboardIconPath}" alt="copy to clipboard icon">
    <img class="success-copy-icon" src="${checkIconPath}" alt="successful copy to clipboard icon">
    <img class="fail-copy-icon" src="${xIconPath}" alt="failed copy to clipboard icon">
    `;
  blockElem.appendChild(copyBtn);
  copyBtn.addEventListener('click', (e) => {
    getCodeContent(e.currentTarget);
  });
});

async function getCodeContent(copyBtn) {
  const codeBlockElem = copyBtn.parentElement.querySelector('code');
  const copyIcon = copyBtn.querySelector('.copy-to-clipboard-icon');
  try {
    await navigator.clipboard.writeText(codeBlockElem.innerText);
    const successIcon = copyBtn.querySelector('.success-copy-icon');
    animateCopyBtn(copyBtn, copyIcon, successIcon);
  } catch (error) {
    console.error(error.message);
    const xIcon = copyBtn.querySelector('.fail-copy-icon');
    animateCopyBtn(copyBtn, copyIcon, xIcon);
  }
}

function animateCopyBtn(copyBtn, copyIcon, statusIcon) {
  copyIcon.classList.toggle('show');
  statusIcon.classList.toggle('show');
  copyBtn.setAttribute('disabled', 'true');
  setTimeout(() => {
    copyIcon.classList.toggle('show');
    statusIcon.classList.toggle('show');
    copyBtn.removeAttribute('disabled');
  }, 1000);
}
