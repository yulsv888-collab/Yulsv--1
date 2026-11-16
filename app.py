import os
from dotenv import load_dotenv

from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from forms import ContactoForm

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///proyecto.db"

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)


class Contacto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template(
        "about.html",
        proyecto="Mi primera app Flask"
    )


@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    form = ContactoForm()

    if form.validate_on_submit():

        nuevo_contacto = Contacto(
            nombre=form.nombre.data,
            correo=form.correo.data
        )

        db.session.add(nuevo_contacto)
        db.session.commit()

        flash(
            f"¡Gracias, {form.nombre.data}! Recibimos tus datos.",
            "success"
        )

        return redirect(url_for("contacto"))

    return render_template(
        "contacto.html",
        form=form
    )


@app.route("/contactos")
def contactos():

    lista_contactos = Contacto.query.all()

    return render_template(
        "contactos.html",
        contactos=lista_contactos
    )


if __name__ == "__main__":
    app.run(debug=True)