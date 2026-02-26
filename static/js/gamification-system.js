/**
 * 🎮 ADVANCED GAMIFICATION SYSTEM
 * Professional 3D animations, parallax effects, and unlock celebrations
 */

class GamificationSystem {
    constructor() {
        this.particles = [];
        this.isAnimating = false;
        this.init();
    }

    init() {
        this.setupParallax();
        this.setupIntersectionObserver();
        this.setupStreakAnimation();
    }

    // 🛣 PARALLAX SCROLL EFFECT
    setupParallax() {
        const roadElements = document.querySelectorAll('.level-node, .badge-card');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            roadElements.forEach((el, index) => {
                const speed = 0.05 + (index * 0.01);
                const yPos = -(scrolled * speed);
                el.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // 🔍 INTERSECTION OBSERVER FOR LAZY ANIMATIONS
    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });

        document.querySelectorAll('.badge-card, .level-node').forEach(el => {
            observer.observe(el);
        });
    }

    // 🔥 STREAK FLAME ANIMATION
    setupStreakAnimation() {
        const streakFlame = document.querySelector('.streak-flame');
        if (!streakFlame) return;

        const streakDays = parseInt(streakFlame.dataset.days || 0);
        
        if (streakDays >= 30) {
            streakFlame.classList.add('legendary');
            this.createAuraEffect(streakFlame);
        } else if (streakDays >= 7) {
            streakFlame.classList.add('hot');
        } else if (streakDays >= 3) {
            streakFlame.classList.add('warm');
        }
    }

    // ✨ AURA EFFECT FOR LEGENDARY STREAK
    createAuraEffect(element) {
        const aura = document.createElement('div');
        aura.className = 'streak-aura';
        element.appendChild(aura);
    }

    // 💥 LEVEL UNLOCK ANIMATION
    async unlockLevel(levelNode) {
        if (this.isAnimating) return;
        this.isAnimating = true;

        // 1️⃣ Freeze background
        document.body.style.overflow = 'hidden';
        
        // 2️⃣ Create overlay
        const overlay = this.createOverlay();
        document.body.appendChild(overlay);

        // 3️⃣ Zoom and vibrate
        await this.animateZoomVibrate(levelNode);

        // 4️⃣ Particle explosion
        await this.createParticleExplosion(levelNode);

        // 5️⃣ Badge flip
        await this.animateBadgeFlip(levelNode);

        // 6️⃣ Confetti
        await this.createConfetti();

        // 7️⃣ Sound effect (optional)
        this.playUnlockSound();

        // Cleanup
        setTimeout(() => {
            overlay.remove();
            document.body.style.overflow = '';
            this.isAnimating = false;
        }, 1500);
    }

    createOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'unlock-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(8px);
            z-index: 9998;
            animation: fadeIn 0.3s ease;
        `;
        return overlay;
    }

    async animateZoomVibrate(element) {
        return new Promise(resolve => {
            element.style.animation = 'unlockZoomVibrate 0.6s ease';
            setTimeout(resolve, 600);
        });
    }

    async createParticleExplosion(element) {
        const rect = element.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const particleCount = 30;
        const particles = [];

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'unlock-particle';
            
            const angle = (Math.PI * 2 * i) / particleCount;
            const velocity = 100 + Math.random() * 100;
            const size = 4 + Math.random() * 8;
            
            particle.style.cssText = `
                position: fixed;
                left: ${centerX}px;
                top: ${centerY}px;
                width: ${size}px;
                height: ${size}px;
                background: linear-gradient(135deg, #ffd700, #ffed4e);
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                box-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
            `;
            
            document.body.appendChild(particle);
            particles.push({ element: particle, angle, velocity });
        }

        // Animate particles
        let frame = 0;
        const animate = () => {
            frame++;
            particles.forEach(({ element, angle, velocity }) => {
                const x = centerX + Math.cos(angle) * velocity * (frame / 10);
                const y = centerY + Math.sin(angle) * velocity * (frame / 10) + (frame * frame * 0.5);
                const opacity = Math.max(0, 1 - frame / 30);
                
                element.style.transform = `translate(${x - centerX}px, ${y - centerY}px)`;
                element.style.opacity = opacity;
            });

            if (frame < 30) {
                requestAnimationFrame(animate);
            } else {
                particles.forEach(({ element }) => element.remove());
            }
        };
        
        animate();
        return new Promise(resolve => setTimeout(resolve, 800));
    }

    async animateBadgeFlip(element) {
        const badge = element.querySelector('.badge-image');
        if (!badge) return;

        return new Promise(resolve => {
            badge.style.animation = 'badgeFlip3D 0.8s ease';
            setTimeout(resolve, 800);
        });
    }

    async createConfetti() {
        const confettiCount = 50;
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#ffd93d', '#6bcf7f'];

        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            
            const left = Math.random() * 100;
            const animationDelay = Math.random() * 0.5;
            const color = colors[Math.floor(Math.random() * colors.length)];
            
            confetti.style.cssText = `
                position: fixed;
                left: ${left}%;
                top: -10px;
                width: 10px;
                height: 10px;
                background: ${color};
                z-index: 9999;
                animation: confettiFall 2s ease-out ${animationDelay}s forwards;
                transform: rotate(${Math.random() * 360}deg);
            `;
            
            document.body.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 2500);
        }

        return new Promise(resolve => setTimeout(resolve, 1000));
    }

    playUnlockSound() {
        // Optional: Add sound effect
        if (window.unlockSoundEnabled) {
            const audio = new Audio('/static/sounds/unlock.mp3');
            audio.volume = 0.3;
            audio.play().catch(() => {});
        }
    }

    // 🔥 STREAK BREAK ANIMATION
    breakStreak() {
        const flame = document.querySelector('.streak-flame');
        if (!flame) return;

        flame.style.animation = 'flameFadeOut 1s ease forwards';
        
        // Show motivation popup
        setTimeout(() => {
            this.showMotivationPopup();
        }, 500);
    }

    showMotivationPopup() {
        const popup = document.createElement('div');
        popup.className = 'motivation-popup';
        popup.innerHTML = `
            <div class="motivation-content">
                <div class="crack-icon">💔</div>
                <h3>Don't lose momentum!</h3>
                <p>Start a new streak today</p>
                <button onclick="this.parentElement.parentElement.remove()">Let's Go!</button>
            </div>
        `;
        document.body.appendChild(popup);
    }

    // 🎯 NEXT REWARD PREVIEW
    showNextReward(currentLevel) {
        const nextLevel = currentLevel + 1;
        const preview = document.querySelector('.next-reward-preview');
        
        if (preview) {
            preview.style.animation = 'pulseGlow 2s ease-in-out infinite';
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    window.gamificationSystem = new GamificationSystem();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GamificationSystem;
}
