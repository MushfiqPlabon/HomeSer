# Bug Tracking Document

## Overview
This document tracks actual bugs in the HomeSer project that need to be fixed. These are issues that would prevent the application from working correctly in development.

## Current Bugs to Fix

### 1. Database Relationship Issues
**Priority**: High
**Description**: Need to verify that the Cart-CartItem and Order-OrderItem relationships are working correctly with the new indexes and constraints.
**Affected Files**: 
- `HomeSer/models.py`
- `HomeSer/views.py` (CartViewSet, OrderViewSet)
- `HomeSer/serializers.py` (CartSerializer, OrderSerializer)

### 2. Cache Key Validation
**Priority**: Medium
**Description**: Some cache keys might not be invalidated properly when related data changes.
**Affected Files**: 
- `HomeSer/views.py` (all view functions)
- Management commands

### 3. Form Validation Edge Cases
**Priority**: Medium
**Description**: Form validation might not handle all edge cases properly, especially for file uploads.
**Affected Files**: 
- `HomeSer/forms.py`
- `HomeSer/views.py` (edit_profile view)
- JavaScript form validation

### 4. Template Variable Consistency
**Priority**: Medium
**Description**: Need to verify that all template variables match what's being passed from views.
**Affected Files**: 
- All HTML templates in `templates/` directory
- Corresponding view functions

### 5. JavaScript Event Listener Cleanup
**Priority**: Low
**Description**: Ripple effect and other JavaScript interactions might not clean up event listeners properly.
**Affected Files**: 
- `static/js/scripts.js`

### 6. Rating Display Logic
**Priority**: Low
**Description**: Rating stars display might fail with None or invalid average_rating values.
**Affected Files**: 
- `templates/service_detail.html`
- `templates/services.html`

## Verification Needed

### 1. Migration Status
- [ ] Verify all database migrations applied successfully
- [ ] Check that unique constraints are working
- [ ] Validate index creation

### 2. URL Routing
- [ ] Test all URL patterns work correctly
- [ ] Verify API endpoints are accessible
- [ ] Check web views render properly

### 3. User Authentication
- [ ] Test login/logout functionality
- [ ] Verify role-based access control
- [ ] Check profile management

### 4. Core Functionality
- [ ] Test service browsing and search
- [ ] Verify cart operations (add/remove items)
- [ ] Test checkout process
- [ ] Check order history
- [ ] Validate review system

## Testing Approach

1. Run through all user flows manually
2. Test edge cases and error conditions
3. Verify data consistency between database and UI
4. Check cache behavior with data changes
5. Validate form submissions and validations

## Priority Fix Order

1. Database relationship issues (breaks core functionality)
2. URL routing and view rendering (breaks navigation)
3. User authentication (breaks access)
4. Cache invalidation (causes stale data)
5. Form validation (affects data integrity)
6. Template variables (UI display issues)
7. JavaScript cleanup (memory leaks)
8. Rating display (minor UI issues)