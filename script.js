"use strict";
document.documentElement.classList.add("js");
document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});
const toggle = document.querySelector(".menu-toggle");
const nav = document.getElementById("main-nav");
function closeMenu() {
  if (!toggle || !nav) return;
  toggle.setAttribute("aria-expanded", "false");
  nav.classList.remove("is-open");
}
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("is-open", open);
  });
  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      closeMenu();
      toggle.focus();
    }
  });
}
const copyButton = document.querySelector("[data-copy-email]");
const copyStatus = document.querySelector(".copy-status");
if (copyButton && copyStatus) {
  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(copyButton.dataset.copyEmail);
      copyStatus.textContent = "Email скопирован";
    } catch {
      copyStatus.textContent = "Не удалось скопировать. Выделите email или нажмите на него.";
    }
  });
}
// Движение «прогона»: блок запускается один раз, когда попадает в экран.
// Без JS или при prefers-reduced-motion всё видно сразу в конечном состоянии.
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
if (!reduceMotion && "IntersectionObserver" in window) {
  document.documentElement.classList.add("motion");
  const runState = document.querySelector(".run-state b");
  const finalState = runState ? runState.textContent : "";
  if (runState) runState.textContent = "running…";
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-run");
      observer.unobserve(entry.target);
      if (entry.target.classList.contains("run-summary") && runState) {
        window.setTimeout(() => { runState.textContent = finalState; }, 1500);
      }
    });
  }, { threshold: 0.35 });
  document.querySelectorAll(".run-summary, .tc, .chain").forEach((element) => observer.observe(element));
}
