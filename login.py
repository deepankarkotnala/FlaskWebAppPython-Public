from flask import Flask, flash, redirect, url_for, render_template, request, session, abort
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

#app.secret_key = os.urandom(12)
#app.secret_key = os.environ.get('SECRET')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.urandom(12)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/home")
def home():
    if not session.get("logged_in"):
        return render_template("login.html", title="Login")
    else:
        return render_template("index.html", title="Home")

@app.route("/login", methods=["POST"])
def do_admin_login():
    user = User.query.filter_by(username=request.form["username"]).first()
    if user:
        login_user(user)
        print("Username===================", user.username)
        print("Email======================", user.email)
        print("Password===================", user.password)
        if request.form["password"] == user.password and request.form["username"] == user.username:
            session["logged_in"] = True
            print("===================== Username and password verified from Database. Logged in!!")
            #flash('Logged In!', 'success')
            return render_template("index.html", title ="Home")
    else:
        error = 'Invalid credentials'
        flash('Invalid credentials!', 'danger')
        return render_template("login.html", title="Login", error=error)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    #return render_template("login.html", title="Login")
    return redirect(url_for('home'))
    
@app.route("/blog_cards")
def blog_card_fn():
    return render_template("blog_cards.html", title="Blog")
    
@app.route("/signup")
def signup():
    return render_template("signup.html", title="Signup")

# We can refer to this about() function in the template.html file by using 
# href="{{ url_for('about') }}"

# or we can directly use href="/about" for referring to the app route
@app.route("/about")
def about():
  return render_template("aboutus.html", title="The Team")


if __name__ == "__main__":
    #app.secret_key = os.environ.get("SECRET")
    app.run(debug=True)