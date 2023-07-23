from flask import render_template, request, session, redirect,jsonify,url_for
from flask import current_app as app
from application.database import db
from application.models import *
from passlib.hash import sha256_crypt

@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html", user=session["user"],signed=True)
    else:
        return render_template("home.html", user="None" ,signed=False)


    
@app.route("/register", methods=["GET", "POST"])
def user_registration():
    
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User(name = username, password = password)
        db.session.add(user)
        db.session.commit()
        session["user"] = username
        return redirect("/login")

    return render_template('registration.html', error_message='',x="User")
@app.route('/register/manager', methods=['GET', 'POST'])
def manager_registration():
    if "manager" in session:
        return redirect('/')
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        

        manager = Manager.query.filter_by(username=username).first()
        if manager:
            return render_template('registration.html', error_message='Username already exists')

        new_manager = Manager(username=username, password=password)
        db.session.add(new_manager)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template('registration.html', error_message='',x="Manager")
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(name=username).first()
        if user and sha256_crypt.verify(password, user.password):
            session["user"] = user.name
            return redirect(url_for('market'))

        manager = Manager.query.filter_by(username=username).first()
        if manager and sha256_crypt.verify(password, manager.password):
            session["user"] = manager.username
            return redirect(url_for('manage_category'))

        return render_template('login.html', error_message='Invalid username or password')

    return render_template('login.html', error_message='')
@app.route('/market')
def market():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('userdashboard.html', categories=categories, products=products, user=session["user"])

@app.route('/add_to_cart/<int:category_id>/<int:product_id>', methods=['POST', 'GET'])
def add_to_cart(category_id, product_id):
    if request.method == 'POST':
        quantity_selected = int(request.form.get('quantity'))
        product = Product.query.get(product_id)
        user = User.query.filter_by(name=session["user"]).first()

        if user and product and 0 < quantity_selected <= product.quantity:
            total = product.rate * quantity_selected
            cart_item = CartItem(user_id=user.id, product_id=product_id, quantity=quantity_selected, total=total)
            db.session.add(cart_item)

            # Update the product quantity
            product.quantity -= quantity_selected
            db.session.commit()
            return redirect(url_for('cart'))
        else:
            return jsonify({'message': 'Invalid request'}), 400

    else:
        product = Product.query.get(product_id)
        category = Category.query.get(category_id)
        return render_template('addcart.html', product=product, category=category, user=session["user"])

@app.route('/cart')
def cart():
    user = User.query.filter_by(name=session["user"]).first()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()

    # Create a dictionary to store the grouped cart items
    grouped_cart_items = {}

    for cart_item in cart_items:
        product_name = cart_item.product.name
        if product_name in grouped_cart_items:
            # If product already exists in the dictionary, update quantity and total
            grouped_cart_items[product_name]['quantity'] += cart_item.quantity
            grouped_cart_items[product_name]['total'] += cart_item.total
        else:
            # If product does not exist, add it to the dictionary
            grouped_cart_items[product_name] = {
                'quantity': cart_item.quantity,
                'total': cart_item.total
            }

    # Calculate the total cost of all cart items
    total_cost = sum(cart_item.total for cart_item in cart_items) if cart_items else 0

    return render_template('cart.html', user=session["user"], cart_items=grouped_cart_items, total_cost=total_cost)
@app.route('/delete_cart', methods=['POST'])
def delete_cart():
    product_name_to_delete = request.form.get('product_name')
    user = User.query.filter_by(name=session["user"]).first()
    cart_items_to_delete = CartItem.query.filter_by(user_id=user.id).join(Product).filter(Product.name == product_name_to_delete).all()

    if cart_items_to_delete:
        for cart_item in cart_items_to_delete:
            product = Product.query.get(cart_item.product_id)
            if product:
                # Increase the product quantity back to the cart_item's quantity
                product.quantity += cart_item.quantity
                db.session.delete(cart_item)
        
        db.session.commit()

    return redirect(url_for('cart'))







@app.route('/create_category', methods=['GET', 'POST'])
def manage_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        manager = Manager.query.filter_by(username=session["user"]).first()
        category = Category(name=category_name, creator=manager)
        db.session.add(category)
        db.session.commit()

    categories = Category.query.all()
    return render_template('market.html', categories=categories, user=session["user"])

@app.route('/edit_category/<int:category_id>',methods=["GET","POST"])
def edit_category(category_id):
    if request.method=='POST':
        new_c_name=request.form.get('category_name')
        category=Category.query.get(category_id)
        if not category:
            raise ValueError("Category not found")
        category.name=new_c_name
        db.session.commit()
        return redirect(url_for('manage_category'))
    return render_template("edit_cat.html")



@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()

    return redirect(url_for('manage_category'))

@app.route('/create_product/<int:category_id>', methods=['POST','GET'])
def create_product(category_id):
    if request.method == 'POST':
        product_name = request.form['product_name']
        unit = request.form['unit']
        rate = float(request.form['rate'])
        quantity = int(request.form['quantity'])
        product = Product(name=product_name, unit=unit, rate=rate, quantity=quantity, parent=category_id)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('manage_category'))
    else:
        return render_template('create_product.html')

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('manage_category'))
   

@app.route('/products')
def products():
    all_products = Product.query.all()
    return render_template('products.html', products=all_products)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
# app.py

from datetime import datetime  # Add this import at the top

@app.route('/purchase', methods=['POST'])
def purchase():
    user = User.query.filter_by(name=session["user"]).first()
    cart_items = CartItem.query.filter_by(user_id=user.id).all()

    if cart_items:
        # Create a new entry in the PurchasedProduct table for each cart item
        for cart_item in cart_items:
            purchased_product = PurchasedProduct(
                user_id=user.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                total=cart_item.total,
                purchased_at=datetime.utcnow()  
                
            )
            db.session.add(purchased_product)

        # Clear the user's cart by deleting all cart items
        CartItem.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        return redirect(url_for('purchased_products'))

    return redirect(url_for('cart'))
@app.route('/purchased_products')
def purchased_products():
    user = User.query.filter_by(name=session["user"]).first()
    purchased_products = PurchasedProduct.query.filter_by(user_id=user.id).all()
    
    product=Product.query.all()
    return render_template('purchased_product.html', purchased_products=purchased_products,product=product,user=user.name)