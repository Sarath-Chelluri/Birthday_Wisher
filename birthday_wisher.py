from datetime import datetime
import os
import secrets
from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
db = SQLAlchemy(app)
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///birthday.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "lol"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(120), nullable=False)
    img_url = db.Column(db.String(200), unique=True, nullable=False)


class Forms(FlaskForm):
    name = StringField("Enter Name", validators=[DataRequired()])
    birthday = StringField(
        "Enter Birthday",
        validators=[DataRequired()],
    )
    img_url = FileField("Add Image", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("Submit")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    form_picture.save(picture_path)

    return picture_fn


db.create_all()


@app.route("/", methods=["POST", "GET"])
def main():
    now = datetime.now()
    today = now.strftime("%d-%m")
    users = User.query.all()
    for user in users:
        date = user.date[:5]
        if date == today:
            id = user.id
    try:
        birthday = User.query.get(id)
        print(user.img_url)

    except UnboundLocalError:
        return redirect(url_for("add"))

    return render_template("index.html", user=birthday)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = Forms()
    if request.method == "POST":
        picture_file = save_picture(form.img_url.data)
        print(picture_file)
        user = User(name=form.name.data, date=form.birthday.data, img_url=picture_file)
        db.session.add(user)
        user.img_url = url_for("static", filename="profile_pics/" + user.img_url)
        db.session.commit()

        return redirect(url_for("main"))

    elif request.method == "GET":
        now = datetime.now()
        today = now.strftime("%d-%m-%Y")
        form.name.data = "John Doe"
        form.birthday.data = today

        return render_template("add_user.html", form=form)

    return render_template("add_user.html", form=form)


if __name__ == "__main__":
    app.run()
