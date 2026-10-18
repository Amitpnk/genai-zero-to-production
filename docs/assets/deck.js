// Present mode: one slide at a time, full screen. Scroll view needs no script.
(function () {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const btn = document.querySelector("[data-present]");
  const hint = document.querySelector(".present-hint");
  if (!slides.length) return;

  slides.forEach((s, i) => {
    s.id = s.id || "slide-" + (i + 1);
    const n = document.createElement("span");
    n.className = "slide-num";
    n.setAttribute("aria-hidden", "true");
    n.textContent = i + 1 + " / " + slides.length;
    s.appendChild(n);
  });

  let current = 0;
  const show = (i) => {
    current = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => s.classList.toggle("current", k === current));
    history.replaceState(null, "", "#" + slides[current].id);
  };

  const start = () => {
    // Start from the slide nearest the top of the viewport.
    const top = slides.findIndex((s) => s.getBoundingClientRect().bottom > 80);
    document.body.classList.add("presenting");
    show(top < 0 ? 0 : top);
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().catch(() => {});
    }
    if (hint) { hint.style.opacity = 1; setTimeout(() => (hint.style.opacity = 0), 2500); }
  };
  const stop = () => {
    document.body.classList.remove("presenting");
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    slides[current].scrollIntoView({ block: "start" });
  };

  if (btn) btn.addEventListener("click", start);
  document.addEventListener("fullscreenchange", () => {
    if (!document.fullscreenElement && document.body.classList.contains("presenting")) stop();
  });

  document.addEventListener("keydown", (e) => {
    const on = document.body.classList.contains("presenting");
    if (!on) {
      if (e.key === "p" && !e.ctrlKey && !e.metaKey) start();
      return;
    }
    if (["ArrowRight", "ArrowDown", "PageDown", " ", "Enter"].includes(e.key)) { show(current + 1); e.preventDefault(); }
    else if (["ArrowLeft", "ArrowUp", "PageUp", "Backspace"].includes(e.key)) { show(current - 1); e.preventDefault(); }
    else if (e.key === "Home") show(0);
    else if (e.key === "End") show(slides.length - 1);
    else if (e.key === "Escape") stop();
  });

  document.querySelector(".deck").addEventListener("click", (e) => {
    if (!document.body.classList.contains("presenting") || e.target.closest("a")) return;
    show(current + (e.clientX < window.innerWidth / 3 ? -1 : 1));
  });
})();
