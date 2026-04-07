function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach((b, i) => {
    b.classList.toggle('active', (i === 0 && tab === 'login') || (i === 1 && tab === 'register'));
  });
  document.getElementById('login-section').classList.toggle('active', tab === 'login');
  document.getElementById('register-section').classList.toggle('active', tab === 'register');
}

// If there's a register error or success message, auto-switch to the register tab
var showRegister = document.getElementById('show-register').dataset.show === 'true';
if (showRegister) switchTab('register');