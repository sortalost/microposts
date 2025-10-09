function timeAgo(unixTimestamp) {
  const now = Math.floor(Date.now() / 1000);
  let seconds = now - unixTimestamp;
  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 }
  ];
  const isFuture = seconds < 0;
  seconds = Math.abs(seconds);
  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      const label = `${count} ${interval.label}${count !== 1 ? 's' : ''}`;
      return isFuture ? `${label} in the future` : `${label} ago`;
    }
  }
  return isFuture ? 'soon' : 'just now';
}


function updateTimeAgo() {
  document.querySelectorAll(".ago").forEach(el => {
    const timestamp = parseInt(el.dataset.timestamp, 10);
    if (!isNaN(timestamp)) {
      el.textContent = timeAgo(timestamp);
    }
  });
}

function adjustBodyPadding() {
    const footer = document.querySelector('.footer');
    if (!footer) return;
    const footerHeight = footer.offsetHeight;
    document.body.style.paddingBottom = footerHeight + 'px';
}

function deleteSetup() {
  document.querySelectorAll('.delete-link').forEach(link => {
      link.addEventListener('click', function(e) {
          e.preventDefault();
          if (!confirm("Sure??")) return;
          const statusDiv = document.getElementsByClassName('processing-status')[0];
          const filename = this.dataset.filename;
          statusDiv.style.display = 'block';
          fetch(`/delete/${filename}`, {
              method: 'POST',
              headers: {
                  'X-Requested-With': 'XMLHttpRequest'
              }
          })
          .then(res => res.json())
          .then(data => {
              if (data.success) {
                  this.closest('.term').remove();
              } else {
                  alert("Term removal failed: " + (data.error || "unknown error"));
              }
              statusDiv.style.display = 'none';
              window.location.reload()
          })
          .catch(err => {
              console.error(err);
              alert("Term removal failed: network or server error");
              statusDiv.style.display = 'none';
              window.location.reload()
          });
      });
  });
}

setInterval(updateTimeAgo, 1*60*1000);
window.addEventListener('DOMContentLoaded', updateTimeAgo);
window.addEventListener('DOMContentLoaded', deleteSetup);
window.addEventListener('DOMContentLoaded', adjustBodyPadding);
window.addEventListener('resize', adjustBodyPadding);

