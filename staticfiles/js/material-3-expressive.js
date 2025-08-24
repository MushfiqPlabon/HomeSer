// material-3-expressive.js - Material 3 Expressive Animations Implementation

class Material3Expressive {
    constructor() {
        this.init();
    }
    
    init() {
        // Initialize all Material 3 Expressive components
        this.initButtons();
        this.initCards();
        this.initForms();
        this.initNavigation();
        this.initNotifications();
        this.initEmojis();
        this.initStaggeredAnimations();
    }
    
    // === Material 3 Expressive Button Animations ===
    initButtons() {
        const buttons = document.querySelectorAll('.glow-button, .m3-button');
        
        buttons.forEach(button => {
            // Hover effect
            button.addEventListener('mouseenter', (e) => {
                this.buttonHover(e.target);
            });
            
            // Leave effect
            button.addEventListener('mouseleave', (e) => {
                this.buttonLeave(e.target);
            });
            
            // Press effect
            button.addEventListener('mousedown', (e) => {
                this.buttonPress(e.target);
            });
            
            button.addEventListener('mouseup', (e) => {
                this.buttonRelease(e.target);
            });
            
            button.addEventListener('mouseleave', (e) => {
                this.buttonRelease(e.target);
            });
        });
    }
    
    buttonHover(element) {
        anime({
            targets: element,
            scale: 1.02,
            duration: 250,
            easing: 'cubicBezier(0, 0, 0.2, 1)', // decelerated
            transformOrigin: 'center'
        });
        
        // Glow effect
        anime({
            targets: element,
            boxShadow: [
                { value: '0 0 15px currentColor, 0 0 30px rgba(255, 255, 255, 0.5)', duration: 250 }
            ],
            easing: 'cubicBezier(0, 0, 0.2, 1)'
        });
    }
    
    buttonLeave(element) {
        anime({
            targets: element,
            scale: 1,
            duration: 250,
            easing: 'cubicBezier(0, 0, 0.2, 1)',
            transformOrigin: 'center'
        });
        
        // Reset glow
        anime({
            targets: element,
            boxShadow: [
                { value: this.getOriginalBoxShadow(element), duration: 250 }
            ],
            easing: 'cubicBezier(0, 0, 0.2, 1)'
        });
    }
    
    buttonPress(element) {
        anime({
            targets: element,
            scale: 0.92,
            duration: 100,
            easing: 'cubicBezier(0.4, 0, 1, 1)', // accelerated
            transformOrigin: 'center'
        });
    }
    
    buttonRelease(element) {
        anime({
            targets: element,
            scale: 1,
            duration: 100,
            easing: 'cubicBezier(0.4, 0, 1, 1)', // accelerated
            transformOrigin: 'center'
        });
    }
    
    getOriginalBoxShadow(element) {
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
    
    // === Material 3 Expressive Card Animations ===
    initCards() {
        const cards = document.querySelectorAll('.service-card, .review-card, .acrylic-card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                this.cardHover(e.target);
            });
            
            card.addEventListener('mouseleave', (e) => {
                this.cardLeave(e.target);
            });
            
            card.addEventListener('mousedown', (e) => {
                this.cardPress(e.target);
            });
            
            card.addEventListener('mouseup', (e) => {
                this.cardRelease(e.target);
            });
        });
    }
    
    cardHover(element) {
        anime({
            targets: element,
            translateY: -4,
            duration: 250,
            easing: 'cubicBezier(0, 0, 0.2, 1)', // decelerated
            boxShadow: [
                { 
                    value: '0 10px 20px rgba(0, 0, 0, 0.3), 0 0 15px var(--neon-green), 0 0 30px rgba(57, 255, 20, 0.2)', 
                    duration: 250 
                }
            ]
        });
    }
    
    cardLeave(element) {
        anime({
            targets: element,
            translateY: 0,
            duration: 250,
            easing: 'cubicBezier(0, 0, 0.2, 1)',
            boxShadow: [
                { 
                    value: '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.05)', 
                    duration: 250 
                }
            ]
        });
    }
    
    cardPress(element) {
        anime({
            targets: element,
            scale: 0.98,
            duration: 100,
            easing: 'cubicBezier(0.4, 0, 1, 1)'
        });
    }
    
    cardRelease(element) {
        anime({
            targets: element,
            scale: 1,
            duration: 100,
            easing: 'cubicBezier(0.4, 0, 1, 1)'
        });
    }
    
    // === Material 3 Expressive Form Animations ===
    initForms() {
        const formInputs = document.querySelectorAll('.form-input');
        
        formInputs.forEach(input => {
            input.addEventListener('focus', (e) => {
                this.formFocus(e.target);
            });
            
            input.addEventListener('blur', (e) => {
                this.formBlur(e.target);
            });
            
            // Error state
            if (input.classList.contains('error')) {
                this.formError(input);
            }
        });
    }
    
    formFocus(element) {
        anime({
            targets: element,
            translateY: -2,
            duration: 100,
            easing: 'cubicBezier(0, 0, 0.2, 1)',
            boxShadow: [
                { 
                    value: '0 0 0 2px rgba(0, 255, 255, 0.3), 0 0 10px var(--neon-blue), 0 0 20px rgba(0, 255, 255, 0.2)', 
                    duration: 100 
                }
            ]
        });
    }
    
    formBlur(element) {
        anime({
            targets: element,
            translateY: 0,
            duration: 100,
            easing: 'cubicBezier(0.4, 0, 1, 1)',
            boxShadow: [
                { 
                    value: '0 0 5px rgba(255, 255, 255, 0.1), inset 0 0 10px rgba(255, 255, 255, 0.05)', 
                    duration: 100 
                }
            ]
        });
    }
    
    formError(element) {
        anime({
            targets: element,
            translateX: [
                { value: -3, duration: 50 },
                { value: 3, duration: 50 },
                { value: -3, duration: 50 },
                { value: 0, duration: 50 }
            ],
            easing: 'cubicBezier(0.2, 0, 0, 1)',
            duration: 250
        });
    }
    
    // === Material 3 Expressive Navigation ===
    initNavigation() {
        const navLinks = document.querySelectorAll('nav a');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                this.navTransition(e.target);
            });
        });
    }
    
    navTransition(element) {
        // Shared axis X transition
        anime({
            targets: element,
            translateX: [0, -20],
            opacity: [1, 0],
            duration: 250,
            easing: 'cubicBezier(0.4, 0, 1, 1)'
        });
    }
    
    // === Material 3 Expressive Notifications ===
    initNotifications() {
        const notifications = document.querySelectorAll('.message-success, .message-error');
        
        notifications.forEach((notification, index) => {
            this.showNotification(notification, index);
        });
    }
    
    showNotification(element, index) {
        anime({
            targets: element,
            translateY: [100, 0],
            opacity: [0, 1],
            duration: 250,
            delay: index * 50,
            easing: 'cubicBezier(0, 0, 0.2, 1)'
        });
    }
    
    // === Material 3 Expressive Emoji Reactions ===
    initEmojis() {
        const emojiButtons = document.querySelectorAll('.emoji-reaction-btn');
        
        emojiButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                this.emojiReaction(e.target);
            });
        });
    }
    
    emojiReaction(element) {
        anime({
            targets: element,
            scale: [1, 1.3, 0.9, 1],
            duration: 300,
            easing: 'cubicBezier(0.3, 0, 0.8, 0.15)' // emphasized
        });
        
        // Add selected class
        element.classList.add('selected');
    }
    
    // === Material 3 Expressive Staggered Animations ===
    initStaggeredAnimations() {
        // Service cards
        const serviceCards = document.querySelectorAll('.service-card');
        if (serviceCards.length > 0) {
            this.staggeredEntrance(serviceCards, 100);
        }
        
        // Value props
        const valueProps = document.querySelectorAll('.value-prop-card');
        if (valueProps.length > 0) {
            this.staggeredEntrance(valueProps, 150);
        }
        
        // Reviews
        const reviews = document.querySelectorAll('.review-card');
        if (reviews.length > 0) {
            this.staggeredEntrance(reviews, 120);
        }
    }
    
    staggeredEntrance(elements, delay) {
        anime({
            targets: elements,
            translateY: [20, 0],
            opacity: [0, 1],
            duration: 300,
            delay: anime.stagger(delay),
            easing: 'cubicBezier(0, 0, 0.2, 1)'
        });
    }
    
    // === Material 3 Expressive Container Transform ===
    containerTransformEnter(element) {
        anime({
            targets: element,
            scale: [0.8, 1],
            opacity: [0, 1],
            duration: 400,
            easing: 'cubicBezier(0.3, 0, 0.8, 0.15)' // emphasized
        });
    }
    
    containerTransformExit(element) {
        anime({
            targets: element,
            scale: [1, 0.8],
            opacity: [1, 0],
            duration: 300,
            easing: 'cubicBezier(0.4, 0, 1, 1)' // accelerated
        });
    }
    
    // === Material 3 Expressive Shared Axis ===
    sharedAxisXEnter(element) {
        anime({
            targets: element,
            translateX: [20, 0],
            opacity: [0, 1],
            duration: 300,
            easing: 'cubicBezier(0.3, 0, 0.8, 0.15)' // emphasized
        });
    }
    
    sharedAxisXExit(element) {
        anime({
            targets: element,
            translateX: [0, -20],
            opacity: [1, 0],
            duration: 250,
            easing: 'cubicBezier(0.4, 0, 1, 1)' // accelerated
        });
    }
    
    // === Material 3 Expressive Feedback ===
    successFeedback(element) {
        anime({
            targets: element,
            boxShadow: [
                { value: '0 0 0 0 rgba(57, 255, 20, 0.4)', duration: 0 },
                { value: '0 0 0 10px rgba(57, 255, 20, 0)', duration: 200 },
                { value: '0 0 0 0 rgba(57, 255, 20, 0)', duration: 50 }
            ],
            duration: 250,
            easing: 'cubicBezier(0.3, 0, 0.8, 0.15)'
        });
    }
    
    errorFeedback(element) {
        anime({
            targets: element,
            translateX: [
                { value: -5, duration: 50 },
                { value: 5, duration: 50 },
                { value: -5, duration: 50 },
                { value: 0, duration: 50 }
            ],
            duration: 250,
            easing: 'cubicBezier(0.2, 0, 0, 1)'
        });
    }
    
    // === Public Methods for External Use ===
    animateButtonPress(element) {
        this.buttonPress(element);
        setTimeout(() => this.buttonRelease(element), 100);
    }
    
    animateCardHover(element) {
        this.cardHover(element);
    }
    
    animateCardLeave(element) {
        this.cardLeave(element);
    }
    
    animateSuccess(element) {
        this.successFeedback(element);
    }
    
    animateError(element) {
        this.errorFeedback(element);
    }
    
    animateContainerEnter(element) {
        this.containerTransformEnter(element);
    }
    
    animateContainerExit(element) {
        this.containerTransformExit(element);
    }
    
    animateSharedAxisEnter(element) {
        this.sharedAxisXEnter(element);
    }
    
    animateSharedAxisExit(element) {
        this.sharedAxisXExit(element);
    }
}

// Initialize Material 3 Expressive when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.material3Expressive = new Material3Expressive();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Material3Expressive;
}