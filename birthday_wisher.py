from flask import Flask, redirect, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from datetime import datetime


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
    img_url = StringField("Enter Image Url", validators=[DataRequired()])
    submit = SubmitField("Submit")


db.create_all()


@app.route("/", methods=["POST", "GET"])
def main():
    now = datetime.now()
    today = now.strftime("%d-%m")
    print(today)
    users = User.query.all()
    for user in users:
        date = user.date[:5]
        if date == today:
            id = user.id
    try:
        birthday = User.query.get(id)
    except UnboundLocalError:
        return redirect(url_for("add"))
    return render_template("index.html", user=birthday)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = Forms()
    if request.method == "POST":
        name = form.name.data
        user = User(
            name=form.name.data, date=form.birthday.data, img_url=form.img_url.data
        )
        print(name)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main"))
    return render_template("add_user.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
