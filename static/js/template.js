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

  // ========== 出演者イラスト 遷移アニメーション ==========
  const artistTransition = document.getElementById("artist-transition");

  document.querySelectorAll('a[href*="/artist/"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      // 既にアニメーション中なら何もしない
      if (artistTransition.classList.contains("active")) return;

      e.preventDefault();
      const dest = link.href;

      // オーバーレイを表示してアニメーション開始
      artistTransition.classList.add("active");

      // 最後のキャラクターが渡り終わる頃（delay 0.7s + duration 2.0s = 2.7s）に遷移
      setTimeout(() => {
        window.location.href = dest;
      }, 2700);
    });
  });
});
