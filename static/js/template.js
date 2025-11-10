document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  if (!menuButton || !navLinks) return;

  // ハンバーガー開閉
  menuButton.addEventListener("click", () => {
    navLinks.classList.toggle("active");
    menuButton.textContent = navLinks.classList.contains("active") ? "✕" : "☰";
  });

  // ✅ 各リンクをクリックしたら閉じる
  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("active");
      menuButton.textContent = "☰";
    });
  });
});
