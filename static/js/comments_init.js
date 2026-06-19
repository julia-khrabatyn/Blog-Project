document.addEventListener('DOMContentLoaded', () => {
    const postId = document.body.dataset.postId;

    setupInlineCreate('comment', {
        url: `/comments/create/${postId}/`,
        buildPayload: (text) => ({ text }),
        onSuccess: (data) => {
            const list = document.getElementById('comments-list');
            const item = document.createElement('div');
            item.className = 'comment-item p-3 border-b';
            item.textContent = data.text;
            list.prepend(item);
        }
    });
});
