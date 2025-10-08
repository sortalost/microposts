document.querySelectorAll('.pin-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const filename = this.dataset.filename;
        const termDiv = this.closest('.term');
        const statusDiv = document.getElementsByClassName('processing-status')[0];
        statusDiv.style.display = 'block';
        fetch(`/pin/${filename}`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                this.innerText = data.pin ? "[unpin]" : "[pin]";
                if (data.pin) {
                    termDiv.parentNode.prepend(termDiv);
                } else {
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
                if(data.pin){
                    if(!termDiv.querySelector('.pin-icon')){
                        const pinEl = document.createElement('span');
                        pinEl.className = 'pin-icon';
                        pinEl.title = 'Pinned';
                        pinEl.innerHTML = '&#128204;';
                        termDiv.appendChild(pinEl);
                    }
                } else {
                    const pinEl = termDiv.querySelector('.pin-icon');
                    if(pinEl) pinEl.remove();
                }
            } else {
                alert("Pin failed: " + (data.error || "unknown error"));
            }
        })
        .catch(err => {
            console.error(err);
            alert("Pin failed: network error");
        });
        statusDiv.style.display = 'none';
    });
});
