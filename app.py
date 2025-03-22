from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,current_user,mixins
from config import Config
from models import db, User, Train
from admin import init_admin
from registrationandauth import init_auth
from flask import Flask, render_template, redirect, url_for , request , abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

init_admin(app)
init_auth(app)

@app.route("/accountlogout")
def accountlogout():
    return render_template("index.html")

@app.route("/")
def index():
    if(User.is_authenticated):
        return render_template("Home.html")
    else:
        return render_template("Home.html")

@app.route("/home")
def home():
    return render_template("Home.html")

@app.route("/about")
def about():
    return render_template('contact.html')

@app.route("/registration")
def registration():
    
    if  current_user.is_authenticated:
        user = current_user
        print(user.id)
        trainer = Train.query.filter_by(loggedby=user.id).all()
        return render_template('registration.html', trainer=trainer)
    return redirect(url_for("login"))

@app.route("/delete/<int:reg_id>")
def delete_train(reg_id):
    reg = Train.query.get(reg_id)
    if reg:
        db.session.delete(reg)
        db.session.commit()
    return redirect(url_for("registration"))


@app.route("/change/<int:reg_id>", methods=["GET", "POST"]
)
def change_train(reg_id):
    reg = Train.query.get(reg_id)
    if not reg:
        return abort(404)
    if request.method == "POST":
        trainer = request.form.get("trainer").strip()
        place = request.form.get("place").strip()
        price = request.form.get("price").strip()
        if not all((trainer, place, price)):
            return abort(400)
        reg.trainer = trainer
        reg.place = place
        reg.price = price
        db.session.commit()
        return redirect(url_for("registration"))
    return render_template("change.html", reg=reg)


@app.route("/add", methods=["GET", "POST"]
)
def add_train():
    if request.method == "POST":
        trainer = request.form.get("trainer").strip()
        place = request.form.get("place").strip()
        price = request.form.get("price").strip()
        if not all((trainer, place, price)):
            return abort(400)
        reg = Train(place=place, price=price, trainer=trainer, loggedby=current_user.id)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for("registration"))
    return render_template("base.html") 


if __name__ == "__main__":
  
    app.run(debug=True)

