from urllib.parse import urlencode, quote_plus

import flask
from authlib.integrations.flask_client import OAuth
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import url_for, session, redirect, flash
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import exists

import database
from database import Base, engine
from forms import AddStudentForm
from models import Student, Teacher

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = flask.Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route('/')
def index():
    return flask.render_template("index.html")

def init_db():
    # Create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("dashboard"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if session["user"] is None:
        return redirect(url_for("login"))

    email = session["user"]["userinfo"]['email']

    with Session(database.engine) as db_session:
        teacher = db_session.execute(select(Teacher).filter_by(email=email)).first()

        if not teacher is None:
            form = AddStudentForm()
            if form.validate_on_submit():
                flash("test message")
                return add_student()
            return flask.render_template("dashboard-teacher.html", teacher=teacher, form=form)

        student = db_session.execute(select(Student).filter_by(email=email)).first()
        if not student is None:
            return flask.render_template("dashboard-student.html", student=student)

    return redirect("/")

def add_student():
    with Session(database.engine) as db_session:
        form = AddStudentForm()
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data

            if db_session.execute(select(Student).where(Student.email == email)): # check if that email already exists
                return "already exists"

            teacher_email = session["user"]["userinfo"]['email']
            teacher = db_session.execute(select(Teacher).filter_by(email=teacher_email)).first()

            if teacher.Teacher is None:
                return "failed"

            newStudent = Student(name=name, email=email, teacher_id=teacher.Teacher.id)
            db_session.add(newStudent)
            db_session.commit()

            print("committed")
            return "test"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
