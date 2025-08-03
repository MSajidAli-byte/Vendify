# Multi-Vendor E-commerce Platform

A full-featured multi-vendor e-commerce website built with Django. This platform allows sellers to register and list their products, while customers can browse, purchase, and manage their orders.

## Features

### For Customers
- **User Authentication**: Secure signup, login, logout, and password reset functionality.
- **Profile Management**: Edit personal details, profile picture, and change password.
- **Product Discovery**: Browse all products, view single product details, search for products, and filter by category.
- **Shopping Cart**: Add products to the cart, view the cart, update item quantities, and remove items.
- **Checkout Process**: Integrated with PayPal and JazzCash for payments.
- **Order History**: View a history of all past orders and their status.

### For Sellers
- **Seller Registration**: A separate registration flow for sellers.
- **Seller Dashboard**: A dedicated dashboard to manage products and view sales information.
- **Product Management**: Add new products, update existing product details, and delete products from the catalog.
- **My Products View**: See a list of all products listed by the seller.

### Admin
- **Admin Panel**: A comprehensive Django admin panel to manage users, products, categories, orders, and more.

## Tech Stack

- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite 3 (default)
- **Payment Gateways**:
  - PayPal (via `django-paypal`)
  - JazzCash (custom integration)

## Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

- Python 3.8+
- Pip (Python Package Installer)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/secondproject.git
cd secondproject
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

This project uses a `.env` file to manage sensitive information like secret keys and API credentials.

- Make a copy of the `.env.example` file and rename it to `.env`.
  ```bash
  cp .env.example .env
  ```
- Open the `.env` file and fill in your actual credentials for the `SECRET_KEY`, email server, and payment gateways.

### 5. Apply Database Migrations

Create the database schema by running the migrations.

```bash
python manage.py migrate
```

### 6. Create a Superuser

To access the Django admin panel, you need to create a superuser account.

```bash
python manage.py createsuperuser
```
Follow the prompts to set up your username, email, and password.

### 7. Run the Development Server

You're all set! Start the development server.

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin/`.
- Register as a "Seller" to add products.
- Register as a "Customer" to browse and buy products.
