
function timeAgo(unixTimestamp) {
  const seconds = Math.floor(Date.now() / 1000) - unixTimestamp;
  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 }
  ];
  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      return `${count} ${interval.label}${count !== 1 ? 's' : ''} ago`;
    }
  }
  return 'just now';
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
          if (!confirm("Sure?")) return;
          const statusDiv = document.getElementsByClassName('delete-status')[0];
          statusDiv.style.display = 'inline';
          const filename = this.dataset.filename;
          fetch(`/dashboard/delete/${filename}`, {
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
                  statusDiv.style.display = 'none';
              }
          })
          .catch(err => {
              console.error(err);
              alert("Term removal failed: network or server error");
              statusDiv.style.display = 'none';
          });
      });
  });
}

setInterval(updateTimeAgo, 1*60*1000);
window.addEventListener('DOMContentLoaded', updateTimeAgo);
window.addEventListener('DOMContentLoaded', deleteSetup);
window.addEventListener('DOMContentLoaded', adjustBodyPadding);
window.addEventListener('resize', adjustBodyPadding);
