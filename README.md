Flask E-Commerce Web Application
This is a Flask-based E-commerce web application project developed by Himanshu Pathak. It allows users to browse and purchase products, manage their shopping cart, and view their purchased products. Managers can create new categories and add products to each category.

Technologies Used:-
Flask: A lightweight web framework used for building the backend of the application.
Flask-SQLAlchemy: An extension used for database management with SQLAlchemy ORM.
Flask-WTF: Used for handling forms and data validation.
Jinja2 Templating Engine: Used for rendering dynamic content on the frontend.
Bootstrap: For styling and responsive design.
HTML, CSS, and JavaScript: For frontend development and user interface.

Features

User Registration and Login: Users can sign up and log in to their accounts to access personalized features.
Product Display: The application displays various product categories and their associated products.
Cart Functionality: Users can add products to their cart, view the cart contents, and update quantities.
Purchase Products: Users can purchase the products in their cart, and the quantity of purchased items will be deducted from the available stock.
User Dashboard: Users can view their purchased products and order history.
Manager Registration and Login: Managers can sign up and log in to their accounts to manage the market.
Category and Product Creation: Managers can create new categories and add products to each category. They can also manage existing categories and products.

Installation

Clone the repository to your local machine:

git clone https://github.com/pathakvishal132/GreenMarket
Navigate to the project directory:

cd flask-ecommerce-app
Set up a virtual environment (optional but recommended):

python3 -m venv venv
source venv/bin/activate # On Windows, use 'venv\Scripts\activate'
Install the required packages:

pip install -r requirements.txt
Go to the code folder:

cd code
Run the application:

python3 main.py
Access the application in your web browser at http://localhost:5000/.
Usage

Visit the homepage to browse products and add them to your cart.
Click on the "Cart" link in the navigation bar to view and manage your cart items.
To purchase the items in your cart, click on the "Checkout" button on the cart page.
After a successful purchase, you can view your purchased products on the "Purchased Products" page.

Future Improvements

Implement user profiles to allow users to update their personal information and view order history.
Add product search functionality to enable users to search for specific products.
Implement product reviews and ratings to enhance user engagement.
Integrate payment gateways for real transactions.
