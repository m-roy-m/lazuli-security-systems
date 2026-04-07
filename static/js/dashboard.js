// Toggle dropdown nav items
document.querySelectorAll('.nav-link[data-toggle]').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var parent = this.closest('.nav-item');
    var wasOpen = parent.classList.contains('open');
    // Close all
    document.querySelectorAll('.nav-item').forEach(function(i) { i.classList.remove('open'); });
    if (!wasOpen) parent.classList.add('open');
  });
});

// Mark active nav link based on current URL
var path = window.location.pathname;
document.querySelectorAll('.nav-dropdown a').forEach(function(a) {
  if (a.getAttribute('href') === path) {
    a.classList.add('active');
    a.closest('.nav-item').classList.add('open');
  }
});
document.querySelectorAll('.nav-link[href]').forEach(function(a) {
  if (a.getAttribute('href') === path) a.classList.add('active');
});