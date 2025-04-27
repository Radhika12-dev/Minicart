# Orders Management System

This is a simple **FastAPI** application for managing customers, products, and orders, with functionality to view and create customers, products, and orders.

### Features:
- Create and view customers
- Create and view products
- Create and view orders
- Fetch orders by customer name

## Installation

To run this project locally, follow the steps below:

### 1. Clone the Repository
https://github.com/Radhika12-dev/Minicart.git

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt

# Run database migrations
python -m db

# Run the FastAPI app
uvicorn main:app --reload



