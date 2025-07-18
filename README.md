# 📚🐕 Tales & Tails - Where Every Dog Story Begins

A specialized e-commerce platform for dog training, care, and breed books, built with Django and integrated with Google Books API for comprehensive canine literature.

<div align="center">

# 📚🐕 Tales & Tails
### *Where Every Dog Story Begins*

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen.svg)](https://github.com/Nickflanagn24/bookstore)

*Professional e-commerce platform specializing in dog training, care, and breed books*

[🌐 Live Demo](https://your-heroku-app.herokuapp.com) • [📖 Documentation](docs/) • [🐛 Issues](https://github.com/Nickflanagn24/bookstore/issues)

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

## 📊 Project Structure

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

## 🎨 Features in Detail

### 🛍️ E-commerce System
- **Shopping Cart**: Add, remove, and modify book quantities
- **Secure Checkout**: Stripe integration for payment processing
- **Order Tracking**: Real-time order status updates
- **Order History**: Complete customer order management

### 👤 User Experience
- **Custom Registration**: Dog breed and experience level profiling
- **Personalized Recommendations**: Books tailored to user's dog
- **Professional Design**: Forest green theme with responsive layout
- **Newsletter**: Curated book recommendations and dog care tips

### 🔒 Security & Performance
- **Django Security**: CSRF protection, SQL injection prevention
- **User Authentication**: Secure login/logout with profile management
- **Payment Security**: Stripe handles all sensitive payment data
- **Performance**: Optimized queries and image loading

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

## 🤝 Contributing

This is an educational project. For suggestions or improvements:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

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