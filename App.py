import flask
from database import Base, engine
import models

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template("index.html")

def init_db():
    # Create tables if they do not exist
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


