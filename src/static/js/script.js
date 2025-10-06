
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
  
  setInterval(updateTimeAgo, 10*60*1000);
  window.addEventListener('DOMContentLoaded', adjustBodyPadding);
  window.addEventListener('DOMContentLoaded', updateTimeAgo);
  window.addEventListener('resize', adjustBodyPadding);
