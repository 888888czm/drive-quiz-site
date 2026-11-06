// 自动填充当前年份
document.getElementById('year').textContent = new Date().getFullYear();

// 可选：从远端 version.json 读取最新版本号（需与 exe 的自动更新配合）
// 若没有服务器，可注释掉以下代码，版本号保持 HTML 中的静态值
(function loadVersion() {
  const VERSION_URL = null; // 例：'https://your-server.com/version.json'
  if (!VERSION_URL) return;
  fetch(VERSION_URL)
    .then(res => res.json())
    .then(data => {
      if (data.version) {
        document.getElementById('version').textContent = 'v' + data.version;
      }
    })
    .catch(() => { /* 静默失败，保持默认版本号 */ });
})();

// 导航栏平滑滚动（兼容旧浏览器，html { scroll-behavior } 已处理新浏览器）
document.querySelectorAll('.navbar nav a, .hero-btns a').forEach(link => {
  link.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href && href.startsWith('#')) {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
});