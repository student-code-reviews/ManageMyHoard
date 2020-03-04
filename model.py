
"""Models and database functions for MMH Hackbright project."""

from flask_sqlalchemy import SQLAlchemy

import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable = False)
    

    def __repr__(self):
        return f"""<User user_id={self.user_id}
                   email={self.email}
                   password={self.password}
                   fname={self.name}
                   lname={self.name}>"""




class Inventory(db.Model):
    """Items - each item is a Movie with relevant information"""
    __tablename__ = "inventory"

    inv_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inv_type = db.Column(db.Char(1), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float(), nullable=True)
    count_per_package = db.Column(db.Integer, nullable=True)
    size = db.Column(db.Integer, nullable = True)
    picture_path = db.Column(db.String(100), nullable=True)
    keywords = db.Column(db.String(500), nullable=True)

    
    

    def __repr__(self):
        return f"""<Inv inv_id={self.movie_id}
                    name{self.name}
                    inv_type{self.inv_type}
                    description{self.description}
                    price{self.price}
                    count_per_package{self.count_per_package}
                    size{self.size}
                    picture_path{self.picture_path}
                    keywords{self.keywords}
                    >"""


class Project(db.Model):
    """ Table containing a rating a particular user has given to a specific
    movie
    """
    __tablename__ = "projects"

    project_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    name = db.Column(db.String(50) nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    
    # Store the Path to the picture
    picture_path = db.Column(db.String(100), nullable=True)
    keywords = db.Column(db.String(500), nullable=True)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("users",
                                              order_by=user_id))
    

    def __repr__(self):
        return f"""<Project project_id={self.project_id}
                   user_id={self.user_id}
                   name={self.name}
                   description={self.description}
                   picture_path={self.picture_path}
                   keywords={self.keywords}>"""
#     # is Timestamp necessary to the  objective - is it okay if it's null?
#     # i.e. nullable could be False
#     time_stamp = db.Column(db.DateTime, nullable=True)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ManageMyHoard'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

