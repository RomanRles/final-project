from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

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

# Define Each Route
with app.app_context():
    create_tables()

@app.route("/")
@login_required
def index():
    """Display cheat Sheet"""
    
    return render_template("error.html", message="TODO")

@app.route("/history")
@login_required
def history():
    """Display a table with all of the budgets created"""

    return render_template("error.html", message="TODO")

@app.route("/login")
def login():
    """Prompt the user to check username and password"""

    return render_template("layout.html", message="TODO")

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




@app.route("/log_out")
@login_required
def log_out():
    """ Get the user out of the session """

    return render_template("error.html", message="TODO")


if __name__ == "__main__":
    app.run(debug=True)
