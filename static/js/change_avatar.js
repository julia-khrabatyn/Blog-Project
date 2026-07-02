window.addEventListener("load", function () {

    const input = document.getElementById("id_avatar");
    const avatar = document.querySelector(".author-avatar-img");

    console.log(input, avatar);

    if (!input || !avatar) return;

    input.addEventListener("change", async function () {

        console.log("CHANGE FIRED");

        const file = input.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("avatar", file);

        const response = await fetch("/accounts/admin/avatar/update/", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
            body: formData
        });

        const data = await response.json();
        console.log(data);

        if (data.status === "ok") {
            avatar.src = data.avatar_url + "?t=" + Date.now();
        }
    });
});