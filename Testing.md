# 🧪 Tales & Tails Bookstore - Testing Documentation

## 📘 Introduction

All pages of the **Tales & Tails Bookstore** website were tested using the **W3C HTML Validator** and various other tools. Most pages were free from errors, with a few exceptions noted below.

These structural issues were systematically addressed to ensure proper compliance with web standards, improving compatibility across different platforms and devices. While modern browsers are often forgiving of HTML inconsistencies, fixing these errors ensures the site adheres to proper specifications.

---

## ✅ HTML Validation Issues and Fixes

### Base Template: Navigation Menu Error

**Issues identified:**
- Extra closing `</li>` tag in the navigation menu
- Character encoding issue with emoji in "Join Pack" link

**Fix implemented:**
- Removed the redundant closing `</li>` tag
- Fixed the emoji display issue by replacing the broken character

---

### Cart Page: Contrast and Form Label Issues

**Issues identified:**
- Insufficient colour contrast for button elements
- Missing form labels for quantity inputs
- Contrast issues with text elements

**Fixes implemented:**
- Enhanced button styles with higher contrast background colours
- Added proper labels to form elements
- Improved text contrast with darker colours
- Removed problematic promo code section

---

### Checkout Page: Security Badge Contrast Issues

**Issues identified:**
- Low contrast text in security badges (🔒 SSL Secure, 💳 Stripe Protected, ✅ PCI Compliant)

**Fix implemented:**
- Redesigned security badges with dark blue text on light blue background
- Added proper ARIA labels for screen readers
- Enhanced focus styles for better accessibility

---

## 🎨 CSS

All CSS was checked using the **W3C CSS Validator**. The stylesheet passes validation with no errors, ensuring cross-browser compatibility and adherence to standards.

The site uses a carefully designed colour system with consistent variables:
- Primary forest green palette for main branding
- Navy blue secondary palette for contrast elements
- Semantic colours with proper contrast ratios

---

## ⚙️ JavaScript

JavaScript code was tested for quality and functionality across all pages.

### 🔍 Search Functionality
- Autocomplete search works properly across devices
- Proper error handling for failed API requests
- Debounced input for performance optimisation
- Responsive dropdown positioning

### 🛒 Cart Management
- Add to cart functionality works correctly
- Quantity controls update properly
- Error handling for out-of-stock items
- Form submissions include proper CSRF protection

---

## 📋 Manual Testing Checklist

### 🧑‍💻 User Role: Visitor

#### Site Navigation & Information
- [x] Access the homepage and view bookstore information  
- [x] Navigate to the books page and browse offerings  
- [x] View book details including author information and pricing  
- [x] See the login and registration options in the navbar  
- [x] Understand the purpose of the site from the homepage  

#### Registration
- [x] Access the registration form from the navbar  
- [x] Complete registration with required fields  
- [x] Receive appropriate validation messages for form errors  
- [x] Successfully create a new account  
- [x] Be redirected to login page after successful registration  

---

### 👤 User Role: Registered Customer

#### Authentication & Profile
- [x] Login with valid credentials  
- [x] Receive appropriate error messages with invalid credentials  
- [x] View profile information  
- [x] Update personal details (name, email)  
- [x] Logout successfully  

#### Shopping Experience
- [x] Browse books by category  
- [x] Search for specific titles or authors  
- [x] Add books to shopping cart  
- [x] Adjust quantities in cart  
- [x] Remove items from cart  
- [x] Complete checkout process  
- [x] View order history  

---

### 🛠️ User Role: Administrator

#### Dashboard & Management
- [x] Log into the admin panel successfully  
- [x] Add new books to the inventory  
- [x] Edit existing book details  
- [x] Manage categories and authors  
- [x] Process orders and update status  

#### Inventory Management
- [x] Add new books with all required information  
- [x] Upload book cover images  
- [x] Update stock levels  
- [x] Mark books as featured  
- [x] Add books to categories  

---

## 🔍 General Functionality Testing

### 📱 Responsiveness
- [x] Homepage displays correctly on mobile (320px and up)  
- [x] Book listings adapt to tablets (768px)  
- [x] Book details view adjusts correctly on different screen sizes  
- [x] Navigation menu collapses to hamburger on smaller screens  
- [x] Form elements resize appropriately on mobile devices  

### ⚠️ Error Handling
- [x] Appropriate messages displayed for form validation errors  
- [x] Custom 404 page shown for invalid URLs  
- [x] Users prevented from adding out-of-stock books  
- [x] Form submissions include CSRF protection  

### 🔐 Security
- [x] Authentication required for accessing profile features  
- [x] Users can only view and modify their own orders  
- [x] Admin-only functions protected from regular users  
- [x] User passwords are properly hashed and secured  

### 🔔 Notifications & Feedback
- [x] Success messages displayed after adding items to cart  
- [x] Confirmation shown after order placement  
- [x] Warning messages shown before cart clearance  

---

## 🌐 Lighthouse Testing

Lighthouse audits were performed on all pages to evaluate performance, accessibility, best practices, and SEO. Tests were conducted in both mobile and desktop configurations.

### 🏠 Home Page Results
- Excellent accessibility implementation with strong scores  
- Good performance across devices  
- Optimised for visual appeal and fast loading times  

### 📚 Book Listing Page Results
- High user experience scores with strong accessibility  
- Well-structured content with fast performance despite image density  

### 🛍️ Cart Page Results
- Balanced interactive elements and accessibility  
- High SEO and Best Practices scores  

### 💳 Checkout Page Results
- Efficient functionality with excellent accessibility  
- Fast load times and optimised payment/security integration  

---

## 🚀 Optimisation Measures Implemented

### 🖼️ Image Optimisation
- Lazy loading for book cover images  
- Proper sizing and responsive images  
- Fallback placeholders for missing images  

### ♿ Accessibility Improvements
- Enhanced colour contrast for text elements and buttons  
- Added proper labels to all form fields  
- Improved focus states for interactive elements  

### ⚡ Performance Enhancements
- Optimised JavaScript with event delegation  
- Reduced unnecessary DOM operations  
- Improved rendering performance  

### 🧑‍💼 Best Practices
- Proper error handling for API requests  
- Enhanced security with CSRF protection  
- Consistent UI patterns throughout the site  

---

## 🌍 Browser Compatibility

The site was tested across major browsers to ensure consistent functionality:
- Google Chrome (latest)
- Mozilla Firefox (latest)
- Safari (latest)
- Microsoft Edge (latest)

---

## ✅ Conclusion

The testing process confirmed that **Tales & Tails Bookstore** functions effectively across different user roles and devices. All identified HTML validation issues have been addressed, and the site now provides a robust and user-friendly shopping experience for dog book enthusiasts.

The focus on accessibility throughout the development process has resulted in a website that can be effectively used by all visitors — including those with disabilities — while maintaining visual appeal and core functionality.