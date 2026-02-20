/* ============================================
   EduGuard - Authentication Logic
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    const page = document.body.dataset.page;

    if (page === 'login') initLogin();
    else if (page === 'register') initRegister();
    else if (page === 'forgot') initForgotPassword();
});

// ── Login ──
function initLogin() {
    const tabs = document.querySelectorAll('.role-tab');
    const form = document.getElementById('login-form');
    let selectedRole = 'student';

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            selectedRole = tab.dataset.role;
        });
    });

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        Validator.clearAll(form);

        const email = form.querySelector('#email');
        const password = form.querySelector('#password');
        let valid = true;

        if (!Validator.required(email.value)) {
            Validator.showError(email, 'Email is required');
            valid = false;
        } else if (!Validator.email(email.value)) {
            Validator.showError(email, 'Enter a valid email');
            valid = false;
        }

        if (!Validator.required(password.value)) {
            Validator.showError(password, 'Password is required');
            valid = false;
        } else if (!Validator.minLength(password.value, 6)) {
            Validator.showError(password, 'Password must be at least 6 characters');
            valid = false;
        }

        if (!valid) return;

        // Simulate login
        const btn = form.querySelector('.btn-primary');
        btn.innerHTML = '<span class="spinner"></span> Signing in...';
        btn.disabled = true;

        setTimeout(() => {
            const token = Auth.generateToken();
            const userData = {
                name: selectedRole === 'student' ? 'Priya Sharma' :
                    selectedRole === 'admin' ? 'Dr. Sunita Verma' : 'Gov Officer',
                email: email.value,
                role: selectedRole
            };

            Auth.setToken(token, selectedRole, userData);
            Toast.show('Login successful! Redirecting...', 'success');

            setTimeout(() => {
                if (selectedRole === 'student') window.location.href = 'student-dashboard.html';
                else if (selectedRole === 'admin') window.location.href = 'admin-dashboard.html';
                else window.location.href = 'gov-dashboard.html';
            }, 800);
        }, 1200);
    });
}

// ── Register ──
function initRegister() {
    const form = document.getElementById('register-form');
    const roleSelect = document.getElementById('role');
    const studentFields = document.getElementById('student-fields');
    const authorityFields = document.getElementById('authority-fields');

    if (roleSelect) {
        roleSelect.addEventListener('change', () => {
            const role = roleSelect.value;
            if (studentFields) studentFields.style.display = role === 'student' ? 'block' : 'none';
            if (authorityFields) authorityFields.style.display = (role === 'admin' || role === 'gov') ? 'block' : 'none';
        });
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        Validator.clearAll(form);

        const name = form.querySelector('#name');
        const email = form.querySelector('#email');
        const phone = form.querySelector('#phone');
        const password = form.querySelector('#password');
        const confirm = form.querySelector('#confirm-password');
        let valid = true;

        if (!Validator.required(name.value)) {
            Validator.showError(name, 'Full name is required');
            valid = false;
        }
        if (!Validator.required(email.value) || !Validator.email(email.value)) {
            Validator.showError(email, 'Enter a valid email');
            valid = false;
        }
        if (!Validator.required(phone.value) || !Validator.phone(phone.value)) {
            Validator.showError(phone, 'Enter a valid 10-digit phone number');
            valid = false;
        }
        if (!Validator.minLength(password.value, 6)) {
            Validator.showError(password, 'Password must be at least 6 characters');
            valid = false;
        }
        if (!Validator.match(password.value, confirm.value)) {
            Validator.showError(confirm, 'Passwords do not match');
            valid = false;
        }

        if (!valid) return;

        const btn = form.querySelector('.btn-primary');
        btn.innerHTML = '<span class="spinner"></span> Creating account...';
        btn.disabled = true;

        setTimeout(() => {
            Toast.show('Account created successfully! Please login.', 'success');
            setTimeout(() => { window.location.href = 'index.html'; }, 1200);
        }, 1500);
    });
}

// ── Forgot Password ──
function initForgotPassword() {
    const steps = document.querySelectorAll('.forgot-step');
    const dots = document.querySelectorAll('.step-dot');
    let currentStep = 0;

    window.nextStep = function (step) {
        if (step === 1) {
            const email = document.getElementById('reset-email');
            if (!Validator.required(email.value) || !Validator.email(email.value)) {
                Validator.showError(email, 'Enter a valid email');
                return;
            }
            Validator.clearError(email);
            Toast.show('OTP sent to your email!', 'info');
        }

        if (step === 2) {
            const inputs = document.querySelectorAll('.otp-container input');
            const otp = Array.from(inputs).map(i => i.value).join('');
            if (otp.length < 4) {
                Toast.show('Please enter the complete OTP', 'warning');
                return;
            }
        }

        if (step === 3) {
            const pass = document.getElementById('new-password');
            const confirm = document.getElementById('confirm-new-password');
            if (!Validator.minLength(pass.value, 6)) {
                Validator.showError(pass, 'Password must be at least 6 characters');
                return;
            }
            if (!Validator.match(pass.value, confirm.value)) {
                Validator.showError(confirm, 'Passwords do not match');
                return;
            }
            Toast.show('Password reset successful!', 'success');
            setTimeout(() => { window.location.href = 'index.html'; }, 1500);
            return;
        }

        steps[currentStep].style.display = 'none';
        currentStep = step;
        steps[currentStep].style.display = 'block';
        steps[currentStep].style.animation = 'fadeInUp 0.4s ease';

        dots.forEach((d, i) => {
            d.classList.remove('active', 'completed');
            if (i < currentStep) d.classList.add('completed');
            if (i === currentStep) d.classList.add('active');
        });
    };

    // OTP auto-focus
    document.querySelectorAll('.otp-container input').forEach((input, idx, inputs) => {
        input.addEventListener('input', (e) => {
            if (e.target.value && idx < inputs.length - 1) {
                inputs[idx + 1].focus();
            }
        });
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !e.target.value && idx > 0) {
                inputs[idx - 1].focus();
            }
        });
    });
}
