document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('editModal');
    const textarea = document.getElementById('editTextarea');
    const filenameInput = document.getElementById('editFilename');
    const form = document.getElementById('editForm');
    const cancelBtn = document.getElementById('editCancel');

    document.querySelectorAll('.edit-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const termDiv = this.closest('.term');
            const descSpan = termDiv.querySelector('.description');
            const filename = this.dataset.filename;

            textarea.value = descSpan ? descSpan.innerText : '';
            filenameInput.value = filename;
            modal.currentTermDiv = termDiv;
            modal.style.display = 'flex';
        });
    });

    cancelBtn.addEventListener('click', () => modal.style.display = 'none');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const filename = filenameInput.value;
        const newDesc = textarea.value;

        fetch(`/dashboard/edit/${filename}`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams({ description: newDesc })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const termDiv = modal.currentTermDiv;
                const descSpan = termDiv.querySelector('.description');
                if (descSpan) descSpan.innerText = data.description;
                modal.style.display = 'none';
            } else {
                alert("Edit failed: " + (data.error || "unknown error"));
            }
        })
        .catch(err => {
            console.error(err);
            alert("Edit failed: network or server error");
        });
    });
});
