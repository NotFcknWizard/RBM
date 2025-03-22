from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from models import db, User

def init_auth(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                login_user(user)
                flash("Успішний вхід!", "success")
                return redirect(url_for("home"))
            flash("Невірне ім'я користувача або пароль.", "danger")
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Цей логін вже зайнятий. Виберіть інший.", "danger")
                return redirect(url_for("register"))
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Реєстрація успішна! Тепер увійдіть.", "success")
            login_user(user)
            return redirect(url_for("home"))
        return render_template("register.html")

    @app.route("/logout")
    def logout():
        logout_user()
        flash("Ви вийшли з системи.", "success")
        return redirect(url_for("index"))
