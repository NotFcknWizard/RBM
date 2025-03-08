from flask import Flask, render_template, redirect, url_for , request , abort
from flask_sqlalchemy import SQLAlchemy
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)



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
    return render_template("index.html", reg=reg)


@app.route("/add", methods=["GET", "POST"]
)
def add_train():
    if request.method == "POST":
        trainer = request.form.get("trainer").strip()
        place = request.form.get("place").strip()
        price = request.form.get("price").strip()
        if not all((trainer, place, price)):
            return abort(400)
        reg = Train(place=place, price=price, trainer=trainer)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for("registration"))
    return render_template("base.html")






@app.route("/")
def index():
    return render_template('Home.html')




@app.route("/about")
def about():
    return render_template('contact.html')

@app.route("/registration")
def registration():
    trainer = Train.query.all()
    return render_template('registration.html', trainer=trainer)


#newdb

db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trainer = db.Column(db.String(300) ,nullable = False)
    place = db.Column(db.Text,nullable = False)
    price = db.Column(db.Integer , nullable = False)




db.init_app(app)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)


