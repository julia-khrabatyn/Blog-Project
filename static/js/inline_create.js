function getCsrfToken() {
    return document.cookie.split(';')
        .find(c => c.trim().startsWith('csrftoken='))
        ?.split('=')[1];
}

function setupInlineCreate(modelName, options = {}) {
    const {
        url,
        buildPayload,
        onSuccess,
    } = options;

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
        const value = input.value.trim();
        if (!value) return;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(buildPayload(value))
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'ok') {
                    onSuccess(data, form, input);

                    form.classList.remove('flex');
                    form.classList.add('hidden');
                    input.value = '';

                    const existingError = form.querySelector('.error-msg');
                    if (existingError) existingError.remove();
                } else {
                    let errorDiv = form.querySelector('.error-msg');
                    if (!errorDiv) {
                        errorDiv = document.createElement('p');
                        errorDiv.className = 'error-msg text-xs text-red-500 mt-1';
                        form.appendChild(errorDiv);
                    }
                    const firstError = Object.values(data.errors)[0];
                    errorDiv.textContent = firstError;
                }
            })
            .catch(err => console.error('Error:', err));
    });
}