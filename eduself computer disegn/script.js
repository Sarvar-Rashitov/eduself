// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navMenu = document.getElementById('navMenu');
const navLinks = document.querySelectorAll('.nav-link');

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

// Close mobile menu when clicking on a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const icon = mobileMenuBtn.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    });
});

// ===========================================
// LOGIN MODAL FUNCTIONALITY
// ===========================================

const loginBtn = document.getElementById('loginBtn');
const heroLoginBtn = document.getElementById('heroLoginBtn');
const loginModal = document.getElementById('loginModal');
const loginClose = document.getElementById('loginClose');
const loginTabs = document.querySelectorAll('.login-tab');
const loginForms = document.querySelectorAll('.login-form');

// Open login modal
if (loginBtn) {
    loginBtn.addEventListener('click', () => {
        loginModal.classList.add('active');
    });
}

if (heroLoginBtn) {
    heroLoginBtn.addEventListener('click', () => {
        loginModal.classList.add('active');
    });
}

// Close login modal
if (loginClose) {
    loginClose.addEventListener('click', () => {
        loginModal.classList.remove('active');
    });
}

// Close modal when clicking outside
loginModal.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        loginModal.classList.remove('active');
    }
});

// Switch between tabs
loginTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.getAttribute('data-tab');
        
        // Remove active class from all tabs and forms
        loginTabs.forEach(t => t.classList.remove('active'));
        loginForms.forEach(form => form.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Show corresponding form
        if (targetTab === 'signin') {
            document.getElementById('signinForm').classList.add('active');
        } else {
            document.getElementById('signupForm').classList.add('active');
        }
    });
});

// Handle form submissions
const signinForm = document.getElementById('signinForm');
const signupForm = document.getElementById('signupForm');

if (signinForm) {
    signinForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Tizimga kirish funksiyasi ishlab chiqilmoqda...');
        loginModal.classList.remove('active');
    });
}

if (signupForm) {
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Ro\'yxatdan o\'tish funksiyasi ishlab chiqilmoqda...');
        loginModal.classList.remove('active');
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
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        header.style.padding = '0.5rem 0';
        header.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.1)';
    } else {
        header.style.padding = '1rem 0';
        header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
    
    lastScroll = currentScroll;
});

// Tabs Functionality
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        
        // Remove active class from all tabs and contents
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked tab and corresponding content
        btn.classList.add('active');
        document.getElementById(targetTab).classList.add('active');
    });
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
const animatedElements = document.querySelectorAll('.card, .stat-card, .resource-card, .school-card, .university-card, .center-card, .feature, .ai-feature-card');

animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Counter Animation for Stats
const counters = document.querySelectorAll('.stat-card h3');
const speed = 200;

const animateCounter = (counter) => {
    const target = counter.innerText;
    const numericTarget = parseInt(target.replace(/\D/g, ''));
    const suffix = target.replace(/[0-9]/g, '');
    
    let count = 0;
    const increment = numericTarget / speed;
    
    const updateCount = () => {
        count += increment;
        
        if (count < numericTarget) {
            counter.innerText = Math.ceil(count) + suffix;
            requestAnimationFrame(updateCount);
        } else {
            counter.innerText = target;
        }
    };
    
    updateCount();
};

// Trigger counter animation when stats section is visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            counters.forEach(counter => {
                animateCounter(counter);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.stats');
if (statsSection) {
    statsObserver.observe(statsSection);
}

// Button Click Effects with Ripple
const buttons = document.querySelectorAll('.btn');

buttons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});

// Active Link Highlighting on Scroll
const sections = document.querySelectorAll('section[id]');

const highlightNavLink = () => {
    const scrollY = window.pageYOffset;
    
    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
};

window.addEventListener('scroll', highlightNavLink);

// Parallax Effect for Hero Section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroAnimation = document.querySelector('.hero-animation');
    
    if (heroAnimation) {
        heroAnimation.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// ===========================================
// AI ASSISTANT FUNCTIONALITY
// ===========================================

// AI Responses Database
const aiResponses = {
    'matematika': 'Matematika bo\'yicha 1000+ test savolimiz bor. Algebra, Geometriya, Trigonometriya va boshqa mavzular mavjud. Testlar bo\'limiga o\'ting! 📝',
    'test': 'Bizda Matematika, Fizika, Kimyo, Ingliz tili va boshqa fanlar bo\'yicha testlar mavjud. Testlar bo\'limiga o\'ting! 📚',
    'sertifikat': 'Milliy sertifikat olish uchun testlarni muvaffaqiyatli tugatishingiz kerak. Sertifikat davlat tomonidan tan olingan! 🎓',
    'universitet': 'Platformamizda 100+ davlat va nodavlat universitetlari haqida ma\'lumot bor. Universitetlar bo\'limiga o\'ting! 🎯',
    'ingliz': '200+ til o\'rgatish markazlari haqida ma\'lumot beramiz. Resurslar bo\'limidan video va audio darslarni topishingiz mumkin! 🗣',
    'yordam': 'Sizga qanday yordam kerak? Testlar, O\'yinlar, Resurslar, Sertifikat yoki boshqa ma\'lumotlar kerakmi? 💬',
    'salom': 'Salom! Sizga qanday yordam bera olaman? 😊',
    'assalomu': 'Va aleykum assalom! Xush kelibsiz! Nimada yordam kerak? 🤝',
    'rahmat': 'Arzimaydi! Yana savollaringiz bo\'lsa, so\'rang! 😊',
    'maktab': 'Davlat va nodavlat maktablari haqida ma\'lumot beramiz. 150+ maktab platformamizda ro\'yxatga olingan! 🏫',
    'o\'yin': 'Bizda matematik jumboq, xotira o\'yini, geografiya kviz va boshqa o\'yinlar bor. O\'yinlar orqali o\'rganish 5 barobar samaraliroq! 🎮',
    'qanday': 'Platformadan foydalanish oson! Kerakli bo\'limni tanlang va boshlang. Barcha materiallar bepul! ✨'
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
    return 'Savolingiz uchun rahmat! Iltimos, aniqroq savol bering yoki quyidagi mavzulardan birini tanlang: Testlar, O\'yinlar, Resurslar, Sertifikat, Universitetlar, Maktablar. 🤔';
}

// Function to add message to chat
function addMessage(text, isUser = false) {
    const messagesContainer = document.getElementById('aiChatMessages');
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
    
    if (floatMessagesContainer) {
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
            addMessage(message, true);
            aiFloatInput.value = '';
            
            // Simulate AI thinking
            setTimeout(() => {
                const response = getAIResponse(message);
                addMessage(response, false);
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

// Console Welcome Message
console.log('%c🎓 Edu Platform', 'color: #6366f1; font-size: 24px; font-weight: bold;');
console.log('%cO\'zbekistonning eng yirik online ta\'lim platformasi', 'color: #8b5cf6; font-size: 14px;');
console.log('%cDasturchi: Edu Team', 'color: #ec4899; font-size: 12px;');
console.log('%c✨ Kirish tugmasini bosing!', 'color: #10b981; font-size: 12px;');

// Performance optimization: Debounce scroll events
const debounce = (func, wait = 10) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

window.addEventListener('scroll', debounce(() => {
    highlightNavLink();
}, 10));

// Initialize everything when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Edu Platform yuklandi! ✅');
    
    // Add loading animation complete class
    document.body.classList.add('loaded');
    
    // Initial welcome message in AI chat
    setTimeout(() => {
        console.log('AI Yordamchi tayyor! 🤖');
    }, 1000);
});

// Loading animation
const loadingStyle = document.createElement('style');
loadingStyle.textContent = `
    body {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    body.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(loadingStyle);