# 📚🐕 Tales & Tails - Where Every Dog Story Begins

A specialized e-commerce platform for dog training, care, and breed books, built with Django and integrated with Google Books API for comprehensive canine literature.

## 🎯 Project Overview

**Purpose**: "Tales & Tails" is where every dog story begins with the right book. We specialize in curating the best dog-related literature for owners, trainers, and veterinary professionals.

**Brand Mission**: *"Every great dog story starts with the right book."*

**Target Audience**: 
- Dog owners seeking training and care guidance
- Professional dog trainers and behaviorists  
- Veterinarians and veterinary students
- Dog breeders and breed enthusiasts
- Anyone who loves dogs and learning about them

**Business Model**: B2C E-commerce specializing in dog-related books, from puppy training tales to professional veterinary texts.

## 🚀 Features

### 🛍️ Customer Features
- ✅ Browse books by category, author, and genre
- ✅ Advanced search functionality powered by Google Books API
- ✅ User authentication and profile management with dog-specific fields
- ✅ Shopping cart and secure checkout with Stripe
- ✅ Order history and tracking with status updates
- ✅ Newsletter subscription
- ✅ Premium responsive design with forest green theme
- 📋 Book reviews and ratings (planned)
- 📋 Wishlist functionality (planned)

### 👨‍💼 Admin Features
- ✅ Comprehensive inventory management
- ✅ Order processing and fulfillment with status tracking
- ✅ Customer management with detailed profiles
- ✅ Newsletter subscriber management
- ✅ Author and book management
- ✅ Featured book promotions
- 📋 Sales analytics and reporting (planned)

### 🔍 SEO & Marketing
- ✅ Search engine optimized pages
- ✅ Sitemap.xml and robots.txt ready
- ✅ Meta tags and Open Graph integration
- ✅ Newsletter signup integration
- 📋 Facebook business page integration (planned)
- 📋 Social media sharing (planned)

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7, Python 3.12
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Payment Processing**: Stripe API (integrated)
- **External APIs**: Google Books API (integrated)
- **Deployment**: Heroku (configured)
- **Version Control**: Git & GitHub

## 📋 Prerequisites

- Python 3.8+
- Git
- GitHub Codespaces or local development environment

## 📦 Orders & Payment System

### Overview
Tales & Tails features a complete e-commerce order management system integrated with Stripe for secure payment processing. The system provides full order tracking, status management, and customer order history.

### Order Management Features

#### 🛒 Order Creation & Processing
- **Automatic Order Creation**: Orders are created before Stripe checkout to ensure no data loss
- **Unique Order Numbers**: Each order gets a unique identifier in format `TT-YYYYMMDD-XXXXX`
- **Order Status Tracking**: Real-time status updates from pending to delivered
- **Payment Integration**: Seamless Stripe payment processing with webhook support

#### 📊 Order Status Workflow
Pending → Confirmed → Processing → Shipped → Delivered ↓ (Cancelled - if needed)


#### 🔄 Complete Order Lifecycle
1. **Cart to Order**: Items from shopping cart are converted to order items
2. **Stripe Checkout**: Secure payment processing with Stripe
3. **Order Confirmation**: Automatic status update after successful payment
4. **Status History**: All status changes are tracked with timestamps
5. **Customer Notifications**: Order confirmations and status updates

### Technical Implementation

#### Models
- **Order Model**: Core order information with customer details and payment status
- **OrderItem Model**: Individual items within orders with pricing snapshots
- **OrderStatusHistory Model**: Complete audit trail of all order status changes

#### Payment Flow Integration
```python
# Simplified flow:
1. User initiates checkout
2. Order created with 'pending' status
3. Stripe session created with order metadata
4. User completes payment on Stripe
5. Webhook/success handler confirms order
6. Order status updated to 'confirmed'
7. Cart cleared, customer redirected to success page

#### Database Schema
Core Models & Relationships
CustomUser (Extended Django User)
├── Orders (1:many)
│   └── OrderItems (1:many with Books)
├── Cart (1:1)
│   └── CartItems (1:many with Books)
└── Newsletter Subscriptions (1:many)

Books (Central Model)
├── Authors (many:many)
├── Categories (many:many)
├── OrderItems (1:many)
└── CartItems (1:many)

Categories
└── Books (many:many)

Authors  
└── Books (many:many)

#### Additional Models:
- ContactMessage (for contact form submissions)
- OrderStatusHistory (audit trail)

#### Custom User Model Features

Dog-specific profile fields (breed, age, training level)
Newsletter subscription preferences
Marketing communication settings
Professional credentials for discounts

### E-commerce Business Model (LO6.1)

#### Revenue Streams
Direct Book Sales: Primary revenue from individual book purchases
Professional Subscriptions: Premium content for trainers and veterinarians
Bulk Orders: Educational institutions and training facilities
Affiliate Partnerships: Commission from publisher partnerships

#### Value Proposition
Expert Curation: Professional selection by certified trainers and veterinarians
Specialized Focus: Deep expertise in canine education and training
Personalized Recommendations: Tailored suggestions based on dog breed and owner experience
Professional Network: Connection to certified trainers and veterinary professionals

#### Target Market Segmentation
New Dog Owners (35%): First-time puppy parents seeking guidance
Professional Trainers (25%): Certified professionals needing advanced resources
Veterinary Professionals (20%): Medical professionals and students
Experienced Enthusiasts (20%): Breed specialists and advanced owners
 
###Installation & Setup
#### Local Development Setup

#### Clone Repository
#### 1. Copygit clone https://github.com/Nickflanagn24/bookstore.git
cd bookstore

#### 2. Create Virtual Environment
Copypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

#### 3.Install Dependencies
Copypip install -r requirements.txt

#### 4.Environment Configuration
Copy# Create .env file with:
SECRET_KEY=your-secret-key
DEBUG=True
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key
GOOGLE_BOOKS_API_KEY=your-google-books-api-key

#### 5. Database Setup
Copypython manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
#### 6.Run Development Server
Copypython manage.py runserver
 
### Deployment Procedures (LO1.19)
##### Heroku Deployment
#### 1.Heroku Setup
Copyheroku create tales-and-tails-bookstore
heroku addons:create heroku-postgresql:hobby-dev

#### 2. Variables
Copyheroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DEBUG=False
heroku config:set STRIPE_PUBLISHABLE_KEY=your-stripe-key
heroku config:set STRIPE_SECRET_KEY=your-stripe-secret-key
heroku config:set GOOGLE_BOOKS_API_KEY=your-google-books-key

#### 3.Database Migration
Copyheroku run python manage.py migrate
heroku run python manage.py createsuperuser

#### 4.Static Files
Copyheroku run python manage.py collectstatic --noinput

Security Configuration
DEBUG=False in production
Secure secret key management
HTTPS enforcement
CSRF protection enabled
SQL injection prevention
XSS protection headers

## 🧪 Testing Procedures (LO2.3)

### Manual Testing

#### User Authentication Testing

##### Registration Process
- Valid registration with dog profile information
- Email validation and unique username enforcement
- Password strength validation

##### Login/Logout Process
- Successful login with correct credentials
- Error handling for invalid credentials
- Session management and logout functionality

#### E-commerce Functionality Testing

##### Shopping Cart
- Add items to cart
- Update quantities
- Remove items
- Cart persistence across sessions

##### Checkout Process
- Order creation before payment
- Stripe payment integration
- Order confirmation after successful payment
- Error handling for failed payments

##### Order Management
- Order history access
- Order detail views
- Status tracking functionality

#### Payment Testing

##### Stripe Test Cards
- **Success**: 4242424242424242
- **Declined**: 4000000000000002
- **Insufficient funds**: 4000000000009995

### Automated Testing Framework

```python
# Example test structure
class OrderTestCase(TestCase):
    def test_order_creation(self):
        # Test order creation process
        
    def test_stripe_integration(self):
        # Test payment processing
        
    def test_order_status_updates(self):
        # Test status change functionality

Performance Testing

Load Performance
Page load times under 3 seconds

Database query optimization
Image optimization for book covers
CDN implementation for static files
📊 

User Stories & Agile Development (LO2.2, LO2.7)

Epic 1: User Authentication
US001: As a dog owner, I want to create an account with my dog's information
US002: As a user, I want to securely log in to access my profile
US003: As a user, I want to update my profile and dog information

Epic 2: Book Discovery
US004: As a dog owner, I want to browse books by my dog's breed
US005: As a trainer, I want to search for professional training resources
US006: As a user, I want to see featured and recommended books

Epic 3: Shopping & Checkout
US007: As a customer, I want to add books to my cart
US008: As a customer, I want to securely pay for my order
US009: As a customer, I want to track my order status

Epic 4: Communication
US010: As a user, I want to subscribe to the newsletter
US011: As a user, I want to contact customer support
US012: As a user, I want to receive order confirmations

Development Methodology
- Agile Sprints: 2-week development cycles
- User Story Mapping: Feature prioritization based on user value
- Continuous Integration: Automated testing and deployment
- Regular Retrospectives: Process improvement and team feedback


UX Design & Accessibility (LO2.1, LO2.5)

Design Principles
- Professional Forest Green Theme: Reflects natural, trustworthy brand
- Intuitive Navigation: Clear information architecture
- Mobile-First Design: Responsive across all devices
- Accessibility Compliance: WCAG 2.1 guidelines

User Experience Features
- Personalized Recommendations: Based on dog breed and experience level
- Visual Book Discovery: High-quality cover images and descriptions
- Streamlined Checkout: Minimal steps from cart to confirmation
- Professional Design: Premium feel matching target audience expectations

Wireframes & Mockups
-Homepage design with featured books and categories
-Product detail pages with comprehensive book information
-Shopping cart and checkout flow diagrams
-User profile and order history layouts

    Marketing Strategy (LO5.1)
 Digital Marketing Approach
- Content Marketing: Dog training tips and breed-specific guides
- Email Campaigns: Newsletter with book recommendations
- Social Media: Facebook business page with community engagement
- SEO Optimization: Ranking for dog training book searches
- Professional Partnerships: Collaboration with training schools
 Facebook Business Page Strategy
- Regular posts featuring new book arrivals
- Dog training tips and educational content
- Customer success stories and testimonials
- Live Q&A sessions with professional trainers
- Targeted advertising to dog owner demographics

    Newsletter Strategy
- Weekly book recommendations based on subscriber preferences
- Exclusive discounts for newsletter subscribers
- Early access to new releases and featured books
- Training tips and dog care advice from experts

    Security Features (LO4.1-4.6)
Authentication & Authorization
- Custom User Model: Extended with dog-specific profile fields
- Role-based Access: Different permissions for customers, staff, and admins
- Session Management: Secure login state tracking
- Password Security: Django's built-in password hashing

    Data Protection
- CSRF Protection: Form submission security
- SQL Injection Prevention: Django ORM protection
- XSS Protection: Template escaping and security headers
- Secure Payment Processing: Stripe handles all sensitive card data

    Access Control
- Users can only access their own orders and profile
- Admin panel restricted to staff users
- API endpoints protected with authentication
- Sensitive operations require login confirmation

    Project Reflection
Challenges Overcome
- Stripe Integration: Complex payment flow with order management
- Google Books API: Handling large datasets and API rate limits
- User Experience: Balancing professional design with usability
- Database Design: Efficient schema for e-commerce operations

    Learning Outcomes Achieved
- Full-stack web development with Django
- Payment processing integration
- API integration and data management
- Professional UI/UX design principles
- E-commerce business model understanding

Future Enhancements
- Advanced Search: AI-powered book recommendations
- Community Features: User reviews and rating system
- Mobile App: Native iOS/Android application
- International Shipping: Global marketplace expansion
- Subscription Model: Monthly book subscription boxes

    License
This project is developed for educational purposes as part of a Full-Stack Development course.

 Contributing
This is an educational project. For suggestions or improvements, please contact the development team.

## 📋 Project Management

### Development Workflow
This project follows Agile development methodology with 2-week sprints.

**Track Progress**: [GitHub Project Board](https://github.com/yourusername/yourrepo/projects/1)

### Current Sprint
- **Sprint 1**: User Authentication System
- **Duration**: 2 weeks
- **Goal**: Complete user registration, login, and profile management

### User Stories Progress
- [ ] US001: User Registration with Dog Profile
- [ ] US002: Secure Login/Logout Functionality  
- [ ] US003: Profile Management and Updates

### Development Process
1. **Backlog**: All user stories and features
2. **Sprint Planning**: Select items for current sprint
3. **Current Sprint**: Active development work
4. **In Progress**: Currently coding
5. **Review**: Testing and code review
6. **Done**: Completed features


© 2025 Tales & Tails. All rights reserved. "Every great dog story starts with the right book."