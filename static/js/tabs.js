document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".tab-btn");
    const panels = document.querySelectorAll(".tab-panel");

    buttons.forEach((btn) => {
        btn.addEventListener("click", () => {
            buttons.forEach((b) => {
                b.classList.remove("border-sky-600", "text-sky-600");
                b.classList.add("border-transparent", "text-gray-500");
            });
            btn.classList.add("border-sky-600", "text-sky-600");
            btn.classList.remove("border-transparent", "text-gray-500");

            panels.forEach((p) => p.classList.add("hidden"));
            document
                .querySelector(`[data-panel="${btn.dataset.tab}"]`)
                .classList.remove("hidden");
        });
    });
});