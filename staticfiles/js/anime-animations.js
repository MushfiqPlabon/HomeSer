// anime-animations.js - Anime.js implementation for HomeSer

// Initialize Anime.js when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations
    initServiceCardAnimations();
    initButtonAnimations();
    initHeaderAnimations();
    initHeroSectionAnimations();
    initValuePropAnimations();
    initFormAnimations();
    initNotificationAnimations();
    initCartAnimations();
    initReviewAnimations();
    
    // Run staggered animations
    runStaggeredAnimations();
});

// Service card hover animations
function initServiceCardAnimations() {
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        // Mouse enter animation
        card.addEventListener('mouseenter', function() {
            anime({
                targets: this,
                translateY: -10,
                boxShadow: [
                    '0 8px 32px rgba(0, 0, 0, 0.3)',
                    '0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px var(--neon-green), 0 0 30px rgba(57, 255, 20, 0.2)'
                ],
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
        
        // Mouse leave animation
        card.addEventListener('mouseleave', function() {
            anime({
                targets: this,
                translateY: 0,
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.05)',
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
        
        // Click press animation
        card.addEventListener('mousedown', function() {
            anime({
                targets: this,
                scale: 0.98,
                duration: 150,
                easing: 'easeOutQuad'
            });
        });
        
        card.addEventListener('mouseup', function() {
            anime({
                targets: this,
                scale: 1,
                duration: 150,
                easing: 'easeOutQuad'
            });
        });
    });
}

// Button animations
function initButtonAnimations() {
    const buttons = document.querySelectorAll('.glow-button');
    
    buttons.forEach(button => {
        // Hover animation
        button.addEventListener('mouseenter', function() {
            anime({
                targets: this,
                translateY: -2,
                scale: 1.02,
                duration: 200,
                easing: 'easeOutQuad'
            });
            
            // Glow effect
            anime({
                targets: this,
                boxShadow: [
                    getComputedStyle(this).boxShadow,
                    '0 0 15px currentColor, 0 0 30px rgba(255, 255, 255, 0.5), 0 0 45px currentColor'
                ],
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
        
        // Leave animation
        button.addEventListener('mouseleave', function() {
            anime({
                targets: this,
                translateY: 0,
                scale: 1,
                duration: 200,
                easing: 'easeOutQuad'
            });
            
            // Reset glow
            anime({
                targets: this,
                boxShadow: getOriginalBoxShadow(this),
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
        
        // Press animation
        button.addEventListener('mousedown', function() {
            anime({
                targets: this,
                scale: 0.95,
                duration: 100,
                easing: 'easeOutQuad'
            });
        });
        
        button.addEventListener('mouseup', function() {
            anime({
                targets: this,
                scale: 1,
                duration: 100,
                easing: 'easeOutQuad'
            });
        });
    });
}

// Helper function to get original box-shadow
function getOriginalBoxShadow(element) {
    const color = getComputedStyle(element).borderColor;
    if (element.classList.contains('glow-button-green')) {
        return '0 0 5px var(--neon-green), 0 0 10px rgba(57, 255, 20, 0.3), 0 0 20px rgba(57, 255, 20, 0.1)';
    } else if (element.classList.contains('glow-button-blue')) {
        return '0 0 5px var(--neon-blue), 0 0 10px rgba(0, 255, 255, 0.3), 0 0 20px rgba(0, 255, 255, 0.1)';
    } else if (element.classList.contains('glow-button-pink')) {
        return '0 0 5px var(--neon-pink), 0 0 10px rgba(255, 0, 255, 0.3), 0 0 20px rgba(255, 0, 255, 0.1)';
    } else if (element.classList.contains('glow-button-purple')) {
        return '0 0 5px var(--neon-purple), 0 0 10px rgba(128, 0, 255, 0.3), 0 0 20px rgba(128, 0, 255, 0.1)';
    } else if (element.classList.contains('glow-button-orange')) {
        return '0 0 5px var(--neon-orange), 0 0 10px rgba(255, 85, 0, 0.3), 0 0 20px rgba(255, 85, 0, 0.1)';
    }
    return '0 0 5px currentColor, 0 0 10px rgba(255, 255, 255, 0.3)';
}

// Header animations
function initHeaderAnimations() {
    const header = document.querySelector('.header');
    if (header) {
        // Initial fade-in
        anime({
            targets: header,
            translateY: [-20, 0],
            opacity: [0, 1],
            duration: 800,
            easing: 'easeOutQuad'
        });
    }
}

// Hero section animations
function initHeroSectionAnimations() {
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        anime({
            targets: heroSection,
            scale: [0.95, 1],
            opacity: [0, 1],
            duration: 1000,
            easing: 'easeOutQuad'
        });
    }
    
    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        anime({
            targets: heroContent,
            translateY: [30, 0],
            opacity: [0, 1],
            duration: 1200,
            delay: 300,
            easing: 'easeOutQuad'
        });
    }
}

// Value proposition animations
function initValuePropAnimations() {
    const valueProps = document.querySelectorAll('.value-prop-card');
    
    valueProps.forEach((card, index) => {
        anime({
            targets: card,
            translateY: [20, 0],
            opacity: [0, 1],
            duration: 800,
            delay: index * 100,
            easing: 'easeOutQuad'
        });
    });
}

// Form animations
function initFormAnimations() {
    const formInputs = document.querySelectorAll('.form-input');
    
    formInputs.forEach(input => {
        // Focus animation
        input.addEventListener('focus', function() {
            anime({
                targets: this,
                translateY: -2,
                boxShadow: [
                    getComputedStyle(this).boxShadow,
                    '0 0 0 2px rgba(0, 255, 255, 0.3), 0 0 10px var(--neon-blue), 0 0 20px rgba(0, 255, 255, 0.2)'
                ],
                duration: 200,
                easing: 'easeOutQuad'
            });
        });
        
        // Blur animation
        input.addEventListener('blur', function() {
            anime({
                targets: this,
                translateY: 0,
                boxShadow: '0 0 5px rgba(255, 255, 255, 0.1), inset 0 0 10px rgba(255, 255, 255, 0.05)',
                duration: 200,
                easing: 'easeOutQuad'
            });
        });
    });
}

// Notification animations
function initNotificationAnimations() {
    const notifications = document.querySelectorAll('.message-success, .message-error');
    
    notifications.forEach(notification => {
        anime({
            targets: notification,
            translateX: [100, 0],
            opacity: [0, 1],
            duration: 500,
            easing: 'easeOutQuad'
        });
    });
}

// Cart animations
function initCartAnimations() {
    const cartItems = document.querySelectorAll('.cart-item');
    
    cartItems.forEach((item, index) => {
        anime({
            targets: item,
            translateX: [-20, 0],
            opacity: [0, 1],
            duration: 400,
            delay: index * 50,
            easing: 'easeOutQuad'
        });
    });
}

// Review animations
function initReviewAnimations() {
    const reviews = document.querySelectorAll('.review-card');
    
    reviews.forEach((review, index) => {
        anime({
            targets: review,
            translateY: [20, 0],
            opacity: [0, 1],
            duration: 600,
            delay: index * 100,
            easing: 'easeOutQuad'
        });
    });
}

// Staggered animations for multiple elements
function runStaggeredAnimations() {
    // Staggered fade-in for service cards
    anime({
        targets: '.service-card',
        translateY: [30, 0],
        opacity: [0, 1],
        duration: 800,
        delay: anime.stagger(100),
        easing: 'easeOutQuad'
    });
    
    // Staggered fade-in for feature highlights
    anime({
        targets: '.feature-highlight',
        translateX: [-20, 0],
        opacity: [0, 1],
        duration: 600,
        delay: anime.stagger(80),
        easing: 'easeOutQuad'
    });
}

// Export functions for global access
window.HomeSerAnimations = {
    initServiceCardAnimations,
    initButtonAnimations,
    initHeaderAnimations,
    initHeroSectionAnimations,
    initValuePropAnimations,
    initFormAnimations,
    initNotificationAnimations,
    initCartAnimations,
    initReviewAnimations,
    runStaggeredAnimations
};