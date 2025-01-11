const codeBlocks = document.querySelectorAll('.code-block');
const shareCopyLinkBtn = document.getElementById('share-copy-link');
const shareBtn = document.getElementById('share-btn');
const shareLinkList = document.getElementById('share-links-list');

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

shareCopyLinkBtn.addEventListener('click', async (e) => {
  e.stopPropagation();
  const link = shareCopyLinkBtn.dataset.link;
  try {
    await navigator.clipboard.writeText(link);
    shareCopyLinkBtn.querySelector('span').textContent = 'Copied!';
  } catch (error) {
    console.error();
    shareCopyLinkBtn.querySelector('span').textContent = 'Error';
  }
});

shareBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  shareLinkList.classList.toggle('show');
  shareCopyLinkBtn.querySelector('span').textContent = 'Copy Link';
});

document.addEventListener('click', (e) => {
  e.stopPropagation();
  console.log(e.target);
  if (!shareLinkList.contains(e.target)
    && e.target !== shareBtn
    && shareLinkList.classList.contains('show')) {
    shareLinkList.classList.remove('show');
    shareCopyLinkBtn.querySelector('span').textContent = 'Copy Link';
  }
});
