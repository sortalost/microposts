document.addEventListener('click', function(e){
    const target = e.target;
    if(!target.classList.contains('pin-link')) return;
    e.preventDefault();
    const filename = target.dataset.filename;
    const termDiv = target.closest('.term');
    const statusDiv = document.getElementsByClassName('processing-status')[0];
    statusDiv.style.display = 'block';
    fetch(`/pin/${filename}`, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => {
        statusDiv.style.display = 'none';
        if(data.success){
            // Update link text
            target.innerText = data.pin ? "[unpin]" : "[pin]";
            if(data.pin){
                if(!termDiv.querySelector('.pin-icon')){
                    const pinEl = document.createElement('span');
                    pinEl.className = 'pin-icon';
                    pinEl.title = 'Pinned';
                    pinEl.innerHTML = '<img style="height:2em" src="/static/images/pin.gif">';
                    termDiv.style.position = "relative";
                    termDiv.appendChild(pinEl);
                }
                termDiv.parentNode.prepend(termDiv);
            } else {
                const pinEl = termDiv.querySelector('.pin-icon');
                if(pinEl) pinEl.remove();
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
        statusDiv.style.display = 'none';
        console.error(err);
        alert("Pin failed: network error");
    });
});
