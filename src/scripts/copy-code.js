// src/scripts/copy-code.js
export function setupCopyButtons() {
  const blocks = document.querySelectorAll('pre');

  blocks.forEach((block) => {
    // 检查是否已经添加过按钮，防止重复
    if (block.querySelector('.copy-button')) return;

    // 创建按钮
    const button = document.createElement('button');
    button.innerText = 'Copy';
    button.className = 'copy-button';

    // 将按钮加入代码块（pre 标签）
    block.appendChild(button);

    button.addEventListener('click', async () => {
      const code = block.querySelector('code');
      const text = code.innerText;

      try {
        await navigator.clipboard.writeText(text);
        button.innerText = 'Copied!';
        button.classList.add('active');

        // 2秒后恢复原样
        setTimeout(() => {
          button.innerText = 'Copy';
          button.classList.remove('active');
        }, 2000);
      } catch (err) {
        console.error('无法复制: ', err);
      }
    });
  });
}