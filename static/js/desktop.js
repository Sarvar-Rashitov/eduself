// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');
const navLinks = document.querySelectorAll('.nav-link');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        const icon = mobileMenuBtn.querySelector('i');
        
        if (navMenu.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });
}

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (navMenu) {
            navMenu.classList.remove('active');
            const icon = mobileMenuBtn?.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });
});

// User Dropdown
const userDropdownBtn = document.getElementById('userDropdownBtn');
const userDropdown = document.getElementById('userDropdown');

if (userDropdownBtn && userDropdown) {
    userDropdownBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('active');
    });

    document.addEventListener('click', () => {
        userDropdown.classList.remove('active');
    });
}


// ===========================================
// AUTH MODAL FUNCTIONALITY - Chiroyli dizayn
// ===========================================

const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const loginModal = document.getElementById('loginModal');
const loginClose = document.getElementById('loginClose');
const authModalTabs = document.querySelectorAll('.auth-modal-tab');
const authFormContainers = document.querySelectorAll('.auth-modal-form-container');
const authModalContent = document.getElementById('authModalContent');
const authIllustration = document.getElementById('authIllustration');

// Function to open modal with specific tab
function openAuthModal(tab = 'signin') {
    if (!loginModal) return;
    
    loginModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Activate the correct tab
    authModalTabs.forEach(t => {
        if (t.getAttribute('data-tab') === tab) {
            t.click();
        }
    });
}

// Open login modal (Kirish tab)
if (loginBtn) {
    loginBtn.addEventListener('click', () => {
        openAuthModal('signin');
    });
}

// Open register modal (Ro'yxatdan o'tish tab)
if (registerBtn) {
    registerBtn.addEventListener('click', () => {
        openAuthModal('signup');
    });
}

// Auth required buttons (Testni boshlash va boshqalar)
// Mehmon foydalanuvchilar uchun modal ochadi
let pendingRedirectUrl = null;

// Hidden input yaratish yoki yangilash funksiyasi
function setNextInput(form, url) {
    if (!form) return;
    
    let nextInput = form.querySelector('input[name="next"]');
    if (!nextInput) {
        nextInput = document.createElement('input');
        nextInput.type = 'hidden';
        nextInput.name = 'next';
        form.appendChild(nextInput);
    }
    nextInput.value = url || '';
}

document.querySelectorAll('.auth-required-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const redirectUrl = this.getAttribute('data-redirect');
        
        // Redirect URL ni saqlash
        if (redirectUrl) {
            pendingRedirectUrl = redirectUrl;
            
            // Formalarga hidden input qo'shish
            const signinForm = document.getElementById('signinForm');
            const signupForm = document.getElementById('signupForm');
            
            setNextInput(signinForm, redirectUrl);
            setNextInput(signupForm, redirectUrl);
        }
        
        // Modal ochish
        openAuthModal('signin');
    });
});

// Modal yopilganda redirect URL ni tozalash
function clearPendingRedirect() {
    pendingRedirectUrl = null;
    const signinForm = document.getElementById('signinForm');
    const signupForm = document.getElementById('signupForm');
    
    setNextInput(signinForm, '');
    setNextInput(signupForm, '');
}

// Close login modal
if (loginClose) {
    loginClose.addEventListener('click', () => {
        loginModal.classList.remove('active');
        document.body.style.overflow = '';
        clearPendingRedirect();
    });
}

// Close modal when clicking outside
if (loginModal) {
    loginModal.addEventListener('click', (e) => {
        if (e.target === loginModal) {
            loginModal.classList.remove('active');
            document.body.style.overflow = '';
            clearPendingRedirect();
        }
    });
}

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && loginModal && loginModal.classList.contains('active')) {
        loginModal.classList.remove('active');
        document.body.style.overflow = '';
        clearPendingRedirect();
    }
});

// Switch between tabs with animation
authModalTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.getAttribute('data-tab');
        
        // Remove active class from all tabs and forms
        authModalTabs.forEach(t => t.classList.remove('active'));
        authFormContainers.forEach(form => form.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Show corresponding form and update left side content
        if (targetTab === 'signin') {
            document.getElementById('signinFormContainer')?.classList.add('active');
            // Update left side for login
            if (authModalContent) {
                authModalContent.innerHTML = `
                    <h1>Xush kelibsiz!</h1>
                    <p>EduSelf platformasiga kiring va bilimingizni sinang</p>
                `;
            }
            if (authIllustration) {
                authIllustration.className = 'fas fa-user-graduate';
            }
        } else {
            document.getElementById('signupFormContainer')?.classList.add('active');
            // Update left side for register
            if (authModalContent) {
                authModalContent.innerHTML = `
                    <h1>Bepul ro'yxatdan o'ting!</h1>
                    <p>EduSelf platformasiga qo'shiling va bilimingizni sinang</p>
                `;
            }
            if (authIllustration) {
                authIllustration.className = 'fas fa-rocket';
            }
        }
    });
});

// Toggle password visibility
document.querySelectorAll('.auth-toggle-password').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        const input = this.parentElement.querySelector('input');
        const icon = this.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });
});

// Forma submit ni ta'minlash
const signinForm = document.getElementById('signinForm');
const signupForm = document.getElementById('signupForm');

if (signinForm) {
    signinForm.addEventListener('submit', function(e) {
        // Forma submit bo'lishiga ruxsat berish
        console.log('Signin form submitting...');
    });
}

if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
        // Forma submit bo'lishiga ruxsat berish
        console.log('Signup form submitting...');
    });
}

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            const headerOffset = 80;
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Header Scroll Effect
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (header) {
        if (currentScroll > 100) {
            header.style.padding = '0.5rem 0';
            header.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.padding = '1rem 0';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    }
});


// ===========================================
// AI ASSISTANT FUNCTIONALITY
// ===========================================

// AI Responses Database
const aiResponses = {
    'matematika': 'Matematika bo\'yicha ko\'plab test savollarimiz bor. Algebra, Geometriya, Trigonometriya va boshqa mavzular mavjud. Fanlar bo\'limiga o\'ting! 📝',
    'test': 'Bizda Matematika, Fizika, Kimyo, Ingliz tili va boshqa fanlar bo\'yicha testlar mavjud. Fanlar bo\'limiga o\'ting! 📚',
    'sertifikat': 'Milliy sertifikat olish uchun testlarni muvaffaqiyatli tugatishingiz kerak. Sertifikat davlat tomonidan tan olingan! 🎓',
    'universitet': 'Platformamizda ko\'plab davlat va nodavlat universitetlari haqida ma\'lumot bor. Muassasalar bo\'limiga o\'ting! 🎯',
    'ingliz': 'Til o\'rgatish markazlari haqida ma\'lumot beramiz. Resurslar bo\'limidan video va audio darslarni topishingiz mumkin! 🗣',
    'yordam': 'Sizga qanday yordam kerak? Testlar, Sertifikatlar, Muassasalar yoki boshqa ma\'lumotlar kerakmi? 💬',
    'salom': 'Salom! Sizga qanday yordam bera olaman? 😊',
    'assalomu': 'Va aleykum assalom! Xush kelibsiz! Nimada yordam kerak? 🤝',
    'rahmat': 'Arzimaydi! Yana savollaringiz bo\'lsa, so\'rang! 😊',
    'maktab': 'Davlat va nodavlat maktablari haqida ma\'lumot beramiz. Muassasalar bo\'limiga o\'ting! 🏫',
    'kurs': 'Bizda turli xil online kurslar mavjud. Kurslar bo\'limiga o\'ting! 📖',
    'imtihon': 'Mock imtihonlar orqali haqiqiy imtihonga tayyorlaning. Imtihonlar bo\'limiga o\'ting! 📋',
    'qanday': 'Platformadan foydalanish oson! Kerakli bo\'limni tanlang va boshlang. ✨'
};

// Function to get AI response
function getAIResponse(question) {
    const lowerQuestion = question.toLowerCase();
    
    // Check for keywords in question
    for (let keyword in aiResponses) {
        if (lowerQuestion.includes(keyword)) {
            return aiResponses[keyword];
        }
    }
    
    // Default response
    return 'Savolingiz uchun rahmat! Iltimos, aniqroq savol bering yoki quyidagi mavzulardan birini tanlang: Fanlar, Sertifikatlar, Imtihonlar, Muassasalar, Kurslar. 🤔';
}

// Function to add message to chat
function addMessage(text, isUser = false, containerId = 'aiChatMessages') {
    const messagesContainer = document.getElementById(containerId);
    const floatMessagesContainer = document.getElementById('aiFloatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-message ${isUser ? 'ai-user' : 'ai-bot'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'ai-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';
    
    const content = document.createElement('div');
    content.className = 'ai-message-content';
    
    const p = document.createElement('p');
    p.textContent = text;
    
    content.appendChild(p);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    // Add to both chat containers
    if (messagesContainer) {
        messagesContainer.appendChild(messageDiv.cloneNode(true));
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    if (floatMessagesContainer && containerId !== 'aiFloatMessages') {
        floatMessagesContainer.appendChild(messageDiv.cloneNode(true));
        floatMessagesContainer.scrollTop = floatMessagesContainer.scrollHeight;
    }
}

// Handle chat input - Main chat
const aiChatInput = document.getElementById('aiChatInput');
const aiSendBtn = document.getElementById('aiSendBtn');

if (aiSendBtn) {
    aiSendBtn.addEventListener('click', () => {
        const message = aiChatInput.value.trim();
        if (message) {
            addMessage(message, true);
            aiChatInput.value = '';
            
            // Simulate AI thinking
            setTimeout(() => {
                const response = getAIResponse(message);
                addMessage(response, false);
            }, 500);
        }
    });
}

if (aiChatInput) {
    aiChatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            aiSendBtn.click();
        }
    });
}

// Handle chat input - Floating chat
const aiFloatInput = document.getElementById('aiFloatInput');
const aiFloatSendBtn = document.getElementById('aiFloatSendBtn');

if (aiFloatSendBtn) {
    aiFloatSendBtn.addEventListener('click', () => {
        const message = aiFloatInput.value.trim();
        if (message) {
            addMessage(message, true, 'aiFloatMessages');
            aiFloatInput.value = '';
            
            // Simulate AI thinking
            setTimeout(() => {
                const response = getAIResponse(message);
                addMessage(response, false, 'aiFloatMessages');
            }, 500);
        }
    });
}

if (aiFloatInput) {
    aiFloatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            aiFloatSendBtn.click();
        }
    });
}

// Handle suggestion buttons
const suggestionBtns = document.querySelectorAll('.ai-suggestion-btn');

suggestionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const question = btn.getAttribute('data-question');
        addMessage(question, true);
        
        setTimeout(() => {
            const response = getAIResponse(question);
            addMessage(response, false);
        }, 500);
    });
});

// Floating AI Button Toggle
const aiFloatBtn = document.getElementById('aiFloatBtn');
const aiChatWindow = document.getElementById('aiChatWindow');
const aiMinimizeBtn = document.getElementById('aiMinimizeBtn');

if (aiFloatBtn) {
    aiFloatBtn.addEventListener('click', () => {
        aiChatWindow.classList.toggle('active');
    });
}

if (aiMinimizeBtn) {
    aiMinimizeBtn.addEventListener('click', () => {
        aiChatWindow.classList.remove('active');
    });
}

// Close chat when clicking outside
document.addEventListener('click', (e) => {
    if (aiChatWindow && aiFloatBtn) {
        if (!aiChatWindow.contains(e.target) && !aiFloatBtn.contains(e.target)) {
            aiChatWindow.classList.remove('active');
        }
    }
});

// Scroll Animation - Elements fade in when they come into view
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections
const animatedElements = document.querySelectorAll('.card, .stat-card, .university-card, .ai-feature-card, .leaderboard-item, .user-stat-card');

animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Console Welcome Message
console.log('%c🎓 EduSelf Platform', 'color: #6366f1; font-size: 24px; font-weight: bold;');
console.log('%cO\'zbekistonning ta\'lim platformasi', 'color: #8b5cf6; font-size: 14px;');

// Initialize everything when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('EduSelf Desktop yuklandi! ✅');
});
