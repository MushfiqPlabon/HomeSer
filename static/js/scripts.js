// scripts.js

// Function to initialize ripple effect on buttons
function initRippleEffect() {
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
        
        // Add animation class
        ripple.classList.add('animate');
        
        // Remove ripple after animation completes
        setTimeout(() => {
            ripple.remove();
        }, 600);
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
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            // Validation on blur
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            // Clear error state when user starts typing
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
            
            // Enhanced validation on focus out
            input.addEventListener('focusout', function() {
                validateField(this);
            });
        });
    });
}

// Function to validate individual fields
function validateField(field) {
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
    
    // Password confirmation validation
    if (field.name === 'password_confirm') {
        const passwordField = document.querySelector('input[name="password"]');
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
    errorEl.textContent = message;
    
    // Insert error after field
    field.parentNode.insertBefore(errorEl, field.nextSibling);
    
    // Add shake animation
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
    const cards = document.querySelectorAll('.service-card, .review-card, .acrylic-card');
    
    cards.forEach(card => {
        // Add elevation effect on hover
        card.addEventListener('mouseenter', function() {
            this.classList.add('elevated-card');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('elevated-card');
        });
        
        // Add press effect on click
        card.addEventListener('mousedown', function() {
            this.classList.add('container-transform');
        });
        
        card.addEventListener('mouseup', function() {
            this.classList.remove('container-transform');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('container-transform');
        });
    });
}

// Function to initialize loading skeletons
function initSkeletonScreens() {
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
    
    // Add loading state to interactive elements
    const loadingElements = document.querySelectorAll('[data-loading]');
    loadingElements.forEach(el => {
        el.addEventListener('click', function() {
            this.classList.add('loading-state');
            this.disabled = true;
            
            // Simulate loading completion
            setTimeout(() => {
                this.classList.remove('loading-state');
                this.disabled = false;
            }, 2000);
        });
    });
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
    const buttons = document.querySelectorAll('.glow-button');
    
    buttons.forEach(button => {
        // Add hover effect
        button.addEventListener('mouseenter', function() {
            this.classList.add('elevated-card');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('elevated-card');
        });
        
        // Add press effect
        button.addEventListener('mousedown', function() {
            this.classList.add('container-transform');
        });
        
        button.addEventListener('mouseup', function() {
            this.classList.remove('container-transform');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('container-transform');
        });
        
        // Add focus visible effect
        button.addEventListener('focus', function() {
            this.classList.add('focus-state');
        });
        
        button.addEventListener('blur', function() {
            this.classList.remove('focus-state');
        });
    });
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
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
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

// Function to initialize the page
function initPage() {
    // Ensure all content is visible immediately
    document.querySelectorAll('.fade-in, .animate-on-scroll').forEach(el => {
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
    } catch (error) {
        console.warn('Some JavaScript enhancements failed to load:', error);
        // Ensure content is still visible even if animations fail
        document.querySelectorAll('.fade-in, .animate-on-scroll').forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    }
    
    // Add fade-in effect to messages
    const messages = document.querySelectorAll('.message-success, .message-error');
    messages.forEach((message, index) => {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            message.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
        }, 100 + index * 50);
    });
    
    // Add fade-in effect to header
    const header = document.querySelector('.header');
    if (header) {
        header.style.opacity = '0';
        header.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            header.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            header.style.opacity = '1';
            header.style.transform = 'translateY(0)';
        }, 100);
    }
    
    // Add fade-in effect to service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 200 + index * 100);
    });
    
    // Add interactive state to form elements
    const formElements = document.querySelectorAll('input, textarea, select');
    formElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('focus-state');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('focus-state');
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initPage);