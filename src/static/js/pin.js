document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.pin-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const filename = this.dataset.filename;
            const termDiv = this.closest('.term');

            fetch(`/dashboard/pin/${filename}`, {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    this.innerText = data.pin ? "[unpin]" : "[pin]";
                    // move pinned item to top
                    if (data.pin) termDiv.parentNode.prepend(termDiv);
                    else {
                        // re-sort unpinned by timestamp
                        const allTerms = Array.from(termDiv.parentNode.querySelectorAll('.term'));
                        allTerms.sort((a,b) => {
                            const aTime = parseInt(a.querySelector('.display-datetime').dataset.timestamp);
                            const bTime = parseInt(b.querySelector('.display-datetime').dataset.timestamp);
                            const aPin = a.querySelector('.pin-link').innerText === "[unpin]" ? 1 : 0;
                            const bPin = b.querySelector('.pin-link').innerText === "[unpin]" ? 1 : 0;
                            if(aPin !== bPin) return bPin - aPin;
                            return bTime - aTime;
                        });
                        allTerms.forEach(t => termDiv.parentNode.appendChild(t));
                    }
                } else {
                    alert("Pin failed: " + (data.error || "unknown error"));
                }
            })
            .catch(err => {
                console.error(err);
                alert("Pin failed: network error");
            });
        });
    });
});
