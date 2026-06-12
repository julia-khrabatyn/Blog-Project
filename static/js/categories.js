document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("category-modal");
    const openBtn = document.getElementById("open-category-modal");
    const closeBtn = document.getElementById("close-category-modal");
    const saveBtn = document.getElementById("save-category");
    const input = document.getElementById("cat-title");
    const lang = document.documentElement.lang || 'en';

    if (!modal) {
        console.error("Modal not found");
        return;
    }

    const url = modal.dataset.url;

    // OPEN MODAL
    if (openBtn) {
        openBtn.addEventListener("click", () => {
            modal.classList.remove("hidden");
        });
    }

    // CLOSE MODAL
    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            modal.classList.add("hidden");
        });
    }

    // SAVE CATEGORY
    if (saveBtn) {
        saveBtn.addEventListener("click", async () => {

            const title = input.value.trim();

            if (!title) {
                alert("Title is required");
                return;
            }

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    body: new URLSearchParams({
                        [`title_${lang}`]: title
                    })
                });

                const data = await response.json();

                if (data.error) {
                    alert(data.error);
                    return;
                }

                const select = document.querySelector("select[name='categories']");

                if (select) {
                    const option = document.createElement("option");
                    option.value = data.id;
                    option.textContent = data.title;
                    option.selected = true;

                    select.appendChild(option);
                }

                input.value = "";
                modal.classList.add("hidden");

            } catch (err) {
                console.error(err);
                alert("Something went wrong");
            }
        });
    }

    // COOKIE HELPER
    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');

            for (let cookie of cookies) {
                cookie = cookie.trim();

                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }

});