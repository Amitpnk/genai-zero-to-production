// Copy buttons: copy the command or code block next to the button.
document.querySelectorAll(".copy").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const src = btn.parentElement.querySelector("code, pre");
    try {
      await navigator.clipboard.writeText(src.textContent.trim());
      btn.textContent = "Copied";
      btn.classList.add("done");
    } catch {
      btn.textContent = "Select & copy";
    }
    setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("done"); }, 1500);
  });
});
