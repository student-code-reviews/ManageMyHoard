"""Main Serverr for MHH page/app
"""


from flask import Flask, redirect, request, flash, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import connect_to_db, db, User, Project, Inventory

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar

app.secret_key = "ProtectTheHoard"

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

    # check to see if user is logged in
    # user_id = session['user_id']

    # if user_id is None:
    #     return render_template('index.html')

    # else:
    #     return redirect(f'/user/{user_id}')

    # if not display the index page

    # if there is a user_id in session
    # display the user profile page?

    return render_template('index.html')

@app.route('/index')
def index2():
    """Show our index page."""
    user_id = session['user_id']
    # check to see if user is logged in


    # if not display the index page

    # if there is a user_id in session
    # display the user profile page?
    return render_template('index.html')

@app.route('/login_form')
def login_form():
    """Bring the User to the login webpage."""

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login():

    #check to see if user_id is in session


    """Validate email and password and update session."""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    

    user = User.query.filter_by(email=request.form.get('email')).first()

    if user.login(request.form.get('password')):
        app.logger.info('Login successful ...')
        session['user_id'] = user.user_id
        flash('Login successful.')
        return redirect(f'/user/{ user.user_id }')
    else:
        app.logger.info('Login failed!')
        return redirect('/login_form')

    


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["user_id"]
    flash("Logged out.")
    return redirect("/")


@app.route("/register")
def register():
    """Display the form for user to fill out and register for an account."""
    return render_template('register.html')


@app.route("/new_user", methods=['POST'])
def new_user():
    """Take the information from the register form and insert this User into 
    the database"""
    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname= request.form["lname"]
    username = request.form["username"]

    new_user = User(username=username,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname)

    
    #hashing password before storing it
    new_user.create_hashedpw(password)

    new_user.save()

    # db.session.add(new_user)
    # db.session.commit()

    flash(f"User {email} added.")
    return redirect("/")


@app.route('/user/<user_id>')
def user_info(user_id):
    """Display user info."""
  
    user = User.query.get(user_id)

    return render_template('user_profile.html', user=user)


@app.route('/user')
def user():
    """ NOTE TO SELF - do I NEED two routes???"""
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)

        return redirect(f'/user/{user_id}')
    else:
        return redirect('/login')


@app.route('/add_inv', methods=['POST'])
def create_inv():
    """ Display the form for the user to enter the required info for an 
    inventory item """

    # get the user info saved in session
    user_id = session.get('user_id')

    #get the info from the form
    inv_name = request.form['inv_name']
    inv_type = request.form['inv_type']
    description = request.form['description']
    price = request.form['price']
    count_per_package = request.form['count_per_package']
    manufacturer = request.form['manufacturer']['user_id']
    size = request.form['size']

    # Not using picture path yet - just initializing it as a blank
    picture_path=""
    # do we need to process keywords into a python list?
    keywords = request.form['keywords']

    
    #create the inv item
    # if the form fields align with the model fields you can do this ...
    new_inv = Inventory(**request.form)

    #add to session & commit
    # db.session.add(new_inv)
    # db.session.commit()
    new_inv.save()

    flash(f"Inventory Item: {inv_name} added.")

    return redirect('/inventory')


@app.route('/add_inv_form')
def add_inv_form():
    """ Add a new inventory item """
    return render_template('inv_form.html')

@app.route('/inventory/<int:inv_id>')
def get_inv_item(inv_id):
    """View an individual inv_item"""

    # get the user info saved in session
    user_id = session['user_id']

    #the inv_id was passed in with the route path
    # we can use it to query the db and get an individual inventory
    # item from the inventory table.
    inv_item = Inventory.query.get(inv_id)
    
    #return that info to be displayed on the view_inv_item.html page

    return render_template("view_inv_item.html", inv_item=inv_item)

@app.route('/inventory')
def view_inventory():
    """ View all the inventory for a particular user"""

    user_id = session['user_id']
    user = User.query.get(user_id)

    inventory = user.inventory
    #get the tools for this user in the inventory table
    # utools_query = db.session.query(inventory).filter_by(inv_type='t').all()
    # usupplies_query = db.session.query(inventory).filter_by(inv_type='s').all()

    
    return render_template('inventory.html', user=user, inventory=inventory)

@app.route('/projects/new')
def add_proj_form():
    return render_template('proj_form.html')


@app.route('/projects', methods=['POST'])
def add_project():
    """ Add a new project """
    user_id = session['user_id']
    name = request.form['proj_name']
    status = request.form['status']
    description = request.form['description']
    picture_path = ""
    keywords = request.form['keywords']
    tool_list = request.form['tool_list']
    supply_list = request.form['supply_list']
    directions = request.form['directions']
    URL_link = request.form['URL_link']

    app.logger.info("getting project data from form")
    new_proj = Project(user_id=user_id,
                       status=status,
                       name=name,
                       description=description,
                       picture_path=picture_path,
                       keywords=keywords,
                       tool_list=tool_list,
                       supply_list=supply_list,
                       directions=directions,
                       URL_link=URL_link)

    #add to session & commit
    # db.session.add(new_proj)
    # db.session.commit()
    new_proj.save()

    flash(f"Project: {name} added.")

    return redirect('/projects')


@app.route('/projects')
def view_projects():
    user_id = session['user_id']
    user = User.query.get(user_id)
    projects = user.projects
    
    """ Show all the projects for a particular user"""
    return render_template('projects.html', user=user)

@app.route('/projects/<int:project_id>')
def get_proj_item(project_id):
    """View an individual inv_item"""

    # get the user info saved in session
    user_id = session['user_id']

    #the inv_id was passed in with the route path
    # we can use it to query the db and get an individual inventory
    # item from the inventory table.
    proj_item = Project.query.get(project_id)
    
    #return that info to be displayed on the view_inv_item.html page

    return render_template("view_proj_item.html", proj_item=proj_item)

@app.route('/search')
def search():
    """ Search for specific tools/supplies, and View all of the tools 
    and supplies saved in the database- for the user that is logged in """
    return render_template('search.html')

# @app.route('/user')
# def user_profile():
#     """ Show the profile information of the person logged in"""
#     return render_template('user_profile.html')



if __name__ == "__main__":

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, port=5000, host="0.0.0.0")
