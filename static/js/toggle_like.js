document.addEventListener("change", async (event) => {
    if (!event.target.classList.contains("like-checkbox")) return;

    const checkbox = event.target;
    const url = checkbox.getAttribute("data-url");

    console.log("URL:", url);

    if (!url) {
        console.error("Missing data-url on checkbox!");
        return;
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector(
                    'meta[name="csrf-token"]'
                ).content,
            },
        });

        const data = await response.json();
        checkbox.checked = data.liked;

    } catch (error) {
        console.error("Like error:", error);
        checkbox.checked = !checkbox.checked;
    }
});