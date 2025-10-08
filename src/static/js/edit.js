document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('editModal');
    const textarea = document.getElementById('editTextarea');
    const filenameInput = document.getElementById('editFilename');
    const datetimeInput = document.getElementById('editDatetime');
    const form = document.getElementById('editForm');
    const cancelBtn = document.getElementById('editCancel');
    const statusDiv = document.getElementsByClassName('processing-status')[0];
    statusDiv.style.display = 'inline';
    document.querySelectorAll('.edit-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const termDiv = this.closest('.term');
            const descSpan = termDiv.querySelector('.description');
            const displayDt = termDiv.querySelector('.display-datetime')?.dataset.timestamp;
            const filename = this.dataset.filename;
            textarea.value = descSpan ? descSpan.innerText : '';
            filenameInput.value = filename;
            if (displayDt) {
                const dt = new Date(parseInt(displayDt) * 1000);
                const localStr = dt.toISOString().slice(0,16);
                datetimeInput.value = localStr;
            }
            modal.currentTermDiv = termDiv;
            modal.style.display = 'flex';
        });
    });
    cancelBtn.addEventListener('click', () => modal.style.display = 'none');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const filename = filenameInput.value;
        const newDesc = textarea.value;
        const newDt = datetimeInput.value;
        fetch(`/dashboard/edit/${filename}`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams({ 
                description: newDesc,
                display_datetime: newDt
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const termDiv = modal.currentTermDiv;
                const descSpan = termDiv.querySelector('.description');
                if (descSpan) descSpan.innerText = data.description;
                const metaSpan = termDiv.querySelector('.meta');
                if (metaSpan && data.display_datetime) {
                    const parts = metaSpan.innerHTML.split('|');
                    parts[1] = ` ${data.display_datetime} `;
                    metaSpan.innerHTML = parts.join('|');
                }
                modal.style.display = 'none';
                statusDiv.style.display = 'none';
            } else {
                alert("Edit failed: " + (data.error || "unknown error"));
                statusDiv.style.display = 'none';
            }
        })
        .catch(err => {
            console.error(err);
            alert("Edit failed: network or server error");
            statusDiv.style.display = 'none';
        });
    });
});
