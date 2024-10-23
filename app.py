from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import os
from werkzeug.utils import secure_filename

# Import Helpers file
from helpers import login_required

# Configure Application (Initialize)
app = Flask(__name__)


# Using filesystem 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 to use SQL
db = SQL("sqlite:///budget_admin.db")


# Initialize the database 
def create_tables():
    #create user table
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, hashed_password TEXT NOT NULL)")

# Config for the image implementation
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Define Each Route
with app.app_context():
    create_tables()

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Display cheat Sheet"""
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        # Get the form Data
        budget_type = request.form.get('type')
        budget_title = request.form.get('title')

        item_names = request.form.getlist('item_name[]')
        item_cost = request.form.getlist('item_cost[]')
        item_quantity = request.form.getlist('item_quantity[]')
        profit_percentage = request.form.get('profits')

        # check user input 
        if not budget_type:
            return render_template("error.html", message="Not Budget Type Provided")
        elif not budget_title:
            return render_template("error.html", message="Not Budget title Provided")
        elif not item_names or len(item_names) == 0:
            return render_template("error.html", message="Not Items Provided")
        elif not item_cost or len(item_cost) == 0:
            return render_template("error.html", message="Provide Item Costs")
        elif not item_quantity or len(item_quantity) == 0:
            return render_template("error.html", message="Provide the Total Items")
        try:
            profit_percentage = float(profit_percentage)
        except ValueError:
            return render_template("error.html", message="Invalid Profit Percentage")
        # Process Information
        total_budget = 0
        try:
            for cost, quantity in zip(item_cost, item_quantity):
                total_budget += float(cost) * float(quantity)
        except ValueError:
            return render_template("error.html", message="invalid cost or quantity")

        total_budget *= (1 + (profit_percentage / 100))

        # Store budgets 
        user_id = session.get("user_id")

        if not user_id:
            return redirect("/login")
        
        # Store budget
        budget_id = db.execute("INSERT INTO budgets (user_id, budget_type, budget_title, profit_percentage, total_budget) VALUES (?, ?, ?, ?, ?)",
                    user_id, budget_type, budget_title, profit_percentage, total_budget)
        
        # Store items
        for names, cost, quantity in zip(item_names, item_cost, item_quantity):
            db.execute(
                "INSERT INTO budget_items (budget_id, item_name, item_cost, item_quantity) VALUES (?, ?, ?, ?)",
                budget_id, names, float(cost), float(quantity)
            )

        # DISPLAY SUCCESS
        flash("New Budget Successfully Created!")
        return redirect("/")

@app.route("/history", methods=["GET"])
@login_required
def history():
    """Display a table with all of the budgets created"""

    if request.method == "GET":
        user_id = session.get("user_id")

        # Retrieve the data from database
        budgets = db.execute("SELECT id, budget_type, budget_title, total_budget, timestamp FROM budgets WHERE user_id = ? ORDER BY timestamp DESC",
                             user_id)

        return render_template("history.html", budgets=budgets)

@app.route("/budget/<int:budget_id>")
@login_required
def view_budget(budget_id):
    """Display the budget_id INFO"""
    budget = db.execute("SELECT budget_type, budget_title, timestamp, profit_percentage, total_budget FROM budgets WHERE id = ? AND user_id = ?",
                        budget_id, session.get("user_id"))
    
    items = db.execute("SELECT item_name, item_cost, item_quantity FROM budget_items WHERE budget_id = ?",
                       budget_id)

    return render_template("view_budget.html", budget=budget, items=items)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Prompt the user to check username and password"""
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("error.html", message="Not username Provided")
        elif not password:
            return render_template("error.html", message="Provide a Password")
        
        # Check if user exists

        user = db.execute("SELECT id, hashed_password FROM users WHERE username = ?", username)
        if not user:
            return render_template("error.html", message="Not Registered User")
        # Compare input password with hashed one
        if not check_password_hash(user[0]["hashed_password"], password):
            return render_template("error.html", message="Incorrect Password")
        
        # Log user in
        session["user_id"] = user[0]["id"]

        #Redirect to main route
        return redirect("/")
        

@app.route("/register", methods=["GET", "POST"])
def register():
    """Prompt user to define username and password"""
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        # Getting user input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check user Input
        if not username:
            return render_template("error.html", message="Input A Username")
        elif not password:
            return render_template("error.html", message="Input a Password")
        elif not confirmation:
            return render_template("error.html", message="Confirm Password")
        elif not confirmation == password:
            return render_template("error.html", message="Passwords do not match")
        
        # Check if the user already exist
        existing_user = db.execute("SELECT * FROM users WHERE username == ?", username)
        if existing_user:
            return render_template("error.html", message="User already Exist")
        else:
            # Hash, Store, Login User
            hashed_password = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", username, hashed_password)
            flash("User Successfully Registered")
            return redirect("/")




@app.route("/user_profile", methods=["GET"])
@login_required
def user_profile():
    """ Manage User profile options """
    if request.method == "GET":
        user_id = session["user_id"]
        user_data = db.execute("SELECT username, profile_image FROM users WHERE id = ?", user_id)
        return render_template("user_profile.html", user=user_data[0])


@app.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template("error.html", message="No file part")
        
        file = request.files['image']

        if file.filename == '':
            return render_template("error.html", message="No selected file")
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(file_path)

            user_id = session.get('user_id')
            db.execute("UPDATE users SET profile_image = ? WHERE id = ?", file_path, user_id)

            flash("profile image uploaded successfully!")

            return redirect(url_for('user_profile'))
        
    return render_template('user_profile.html')

if __name__ == "__main__":
    app.run(debug=True)
