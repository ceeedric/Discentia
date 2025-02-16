from urllib.parse import urlencode, quote_plus

import flask
from authlib.integrations.flask_client import OAuth
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask import url_for, session, redirect

from database import Base, engine
import models


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

@app.route("/dashboard")
def dashboard():
    if session["user"] is None:
        return redirect(url_for("login"))
    return flask.render_template("dashboard.html")

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
