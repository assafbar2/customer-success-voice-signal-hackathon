// Light motion: spotlight already CSS-animated; add cue-sheet stagger on scroll.
const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!prefersReduced) {
  const io = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      }
    },
    { threshold: 0.18 },
  );

  document.querySelectorAll(".flow li, .cues article").forEach((el, i) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(12px)";
    el.style.transition = `opacity 500ms ${i * 40}ms ease, transform 500ms ${i * 40}ms ease`;
    io.observe(el);
  });

  const style = document.createElement("style");
  style.textContent = `.is-in{opacity:1!important;transform:none!important}`;
  document.head.appendChild(style);
}
