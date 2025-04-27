// Main JavaScript for Audio Extractor

document.addEventListener('DOMContentLoaded', function() {
  // Register service worker for better mobile experience
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js')
      .then(function(registration) {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
      })
      .catch(function(error) {
        console.log('ServiceWorker registration failed: ', error);
      });
  }

  // Mobile-specific optimizations
  applyMobileOptimizations();
  
  // Setup form validation and UX improvements
  setupFormHandling();
  
  // Setup better download handling
  setupDownloadHandling();
});

// Apply mobile-specific optimizations
function applyMobileOptimizations() {
  // Fix viewport height on mobile browsers
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
  
  window.addEventListener('resize', () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  });
  
  // Prevent zooming on form inputs in iOS
  document.addEventListener('touchmove', function(e) {
    if (e.scale !== 1) {
      e.preventDefault();
    }
  }, { passive: false });
  
  // Better scrolling on iOS
  document.addEventListener('touchstart', function() {}, { passive: true });
}

// Setup form handling and validation
function setupFormHandling() {
  const videoInput = document.getElementById('video');
  const partsInput = document.getElementById('parts');
  const submitButton = document.querySelector('button[type="submit"]');
  
  if (videoInput) {
    // Better file input handling for mobile
    videoInput.addEventListener('change', function() {
      if (this.files.length > 0) {
        // Check file size
        const fileSizeMB = this.files[0].size / (1024 * 1024);
        if (fileSizeMB > 500) {
          alert('Warning: The selected file is ' + fileSizeMB.toFixed(2) + 'MB. Large files may take longer to upload and process on mobile networks.');
        }
        
        // Enable submit button if file is selected
        if (submitButton) {
          submitButton.removeAttribute('disabled');
        }
      }
    });
  }
  
  if (partsInput) {
    // Ensure the parts input is a valid number
    partsInput.addEventListener('input', function() {
      const value = parseInt(this.value, 10);
      if (isNaN(value) || value < 1) {
        this.value = 1;
      } else if (value > 100) {
        this.value = 100;
      }
    });
  }
}

// Setup download handling
function setupDownloadHandling() {
  const downloadLinks = document.querySelectorAll('.list-group-item');
  
  if (downloadLinks.length === 1 && window.innerWidth < 768) {
    // Auto-trigger download on mobile for single files
    setTimeout(function() {
      alert('Download will start automatically. If it doesn\'t, tap the Download button.');
      downloadLinks[0].click();
    }, 1500);
  }
  
  // Add download progress indicators
  downloadLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const fileName = this.querySelector('.file-name').textContent;
      const badge = this.querySelector('.download-badge');
      
      badge.innerHTML = 'Downloading...';
      
      // Restore after a delay (since we can't track actual downloads)
      setTimeout(() => {
        badge.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg> Download';
      }, 3000);
    });
  });
} 