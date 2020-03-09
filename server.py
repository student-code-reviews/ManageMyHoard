"""Main Serverr for MHH page/app
"""


from flask import Flask, redirect, request, render_template, jsonify, session
#from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

app = Flask(__name__)


# This option will cause Jinja to throw UndefinedErrors if a value hasn't
# been defined (so it more closely mimics Python's behavior)
app.jinja_env.undefined = StrictUndefined

# This option will cause Jinja to automatically reload templates if they've been
# changed. This is a resource-intensive operation though, so it should only be
# set while debugging.
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
#app.secret_key = 'ABC'




@app.route('/')
def index():
    """Show our index page."""

    return render_template("index.html")

@app.route('/index')
def index2():
    """Show our index page."""

    return render_template("index.html")


@app.route("/login", methods=["GET"])
def show_login():
    """Bring the User to the login webpage."""

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")