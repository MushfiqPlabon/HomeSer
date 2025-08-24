// scripts.js - Consolidated JavaScript file for HomeSer
// Contains all functionality from scripts.js, anime-animations.js, and material-3-expressive.js

// Cache for frequently accessed DOM elements
const DOMCache = {
    serviceCards: null,
    glowButtons: null,
    formInputs: null,
    fadeElements: null,
    animatedElements: null,
    reviewCards: null,
    valueProps: null,
    messages: null,
    navLinks: null,
    init() {
        this.serviceCards = document.querySelectorAll('.service-card');
        this.glowButtons = document.querySelectorAll('.glow-button, .m3-button');
        this.formInputs = document.querySelectorAll('.form-input');
        this.fadeElements = document.querySelectorAll('.fade-in');
        this.animatedElements = document.querySelectorAll('.animate-on-scroll');
        this.reviewCards = document.querySelectorAll('.review-card');
        this.valueProps = document.querySelectorAll('.value-prop-card');
        this.messages = document.querySelectorAll('.message-success, .message-error');
        this.navLinks = document.querySelectorAll('nav a');
    },
    getServiceCards() {
        if (!this.serviceCards) this.init();
        return this.serviceCards;
    },
    getGlowButtons() {
        if (!this.glowButtons) this.init();
        return this.glowButtons;
    },
    getFormInputs() {
        if (!this.formInputs) this.init();
        return this.formInputs;
    },
    getFadeElements() {
        if (!this.fadeElements) this.init();
        return this.fadeElements;
    },
    getAnimatedElements() {
        if (!this.animatedElements) this.init();
        return this.animatedElements;
    },
    getReviewCards() {
        if (!this.reviewCards) this.init();
        return this.reviewCards;
    },
    getValueProps() {
        if (!this.valueProps) this.init();
        return this.valueProps;
    },
    getMessages() {
        if (!this.messages) this.init();
        return this.messages;
    },
    getNavLinks() {
        if (!this.navLinks) this.init();
        return this.navLinks;
    }
};

// Function to initialize ripple effect on buttons
function initRippleEffect() {
    // Use event delegation for ripple effect
    document.addEventListener('click', function(e) {
        // Check if clicked element is a button or has data-ripple attribute
        const button = e.target.closest('[data-ripple]');
        if (!button) return;
        
        // Create ripple element
        const ripple = document.createElement('span');
        ripple.classList.add('press-ripple');
        
        // Add ripple to button
        button.appendChild(ripple);
        
        // Get button dimensions and click position
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        // Set ripple styles
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        // Enhanced ripple animation with Anime.js
        if (typeof anime !== 'undefined') {
            anime({
                targets: ripple,
                scale: [0, 2],
                opacity: [0.2, 0],
                duration: 600,
                easing: 'cubicBezier(0, 0, 0.2, 1)',
                complete: function() {
                    ripple.remove();
                }
            });
        } else {
            // Fallback to CSS animation
            ripple.classList.add('animate');
            
            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 600);
        }
    });
}

// Function to initialize form validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add loading state to submit buttons
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
                
                // Add spinner icon
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>' + originalText;
                
                // Store original text for later restoration
                submitBtn.dataset.originalText = originalText;
            }
        });
        
        // Real-time validation with optimized event handling
        const inputs = form.querySelectorAll('input, textarea, select');
        
        // Create a map of password fields for faster lookup
        const passwordFields = new Map();
        inputs.forEach(input => {
            if (input.type === 'password' && input.name !== 'password_confirm') {
                passwordFields.set(input.name, input);
            }
        });
        
        inputs.forEach(input => {
            // Validation on blur
            input.addEventListener('blur', function() {
                validateField(this, passwordFields);
            });
            
            // Clear error state when user starts typing
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
            
            // Enhanced validation on focus out
            input.addEventListener('focusout', function() {
                validateField(this, passwordFields);
            });
        });
    });
}

// Function to validate individual fields
function validateField(field, passwordFields = new Map()) {
    // Clear previous error states
    clearFieldError(field);
    
    let isValid = true;
    let errorMessage = '';
    
    // Check if field is required and empty
    if (field.hasAttribute('required') && !field.value.trim()) {
        errorMessage = 'This field is required';
        isValid = false;
    }
    
    // Email validation
    if (field.type === 'email' && field.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value.trim())) {
            errorMessage = 'Please enter a valid email address';
            isValid = false;
        }
    }
    
    // Password validation
    if (field.type === 'password' && field.value.trim()) {
        if (field.value.length < 8) {
            errorMessage = 'Password must be at least 8 characters long';
            isValid = false;
        }
    }
    
    // Password confirmation validation with optimized lookup
    if (field.name === 'password_confirm') {
        // Use the pre-built map for O(1) lookup instead of O(n) querySelector
        const passwordField = passwordFields.get('password') || 
                             document.querySelector('input[name="password"]');
        if (passwordField && field.value !== passwordField.value) {
            errorMessage = 'Passwords do not match';
            isValid = false;
        }
    }
    
    // Username validation
    if (field.name === 'username' && field.value.trim()) {
        if (field.value.length < 3) {
            errorMessage = 'Username must be at least 3 characters long';
            isValid = false;
        }
    }
    
    if (!isValid) {
        showError(field, errorMessage);
    }
    
    return isValid;
}

// Function to clear field error
function clearFieldError(field) {
    field.classList.remove('error');
    const errorEl = field.parentNode.querySelector('.error-message');
    if (errorEl) {
        errorEl.remove();
    }
    
    // Remove error state animation
    field.classList.remove('error-state');
}

// Function to show error message
function showError(field, message) {
    field.classList.add('error');
    field.classList.add('error-state');
    
    // Create error element
    const errorEl = document.createElement('div');
    errorEl.classList.add('error-message', 'text-red-500', 'text-sm', 'mt-1');
    errorEl.innerHTML = '<i class="fas fa-exclamation-circle mr-1"></i>' + message;
    
    // Insert error after field
    field.parentNode.insertBefore(errorEl, field.nextSibling);
    
    // Add shake animation using Anime.js if available
    if (typeof anime !== 'undefined') {
        anime({
            targets: field,
            translateX: [
                { value: -5, duration: 100 },
                { value: 5, duration: 100 },
                { value: -5, duration: 100 },
                { value: 0, duration: 100 }
            ],
            easing: 'easeInOutQuad'
        });
    } else {
        // Fallback to CSS animation
        field.animate([
            { transform: 'translateX(0)' },
            { transform: 'translateX(-5px)' },
            { transform: 'translateX(5px)' },
            { transform: 'translateX(0)' }
        ], {
            duration: 300,
            iterations: 1
        });
    }
}

// Function to show success feedback
function showSuccess(field) {
    field.classList.add('success-state');
    
    // Remove success state after animation
    setTimeout(() => {
        field.classList.remove('success-state');
    }, 500);
}

// Function to detect if device can handle animations
function canHandleAnimations() {
    // Check if user prefers reduced motion
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return false;
    }
    
    // Check for low-end devices
    const isLowEndDevice = (
        navigator.hardwareConcurrency <= 2 || 
        window.devicePixelRatio < 1.5 ||
        screen.width <= 768
    );
    
    // Check for slow network
    if ('connection' in navigator) {
        const connection = navigator.connection;
        if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
            return false;
        }
        if (connection.downlink && connection.downlink < 0.5) { // Less than 0.5 Mbps
            return false;
        }
    }
    
    // Enable animations for devices that can handle them
    return !isLowEndDevice;
}

// Function to initialize scroll animations
function initScrollAnimations() {
    // Make all animated elements visible immediately
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => {
        el.classList.add('animated');
    });
}

// Function to initialize card hover effects
function initCardEffects() {
    // Use event delegation for card effects
    document.addEventListener('mouseenter', function(e) {
        // Check if entered element is a service card, review card, or acrylic card
        if (e.target.classList.contains('service-card') || 
            e.target.classList.contains('review-card') || 
            e.target.classList.contains('acrylic-card')) {
            e.target.classList.add('elevated-card');
        }
    }, true); // Use capture phase
    
    document.addEventListener('mouseleave', function(e) {
        // Check if left element is a service card, review card, or acrylic card
        if (e.target.classList.contains('service-card') || 
            e.target.classList.contains('review-card') || 
            e.target.classList.contains('acrylic-card')) {
            e.target.classList.remove('elevated-card');
            e.target.classList.remove('container-transform');
        }
    }, true); // Use capture phase
    
    document.addEventListener('mousedown', function(e) {
        // Check if pressed element is a service card, review card, or acrylic card
        if (e.target.classList.contains('service-card') || 
            e.target.classList.contains('review-card') || 
            e.target.classList.contains('acrylic-card')) {
            e.target.classList.add('container-transform');
        }
    }, true); // Use capture phase
    
    document.addEventListener('mouseup', function(e) {
        // Check if released element is a service card, review card, or acrylic card
        if (e.target.classList.contains('service-card') || 
            e.target.classList.contains('review-card') || 
            e.target.classList.contains('acrylic-card')) {
            e.target.classList.remove('container-transform');
        }
    }, true); // Use capture phase
}

// Function to initialize loading skeletons
function initSkeletonScreens() {
    // Use event delegation for loading state
    document.addEventListener('click', function(e) {
        // Check if clicked element has data-loading attribute
        if (e.target.hasAttribute('data-loading')) {
            e.target.classList.add('loading-state');
            e.target.disabled = true;
            
            // Simulate loading completion
            setTimeout(() => {
                e.target.classList.remove('loading-state');
                e.target.disabled = false;
            }, 2000);
        }
    });
    
    // This would typically be called when loading content dynamically
    // For now, we'll just add a utility function
    window.showSkeleton = function(container) {
        container.innerHTML = `
            <div class="skeleton-card animate-pulse">
                <div class="bg-dark-gray rounded-lg h-48 mb-4"></div>
                <div class="bg-dark-gray rounded h-6 w-3/4 mb-2"></div>
                <div class="bg-dark-gray rounded h-4 w-full mb-2"></div>
                <div class="bg-dark-gray rounded h-4 w-1/2"></div>
            </div>
        `;
    };
}

// Function to initialize lazy loading for images
function initLazyLoading() {
    // Check if browser supports native lazy loading
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback for browsers that don't support native lazy loading
        // We'll load images immediately for simplicity
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
            }
        });
    }
}

// Function to initialize button hover effects
function initButtonEffects() {
    // Use event delegation for button effects
    document.addEventListener('mouseenter', function(e) {
        // Check if entered element is a glow button
        if (e.target.classList.contains('glow-button')) {
            e.target.classList.add('elevated-card');
        }
    }, true); // Use capture phase
    
    document.addEventListener('mouseleave', function(e) {
        // Check if left element is a glow button
        if (e.target.classList.contains('glow-button')) {
            e.target.classList.remove('elevated-card');
            e.target.classList.remove('container-transform');
        }
    }, true); // Use capture phase
    
    document.addEventListener('mousedown', function(e) {
        // Check if pressed element is a glow button
        if (e.target.classList.contains('glow-button')) {
            e.target.classList.add('container-transform');
        }
    }, true); // Use capture phase
    
    document.addEventListener('mouseup', function(e) {
        // Check if released element is a glow button
        if (e.target.classList.contains('glow-button')) {
            e.target.classList.remove('container-transform');
        }
    }, true); // Use capture phase
    
    document.addEventListener('focus', function(e) {
        // Check if focused element is a glow button
        if (e.target.classList.contains('glow-button')) {
            e.target.classList.add('focus-state');
        }
    }, true); // Use capture phase
    
    document.addEventListener('blur', function(e) {
        // Check if blurred element is a glow button
        if (e.target.classList.contains('glow-button')) {
            e.target.classList.remove('focus-state');
        }
    }, true); // Use capture phase
}

// Function to initialize fade-in animations
function initFadeInAnimations() {
    const fadeElements = document.querySelectorAll('.fade-in');
    
    fadeElements.forEach((el, index) => {
        // Add delay based on index for staggered effect
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('fade-in-animate');
    });
}

// Function to initialize smooth scrolling
function initSmoothScrolling() {
    // Use event delegation for smooth scrolling
    document.addEventListener('click', function(e) {
        // Check if clicked element is an anchor link with hash
        if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            
            const target = document.querySelector(e.target.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
}

// Function to initialize performance optimizations
function initPerformanceOptimizations() {
    // Defer non-critical JavaScript
    const scripts = document.querySelectorAll('script[data-defer]');
    scripts.forEach(script => {
        script.async = true;
    });
    
    // Optimize images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        // Add loading attribute for native lazy loading
        if (!img.hasAttribute('loading')) {
            img.setAttribute('loading', 'lazy');
        }
        
        // Add fetchpriority for important images
        if (img.classList.contains('hero-image') || img.classList.contains('profile-picture')) {
            img.setAttribute('fetchpriority', 'high');
        }
    });
    
    // Prefetch important pages (only on devices that can handle it)
    if (canHandleAnimations()) {
        const prefetchLinks = document.querySelectorAll('a[data-prefetch]');
        prefetchLinks.forEach(link => {
            const prefetchLink = document.createElement('link');
            prefetchLink.rel = 'prefetch';
            prefetchLink.href = link.href;
            document.head.appendChild(prefetchLink);
        });
    }
}

// Function to initialize emoji reactions
function initEmojiReactions() {
    // Use event delegation for emoji reactions
    document.addEventListener('click', function(e) {
        // Check if clicked element is an emoji reaction button
        if (e.target.classList.contains('emoji-reaction-btn')) {
            // Add animation effect using Anime.js if available
            if (typeof anime !== 'undefined') {
                anime({
                    targets: e.target,
                    scale: [1, 1.3, 1],
                    duration: 600,
                    easing: 'easeOutElastic'
                });
            } else {
                // Fallback to CSS animation
                e.target.classList.add('animate-bounce');
                setTimeout(() => {
                    e.target.classList.remove('animate-bounce');
                }, 1000);
            }
            
            // Add selected class
            e.target.classList.add('selected');
        }
    });
    
    // Add emoji reactions to review cards
    const reviewCards = document.querySelectorAll('.review-card');
    reviewCards.forEach(card => {
        // Create emoji reaction container
        const reactionContainer = document.createElement('div');
        reactionContainer.className = 'emoji-reactions mt-3 flex gap-2';
        
        // Add reaction emojis
        const reactions = ['👍', '❤️', '😂', '😮', '😢', '😠'];
        reactions.forEach(emoji => {
            const reactionBtn = document.createElement('button');
            reactionBtn.className = 'emoji-reaction-btn text-lg hover:scale-125 transition-transform';
            reactionBtn.textContent = emoji;
            reactionBtn.setAttribute('data-emoji', emoji);
            reactionContainer.appendChild(reactionBtn);
        });
        
        // Add container to card
        card.appendChild(reactionContainer);
    });
}

// Function to initialize enhanced notifications
function initEnhancedNotifications() {
    // Add icons to existing notifications
    const messages = document.querySelectorAll('.message-success, .message-error');
    messages.forEach(message => {
        if (message.classList.contains('message-success')) {
            message.innerHTML = '<i class="fas fa-check-circle mr-2"></i>' + message.innerHTML;
        } else if (message.classList.contains('message-error')) {
            message.innerHTML = '<i class="fas fa-exclamation-circle mr-2"></i>' + message.innerHTML;
        }
    });
}

// Function to initialize Material 3 Expressive animations
function initMaterial3Animations() {
    // Add shared axis transitions to navigation elements
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Add exit animation class
            this.classList.add('shared-axis-x-exit');
            
            // Remove class after animation
            setTimeout(() => {
                this.classList.remove('shared-axis-x-exit');
            }, 300);
        });
    });
    
    // Add container transform to interactive elements
    const interactiveElements = document.querySelectorAll('.interactive-element-animated');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.classList.add('container-transform');
        });
        
        element.addEventListener('mouseleave', function() {
            this.classList.remove('container-transform');
        });
        
        element.addEventListener('mousedown', function() {
            this.classList.add('button-press-effect');
        });
        
        element.addEventListener('mouseup', function() {
            this.classList.remove('button-press-effect');
        });
        
        element.addEventListener('mouseleave', function() {
            this.classList.remove('button-press-effect');
        });
    });
    
    // Add fade through transitions to modal elements
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.dataset.modalTrigger;
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('fade-through-enter');
                modal.style.display = 'block';
                
                // Remove class after animation
                setTimeout(() => {
                    modal.classList.remove('fade-through-enter');
                }, 300);
            }
        });
    });
    
    // Add close functionality to modals
    const modalClosers = document.querySelectorAll('[data-modal-close]');
    modalClosers.forEach(closer => {
        closer.addEventListener('click', function() {
            const modal = this.closest('.modal');
            if (modal) {
                modal.classList.add('fade-through-exit');
                
                // Hide modal after animation
                setTimeout(() => {
                    modal.classList.remove('fade-through-exit');
                    modal.style.display = 'none';
                }, 150);
            }
        });
    });
}

// Function to initialize the page
function initPage() {
    // Ensure all content is visible immediately
    const elementsToInitialize = DOMCache.getFadeElements();
    const animatedElements = DOMCache.getAnimatedElements();
    
    // Combine both collections
    const allElements = [...elementsToInitialize, ...animatedElements];
    allElements.forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
    });
    
    // Initialize all components
    try {
        initRippleEffect();
        initFormValidation();
        initScrollAnimations();
        initCardEffects();
        initSkeletonScreens();
        initLazyLoading();
        initButtonEffects();
        initFadeInAnimations();
        initSmoothScrolling();
        initPerformanceOptimizations();
        initEmojiReactions();
        initEnhancedNotifications();
        initMaterial3Animations();
    } catch (error) {
        console.warn('Some JavaScript enhancements failed to load:', error);
        // Ensure content is still visible even if animations fail
        allElements.forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    }
    
    // Add fade-in effect to messages using Anime.js if available
    const messages = DOMCache.getMessages();
    messages.forEach((message, index) => {
        if (typeof anime !== 'undefined') {
            anime({
                targets: message,
                translateY: [-10, 0],
                opacity: [0, 1],
                duration: 500,
                delay: index * 100,
                easing: 'easeOutQuad'
            });
        } else {
            // Fallback to CSS animation
            message.style.opacity = '0';
            message.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                message.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                message.style.opacity = '1';
                message.style.transform = 'translateY(0)';
            }, 100 + index * 50);
        }
    });
    
    // Add fade-in effect to header
    const header = document.querySelector('.header');
    if (header) {
        if (typeof anime !== 'undefined') {
            anime({
                targets: header,
                translateY: [-20, 0],
                opacity: [0, 1],
                duration: 800,
                easing: 'easeOutQuad'
            });
        } else {
            // Fallback to CSS animation
            header.style.opacity = '0';
            header.style.transform = 'translateY(-20px)';
            
            setTimeout(() => {
                header.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                header.style.opacity = '1';
                header.style.transform = 'translateY(0)';
            }, 100);
        }
    }
    
    // Add fade-in effect to service cards
    const serviceCards = DOMCache.getServiceCards();
    serviceCards.forEach((card, index) => {
        if (typeof anime !== 'undefined') {
            anime({
                targets: card,
                translateY: [20, 0],
                opacity: [0, 1],
                duration: 600,
                delay: index * 100,
                easing: 'easeOutQuad'
            });
        } else {
            // Fallback to CSS animation
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 200 + index * 100);
        }
    });
    
    // Add interactive state to form elements
    const formElements = DOMCache.getFormInputs();
    formElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('focus-state');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('focus-state');
        });
    });
    
    // Add glow effects to navbar items
    const navItems = document.querySelectorAll('.nav-glow');
    navItems.forEach(item => {
        item.addEventListener('mousedown', function() {
            this.classList.add('active');
        });
        
        item.addEventListener('mouseup', function() {
            this.classList.remove('active');
            this.classList.add('clicked');
            
            // Remove the clicked class after animation completes
            setTimeout(() => {
                this.classList.remove('clicked');
            }, 600);
        });
        
        item.addEventListener('mouseleave', function() {
            this.classList.remove('active');
        });
    });
}

// === Anime.js Animations (from anime-animations.js) ===

// Service card hover animations
function initServiceCardAnimations() {
    const serviceCards = DOMCache.getServiceCards();
    
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
    const buttons = DOMCache.getGlowButtons();
    
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
    const valueProps = DOMCache.getValueProps();
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
    const formInputs = DOMCache.getFormInputs();
    
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
    const notifications = DOMCache.getMessages();
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
    const reviews = DOMCache.getReviewCards();
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
    const serviceCards = DOMCache.getServiceCards();
    if (serviceCards.length > 0) {
        anime({
            targets: serviceCards,
            translateY: [30, 0],
            opacity: [0, 1],
            duration: 800,
            delay: anime.stagger(100),
            easing: 'easeOutQuad'
        });
    }
    
    // Staggered fade-in for feature highlights
    const featureHighlights = document.querySelectorAll('.feature-highlight');
    if (featureHighlights.length > 0) {
        anime({
            targets: featureHighlights,
            translateX: [-20, 0],
            opacity: [0, 1],
            duration: 600,
            delay: anime.stagger(80),
            easing: 'easeOutQuad'
        });
    }
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

// === Material 3 Expressive Animations Implementation ===

class Material3Expressive {
    constructor() {
        // Material 3 Expressive Easing Functions
        this.MD_STANDARD_EASING = 'cubicBezier(0.2, 0, 0, 1)';
        this.MD_EMPHASIZED_EASING = 'cubicBezier(0.3, 0, 0.8, 0.15)';
        this.MD_DECELERATED_EASING = 'cubicBezier(0, 0, 0.2, 1)';
        this.MD_ACCELERATED_EASING = 'cubicBezier(0.4, 0, 1, 1)';
        
        // Check for reduced motion preference
        this.prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
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
        // Respect reduced motion preference
        if (this.prefersReducedMotion) {
            // Use simpler focus/blur effects when reduced motion is preferred
            const buttons = DOMCache.getGlowButtons();
            buttons.forEach(button => {
                button.addEventListener('focus', (e) => {
                    e.target.classList.add('focused');
                });
                
                button.addEventListener('blur', (e) => {
                    e.target.classList.remove('focused');
                });
                
                button.addEventListener('mousedown', (e) => {
                    e.target.classList.add('pressed');
                });
                
                button.addEventListener('mouseup', (e) => {
                    e.target.classList.remove('pressed');
                });
            });
            return;
        }
        
        const buttons = DOMCache.getGlowButtons();
        
        buttons.forEach(button => {
            // Add state layer if it doesn't exist
            if (!button.querySelector('.state-layer')) {
                const stateLayer = document.createElement('span');
                stateLayer.className = 'state-layer';
                button.appendChild(stateLayer);
            }
            
            // Hover effect
            button.addEventListener('mouseenter', (e) => {
                this.buttonHover(e.target);
            });
            
            // Leave effect
            button.addEventListener('mouseleave', (e) => {
                this.buttonLeave(e.target);
            });
            
            // Focus effect
            button.addEventListener('focus', (e) => {
                this.buttonFocus(e.target);
            });
            
            button.addEventListener('blur', (e) => {
                this.buttonBlur(e.target);
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
            
            // Keyboard support
            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    this.buttonPress(e.target);
                }
            });
            
            button.addEventListener('keyup', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    this.buttonRelease(e.target);
                }
            });
        });
    }
    
    buttonHover(element) {
        // State layer hover effect (8% opacity)
        const stateLayer = element.querySelector('.state-layer');
        if (stateLayer) {
            anime({
                targets: stateLayer,
                opacity: 0.08,
                duration: 150,
                easing: 'easeOutQuad'
            });
        }
        
        anime({
            targets: element,
            scale: 1.02,
            duration: 250,
            easing: this.MD_DECELERATED_EASING, // Unified easing
            transformOrigin: 'center'
        });
        
        // Glow effect
        anime({
            targets: element,
            boxShadow: [
                { value: '0 0 15px currentColor, 0 0 30px rgba(255, 255, 255, 0.5)', duration: 250 }
            ],
            easing: this.MD_DECELERATED_EASING // Unified easing
        });
    }
    
    buttonLeave(element) {
        // State layer leave effect
        const stateLayer = element.querySelector('.state-layer');
        if (stateLayer) {
            anime({
                targets: stateLayer,
                opacity: 0,
                duration: 150,
                easing: 'easeOutQuad'
            });
        }
        
        anime({
            targets: element,
            scale: 1,
            duration: 250,
            easing: this.MD_DECELERATED_EASING, // Unified easing
            transformOrigin: 'center'
        });
        
        // Reset glow
        anime({
            targets: element,
            boxShadow: [
                { value: this.getOriginalBoxShadow(element), duration: 250 }
            ],
            easing: this.MD_DECELERATED_EASING // Unified easing
        });
    }
    
    buttonFocus(element) {
        // State layer focus effect (12% opacity)
        const stateLayer = element.querySelector('.state-layer');
        if (stateLayer) {
            anime({
                targets: stateLayer,
                opacity: 0.12,
                duration: 150,
                easing: 'easeOutQuad'
            });
        }
        
        // Add focus ring
        element.classList.add('focused');
    }
    
    buttonBlur(element) {
        // State layer blur effect
        const stateLayer = element.querySelector('.state-layer');
        if (stateLayer) {
            anime({
                targets: stateLayer,
                opacity: 0,
                duration: 150,
                easing: 'easeOutQuad'
            });
        }
        
        // Remove focus ring
        element.classList.remove('focused');
    }
    
    buttonPress(element) {
        // State layer press effect (15% opacity)
        const stateLayer = element.querySelector('.state-layer');
        if (stateLayer) {
            anime({
                targets: stateLayer,
                opacity: 0.15,
                duration: 100,
                easing: 'easeOutQuad'
            });
        }
        
        anime({
            targets: element,
            scale: 0.95, // Enhanced press effect
            duration: 100,
            easing: this.MD_ACCELERATED_EASING, // Unified easing
            transformOrigin: 'center'
        });
        
        // Add pressed class
        element.classList.add('pressed');
        
        // Haptic feedback simulation
        if (navigator.vibrate) {
            navigator.vibrate(10);
        }
    }
    
    buttonRelease(element) {
        // Reset state layer
        const stateLayer = element.querySelector('.state-layer');
        if (stateLayer) {
            anime({
                targets: stateLayer,
                opacity: 0,
                duration: 100,
                easing: 'easeOutQuad'
            });
        }
        
        anime({
            targets: element,
            scale: 1,
            duration: 100,
            easing: this.MD_ACCELERATED_EASING, // Unified easing
            transformOrigin: 'center'
        });
        
        // Remove pressed class
        element.classList.remove('pressed');
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
        // Respect reduced motion preference
        if (this.prefersReducedMotion) {
            return; // Skip card animations if user prefers reduced motion
        }
        
        const cards = DOMCache.getServiceCards();
        
        cards.forEach(card => {
            // Add hardware acceleration hints
            card.style.transformOrigin = 'center';
            card.style.willChange = 'transform, box-shadow';
            
            // Add CSS class for parallax effect (CSS-based, not JS-based)
            card.classList.add('parallax-card');
            
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
            
            // Remove expensive mousemove listener and use CSS-based parallax instead
            // card.addEventListener('mousemove', (e) => {
            //     this.cardParallax(e.target, e);
            // });
        });
    }
    
    cardHover(element) {
        // More pronounced lift effect
        anime({
            targets: element,
            translateY: -8, // Increased from -4 to -8
            translateZ: 0, // Force hardware acceleration
            duration: 300, // Slightly longer duration
            easing: this.MD_DECELERATED_EASING, // Unified easing
            boxShadow: [
                { 
                    value: '0 15px 30px rgba(0, 0, 0, 0.4), 0 0 20px var(--neon-green), 0 0 40px rgba(57, 255, 20, 0.3)', 
                    duration: 300 
                }
            ]
        });
    }
    
    cardLeave(element) {
        anime({
            targets: element,
            translateY: 0,
            translateZ: 0,
            duration: 250,
            easing: this.MD_DECELERATED_EASING, // Unified easing
            boxShadow: [
                { 
                    value: '0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.05)', 
                    duration: 250 
                }
            ]
        });
    }
    
    cardPress(element) {
        // Enhanced press effect
        anime({
            targets: element,
            scale: 0.96, // Increased from 0.98 to 0.96
            translateZ: 0,
            duration: 150, // Slightly longer duration
            easing: this.MD_ACCELERATED_EASING // Unified easing
        });
    }
    
    cardRelease(element) {
        anime({
            targets: element,
            scale: 1,
            translateZ: 0,
            duration: 150,
            easing: this.MD_ACCELERATED_EASING // Unified easing
        });
    }
    
    cardParallax(element, event) {
        // Throttle parallax effect to reduce performance impact
        if (!element._lastParallaxTime) {
            element._lastParallaxTime = 0;
        }
        
        const now = Date.now();
        if (now - element._lastParallaxTime < 16) { // Throttle to ~60fps
            return;
        }
        element._lastParallaxTime = now;
        
        // Use requestAnimationFrame for better performance
        requestAnimationFrame(() => {
            // Physics-based movement effect with optimized calculations
            const rect = element.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const deltaX = (x - centerX) / centerX;
            const deltaY = (y - centerY) / centerY;
            const rotateY = deltaX * 5; // Max 5 degrees
            const rotateX = -deltaY * 5; // Max 5 degrees
            
            // Apply subtle 3D transform with hardware acceleration
            element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(${element.style.transform.includes('translateY(-8px)') ? -8 : 0}px)`;
            element.style.willChange = 'transform';
        });
    }
    
    // === Material 3 Expressive Form Animations ===
    initForms() {
        const formInputs = DOMCache.getFormInputs();
        
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
        // Navigation is now handled via event delegation
        // This function is kept for API compatibility
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
        const notifications = DOMCache.getMessages();
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
        // Emoji reactions are now handled via event delegation
        // This function is kept for API compatibility
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
        const serviceCards = DOMCache.getServiceCards();
        if (serviceCards.length > 0) {
            this.staggeredEntrance(serviceCards, 100);
        }
        
        // Value props
        const valueProps = DOMCache.getValueProps();
        if (valueProps.length > 0) {
            this.staggeredEntrance(valueProps, 150);
        }
        
        // Reviews
        const reviews = DOMCache.getReviewCards();
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

// Initialize all components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize DOM cache
    DOMCache.init();
    
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
    
    // Initialize Material 3 Expressive
    window.material3Expressive = new Material3Expressive();
    
    // Initialize page
    initPage();
});