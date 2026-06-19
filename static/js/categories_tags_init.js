document.addEventListener('DOMContentLoaded', () => {
    setupInlineCreate('category', {
        url: '/core/inline-create/category/',
        buildPayload: (title) => ({ title_en: title }),
        onSuccess: (data) => {
            const select = document.getElementById('id_categories');
            select.append(new Option(data.text, data.id, true, true));
        }
    });

    setupInlineCreate('tag', {
        url: '/core/inline-create/tag/',
        buildPayload: (title) => ({ title_en: title }),
        onSuccess: (data) => {
            const select = document.getElementById('id_tags');
            select.append(new Option(data.text, data.id, true, true));
        }
    });
});