import re
import bcrypt
from flask import Flask, flash, redirect, render_template, request, session
import sqlite3
from flask_session import Session

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        # Ensure username was submitted
        if not username:
            return render_template("apology.html", message="User name must be provided")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", message="Password must be provided")
        with sqlite3.connect('books.db') as conn:
            # Ustawienie row_factory na sqlite3.Row
            conn.row_factory = sqlite3.Row  
            db = conn.cursor()
            # Query database for username
            row = db.execute("SELECT id, hash FROM users WHERE username = ?", [username]).fetchone()
            # Ensure username exists and password is correct
            if row is None:
                return render_template("apology.html", message="Invalid username. Please try again.")
            provided_password = request.form.get("password").encode('utf-8')
            hashed_password = row["hash"]
            if not bcrypt.checkpw(provided_password, hashed_password):
                return render_template("apology.html", message="Invalid password. Please try again.")

            # Remember which user has logged in
            session["user_id"] = row["id"]

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""
    if request.method == "POST":
      with sqlite3.connect('books.db') as conn:
        db = conn.cursor()
        username = request.form.get("username")
        print(username)
        if not username:
            return render_template("apology.html", message="Username must be provided")
        userDB = db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()
        if len(userDB) != 0:
            return render_template("apology.html", message="Username already exists")

        password = request.form.get("password")
        if len(password) < 5 or not re.search(r"[a-z]", password) or not re.search(r"[\d]", password):
            return render_template("apology.html", message="Password must be at least 5 characters long and contain at least one number and one letter")

        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return render_template("apology.html", message="Passwords do not match")
        password_bytes = password.encode('utf-8')
        print(password_bytes)
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        print(hashed)
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)", (username,hashed)
        )
        return redirect("/")
    if request.method == "GET":
        return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/import", methods=["GET", "POST"])
@login_required
def import_page():
    return render_template("import.html")

@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    return render_template("wishlist.html")

@app.route("/books", methods=["GET", "POST"])
@login_required
def books():
    return render_template("books.html")