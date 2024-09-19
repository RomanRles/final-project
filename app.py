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

@app.route("/register")
def register():
    """Prompt user to define username and password"""

    return render_template("register.html", message="TODO")

@app.route("/log_out")
@login_required
def log_out():
    """ Get the user out of the session """

    return render_template("error.html", message="TODO")


if __name__ == "__main__":
    app.run(debug=True)
