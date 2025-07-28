# 📚🐕 Tales & Tails - Where Every Dog Story Begins

A specialised e-commerce platform for dog training, care, and breed books, built with Django and integrated with Google Books API for comprehensive canine literature.

<div align="center">

# 📚🐕 Tales & Tails
### *Where Every Dog Story Begins*

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen.svg)](https://github.com/Nickflanagn24/bookstore)

*Professional e-commerce platform specializing in dog training, care, and breed books*

[🌐 Live Demo](https://tales-and-tails-bookstore-2b31d0bd7c27.herokuapp.com/) • [📖 Documentation](docs/) • [🐛 Issues](https://github.com/Nickflanagn24/bookstore/issues)

</div>

---

##  Overview

Tales & Tails is a specialized Django-based e-commerce platform dedicated to dog-related literature. We serve dog owners, professional trainers, veterinarians, and canine enthusiasts with expertly curated books and resources.

**Mission Statement**: *"Every great dog story starts with the right book."*

### ✨ Key Features

- 🛍️ **E-commerce**: Full shopping cart and secure Stripe checkout
- 📚 **Smart Search**: Google Books API integration for comprehensive catalog
- 👤 **Custom Profiles**: Dog-specific user profiles and personalized recommendations
- 📧 **Email System**: Order confirmations and customer communications
- 📱 **Responsive Design**: Mobile-first with professional forest green theme
- 🔐 **Secure**: Django security best practices and authentication

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

**1. Clone the repository**

git clone https://github.com/Nickflanagn24/bookstore.git
cd bookstore

**2. Set up virtual environment**

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

**3. Install dependencies**

pip install -r requirements.txt

**4. Configure environment variables**

**Create .env file with:**

SECRET_KEY=your-secret-key-here<br>
DEBUG=True<br>
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key<br>
STRIPE_SECRET_KEY=sk_test_your_stripe_key<br>
GOOGLE_BOOKS_API_KEY=your_google_books_key<br>

**5. Set up database**

python manage.py makemigrations <br>
python manage.py migrate<br>
python manage.py createsuperuser<br>

**6. Run development server**

python manage.py runserver

Visit `http://localhost:8000` to see your local instance! 🎉

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Backend** | Django 4.2.7, Python 3.12 |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5 |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **Payments** | Stripe API |
| **APIs** | Google Books API |
| **Deployment** | Heroku |

## Project Structure

### Core Directories

- **bookstore_project/** - Main Django project configuration
  - `settings.py` - Application settings and configuration
  - `urls.py` - URL routing and patterns  
  - `wsgi.py` - WSGI configuration for deployment

### Applications

- **books/** - Book catalog and management
- **cart/** - Shopping cart functionality
- **orders/** - Order processing and tracking
- **accounts/** - User authentication and profiles

### Static Files

- **templates/** - HTML template files
- **static/** - CSS, JavaScript, and image files
- **requirements.txt** - Python package dependencies

# E-commerce System

## Shopping Cart Functionality
- **Intuitive Interface**: Add books to cart with a single click  
- **Real-time Updates**: Cart updates without page reload  
- **Item Management**: Modify quantities or remove items directly from cart  
- **Persistent Cart**: Cart remains across sessions for logged-in users  
- **Visual Indicators**: Cart total and item count in navigation  

## Secure Checkout
- **Stripe Integration**: Secure payment gateway implementation  
- **Payment Options**: Support for major credit/debit cards  
- **Data Security**: SSL/TLS encryption for all transaction data  
- **Compliance**: PCI-compliant payment processing  
- **Webhooks**: Implementation for reliable order completion  

## Order Tracking
- **Reference Numbers**: Unique identifiers for each purchase  
- **Email Notifications**: Alerts at key order stages  
- **Status Dashboard**: Updates viewable in user account  
- **Delivery Estimates**: Timeline information where applicable  

## Order History
- **Purchase Archive**: Complete history accessible to users  
- **Detailed Records**: Order information including dates, items, and prices  
- **Documentation**: Receipt/invoice generation for completed orders  
- **Reordering**: Option to repurchase previously ordered books  

---

# Book Catalog Management

## Google Books API Integration
- **Dynamic Catalog**: Latest dog-related publications automatically included  
- **Rich Information**: Access to extensive metadata and details  
- **Availability Status**: Real-time API checks for book availability  
- **Review System**: Integration with Google's ratings and reviews  

## Smart Search
- **Advanced Filtering**: Search by dog breed, training type, and experience level  
- **Predictive Text**: Suggestions appear as users type  
- **Category Navigation**: Browse options by predefined categories  
- **Sorting Options**: Arrange by relevance, price, or publication date  

## Book Metadata
- **Detailed Descriptions**: Comprehensive summaries and content information  
- **Author Information**: Biographies and credentials of writers  
- **Publication Details**: Publisher, date, and edition data  
- **Physical Attributes**: Page count and format specifications  
- **Cataloging**: ISBN identification and classification  

## High-Quality Cover Images
- **Visual Appeal**: High-resolution book covers from Google Books API  
- **Consistent Display**: Uniform image sizing and quality throughout  
- **Fallback System**: Default images for any missing covers  
- **Performance**: Optimized loading for faster page rendering  

---

# User Management

## Custom Registration System
- **Streamlined Signup**: User-friendly process with minimal required fields  
- **Dog Profiles**: Breed, age, and training needs captured during registration  
- **Experience Assessment**: Level evaluation for personalized recommendations  
- **Marketing Opt-in**: Newsletter subscription option during registration  

## Secure Authentication
- **Password Security**: Strong requirements and validation  
- **Account Recovery**: Reset functionality via email  
- **Convenience**: "Remember me" functionality for returning users  
- **Protection Measures**: Session timeouts and brute force prevention  

## Personalised Recommendations
- **Breed-Specific**: Algorithm-based book suggestions for your dog  
- **Skill-Appropriate**: Training level matched recommendations  
- **Browse History**: Recently viewed items tracking  
- **Related Content**: Similar book suggestions on product pages  

## User Profiles
- **Customisation**: Adjustable user dashboards  
- **Multiple Dogs**: Support for several dog profiles under one account  
- **Reading Tools**: History tracking and wishlist functionality  
- **Preferences**: Customizable communication settings  

---

# Communication Systems

## Email Notifications
- **Order Updates**: Automated confirmations with purchase details  
- **Shipping Alerts**: Delivery status communications  
- **Account Security**: Password reset and verification messages  
- **Marketing**: Special offers for registered users  
- **Onboarding**: Welcome emails for new registrations  

## Newsletter
- **Subscription Options**: Opt-in during registration or via website  
- **Curated Content**: Regular articles about dog training and care  
- **New Releases**: Announcements about latest book additions  
- **Promotions**: Seasonal deals and special offers  
- **Expert Tips**: Training advice from professional dog trainers  

---

# Design & User Experience

## Responsive Design
- **Device Compatibility**: Mobile-first development approach  
- **Adaptive Layouts**: Optimized for smartphones, tablets, and desktops  
- **Touch-Friendly**: Elements designed for mobile users  
- **Cross-Device Consistency**: Uniform experience across all screen sizes  
- **Flexible Images**: Graphics that scale appropriately to device  

## Professional Theme
- **Color Scheme**: Forest green primary palette reflecting nature and books  
- **Typography**: Consistent font usage throughout the application  
- **Navigation**: Intuitive menu structure and information hierarchy  
- **Thematic Elements**: Dog-themed visuals and iconography  
- **Clean Interface**: Uncluttered, focused design  

## Bootstrap 5 Integration
- **Component Library**: Modern UI elements for consistent experience  
- **Grid System**: Responsive layout framework for flexibility  
- **Custom Styling**: Bootstrap components matched to site theme  
- **Accessibility**: Built-in features from Bootstrap framework  
- **Browser Support**: Cross-browser compatibility  

---

# Security Features

## CSRF Protection
- **Form Security**: Validation tokens to prevent cross-site request forgery  
- **Request Verification**: Automatic token checking on all POST requests  
- **Cookie Handling**: Secure processing and validation  
- **Session Protection**: Guards against hijacking attempts  

## SQL Injection Prevention
- **Query Security**: Parameterized database interactions  
- **ORM Implementation**: Django's object-relational mapper for safe queries  
- **Input Validation**: Thorough sanitization of user inputs  
- **Permission Limits**: Restricted database user access  

## Secure Payment Handling
- **No Local Storage**: Credit card details never stored on our servers  
- **Tokenization**: Secure payment processing via Stripe  
- **Industry Standards**: Compliance with PCI requirements  
- **Secure Transfer**: Protected handoff to payment processor  

## Authentication Security
- **Hashing**: Password protection using Django's security best practices  
- **Access Controls**: Rate limiting on login attempts  
- **Recovery Security**: Secure password reset mechanisms  
- **Session Encryption**: Protected user session data  

---

# Technical Infrastructure

## PostgreSQL Database (Production)
- **Relational Structure**: Robust database for production environment  
- **Data Integrity**: Foreign key constraints and relationships  
- **Query Performance**: Optimized database interactions  
- **Backup System**: Regular automated data preservation  

## SQLite Database (Development)
- **Lightweight Solution**: Simplified database for local development  
- **Quick Setup**: Easy configuration for development environment  
- **Self-Contained**: No separate database server required  
- **Iteration Support**: Enables rapid development cycle  

## Heroku Deployment
- **Cloud Platform**: Reliable hosting infrastructure  
- **Scalability**: Automatic resource adjustment capabilities  
- **Continuous Deployment**: Integrated with Git workflow  
- **Environment Management**: Secure variable handling for configuration  

## Performance Optimization
- **Loading Techniques**: Lazy loading of images for faster pages  
- **Query Efficiency**: Optimised database access and caching  
- **File Optimization**: Minified static resources (CSS, JavaScript) 

---

##  SEO Implementation

Tales & Tails implements several SEO best practices to improve search visibility and user experience:

### Technical SEO
- **robots.txt**: Controls search engine crawling with appropriate allow/disallow rules
- **sitemap.xml**: Dynamic XML sitemap generated from Django models
- **Meta tags**: Comprehensive meta tags including description, keywords, Open Graph and Twitter Card support
- **Custom 404 page**: User-friendly error page with helpful navigation options

### On-page SEO
- **Semantic HTML**: Proper heading structure and HTML5 semantic elements throughout the site
- **External links**: All external links include appropriate rel attributes for security and SEO benefits
- **Mobile responsiveness**: Site is fully optimized for mobile devices
- **Content strategy**: All content is dog-specific with no placeholder text

---

## 📈 Marketing Strategy

Tales & Tails employs a multi-channel marketing approach targeting the specialised niche of dog owners, trainers, and veterinary professionals seeking quality canine literature.

### Target Audience Segmentation

Our marketing strategy focuses on four primary customer segments:

1. **Pet Parents** - Dog owners seeking training and care guides
2. **Professional Trainers** - Looking for advanced methodology resources
3. **Veterinary Professionals** - Requiring medical and behavioural reference materials
4. **Breed Enthusiasts** - Collectors of breed-specific books and information

### Digital Marketing Channels

**Social Media Strategy**
- **Facebook**: Curated content featuring dog training tips, breed spotlights, and new book announcements
- **Instagram**: Visual content showcasing beautiful book photography and "dog and book" themed imagery
- **Pinterest**: Infographics and visual guides on dog training techniques sourced from our book collection
- **Twitter**: Engagement with dog training community, sharing expert quotes from featured books

**Email Marketing**
- Welcome series introducing new customers to dog book categories
- Personalised recommendations based on dog breed and training needs
- Monthly newsletter featuring new releases and training tips
- Seasonal promotions tied to dog training milestones (puppy season, competition season)

**Content Marketing**
- Blog featuring excerpts from popular training books
- Guest posts from featured authors and dog training experts
- "Dog Training 101" series to attract beginner dog owners
- "Ask the Expert" Q&A sessions with veterinarians and trainers

### Loyalty & Retention Programme

- **The Pack Membership**: Subscription offering 10% discount and early access to new releases
- Breed-specific book bundles at discounted rates
- Referral programme offering store credit for new customer referrals
- Review rewards programme to encourage customer testimonials

### Offline Marketing Initiatives

- Partnerships with dog training schools and veterinary practices
- Presence at dog shows and canine sporting events with pop-up bookshop
- Book signing events with popular dog training authors
- Community workshops based on book content, held in local dog training facilities

### Metrics & Measurement

Our marketing effectiveness is tracked through:
- Conversion rate by traffic source
- Customer acquisition cost by channel
- Lifetime value segmented by dog breed interest
- Email engagement metrics (open rate, click-through rate)
- Social media engagement and growth

This specialised marketing approach allows Tales & Tails to efficiently reach our target audience and position ourselves as the premier destination for canine literature and professional dog training resources.

---

## 🚀 Deployment

### Heroku Deployment
**Create Heroku app**
heroku create your-app-name

**Add PostgreSQL**
heroku addons:create heroku-postgresql:hobby-dev

**Set environment variables**
heroku config:set SECRET_KEY=your-production-secret
heroku config:set DEBUG=False
heroku config:set STRIPE_PUBLISHABLE_KEY=your-stripe-key
heroku config:set STRIPE_SECRET_KEY=your-stripe-secret
heroku config:set GOOGLE_BOOKS_API_KEY=your-google-key

**Deploy**
git push heroku main
heroku run python manage.py migrate

## 🧪 Testing

Run the test suite:
*Add test command here*

### Test Coverage
- User authentication and profiles
- E-commerce functionality (cart, checkout, orders)
- Payment processing integration
- Book search and catalog features

## 📖 API Documentation

### Stripe Integration
- **Checkout Sessions**: Secure payment processing
- **Webhooks**: Order status updates
- **Test Cards**: Development testing support

### Google Books API
- **Search**: Advanced book discovery
- **Metadata**: Comprehensive book information
- **Images**: High-quality book covers

## 📄 License

This project is developed for educational purposes as part of a Full-Stack Development course.

## 🙏 Acknowledgments

- Django community for excellent documentation
- Stripe for secure payment processing
- Google Books API for comprehensive book data
- Bootstrap for responsive design components

---

<div align="center">

**Tales & Tails** • *Professional Dog Book Specialists*

Made with  for dog lovers everywhere

</div>