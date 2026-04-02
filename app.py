from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)

app.secret_key = "change-this-to-something-random-in-production"

USERS_FILE = "users.txt"


def load_users() -> dict:
    
    users = {}
    if not os.path.exists(USERS_FILE):
        return users                        
    with open(USERS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if ":" in line:                
                username, password = line.split(":", 1)
                users[username] = password
    return users


def save_user(username: str, password: str) -> None:

    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{password}\n")



@app.route("/")
def index():
    
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

      
        if not username or not password:
            flash("Please fill in both fields.", "error")
            return render_template("login.html")

        users = load_users()

        
        if username not in users:
            flash("Username not found. Please register first.", "error")
        elif users[username] != password:
            flash("Incorrect password. Please try again.", "error")
        else:
            flash(f"Welcome back, {username}! You are now logged in.", "success")
            
            return render_template("login.html", logged_in=True, username=username)

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        # ── validation ──
        if not username or not password or not confirm:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return render_template("register.html")

        if len(password) < 4:
            flash("Password must be at least 4 characters.", "error")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        users = load_users()

        if username in users:
            flash(f'Username "{username}" is already taken. Choose another.', "error")
            return render_template("register.html")

        
        save_user(username, password)
        flash(f'Account created for "{username}"! You can now log in.', "success")
        return redirect(url_for("login"))

    return render_template("register.html")



if __name__ == "__main__":
    
    app.run(debug=True)