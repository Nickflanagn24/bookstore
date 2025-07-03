# bookstore
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

## 🎯 Project Overview

**Purpose**: Create a full-stack e-commerce bookstore that allows customers to browse, search, and purchase books online while providing administrators with comprehensive management tools.

**Target Audience**: 
- Book enthusiasts and casual readers
- Students and researchers
- Gift buyers looking for books
- Authors and publishers

**Business Model**: B2C E-commerce with individual book sales, featured author spotlights, and newsletter subscriptions.

## 🚀 Features

### 🛍️ Customer Features (Planned)
- Browse books by category, author, and genre
- Advanced search functionality powered by Google Books API
- User authentication and profile management
- Shopping cart and secure checkout with Stripe
- Order history and tracking
- Book reviews and ratings
- Wishlist functionality
- Newsletter subscription

### 👨‍💼 Admin Features (Planned)
- Inventory management
- Order processing and fulfillment
- Customer management
- Sales analytics and reporting
- Author and book management
- Featured book promotions

### 🔍 SEO & Marketing
- ✅ Search engine optimized pages
- ✅ Sitemap.xml and robots.txt ready
- ✅ Meta tags and Open Graph integration
- 📋 Facebook business page integration (planned)
- 📋 Newsletter signup integration (planned)
- 📋 Social media sharing (planned)

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7, Python 3.12
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **APIs**: Google Books API (planned), Stripe Payment API (planned)
- **Deployment**: Heroku (planned)
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