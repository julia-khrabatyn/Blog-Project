function getCsrfToken() {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='))
        ?.split('=')[1];
}

function setupInlineCreate(modelName) {
    const btn = document.getElementById(`add-${modelName}-btn`);
    const form = document.getElementById(`new-${modelName}-form`);
    const input = document.getElementById(`new-${modelName}-input`);

    if (!btn || !form || !input) return;

    btn.addEventListener('click', () => {
        form.classList.remove('hidden');
        form.classList.add('flex');
    });

    document.getElementById(`cancel-${modelName}-btn`).addEventListener('click', () => {
        form.classList.remove('flex');
        form.classList.add('hidden');
        input.value = '';
    });

    document.getElementById(`save-${modelName}-btn`).addEventListener('click', () => {
        const title = input.value.trim();
        if (!title) return;

        fetch(`/core/inline-create/${modelName}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ 'title_en': title })
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    const select = document.getElementById(`id_${modelName}s`);
                    const option = new Option(data.text, data.id, true, true);
                    select.append(option);

                    form.classList.remove('flex');
                    form.classList.add('hidden');
                    input.value = '';
                } else {
                    alert('Error: ' + JSON.stringify(data.errors));
                }
            })
            .catch(err => console.error('Error:', err));
    });
}

setupInlineCreate('category');
setupInlineCreate('tag');