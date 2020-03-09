from faker import Faker
from sqlalchemy import func
from model import User
from model import Inventory
from model import Project
from model import connect_to_db, db
from server import app
from pandas_ods_reader import read_ods

faker = Faker()



def load_users(amount_to_generate):
    """ Use this function to generate users (integer representing the number
    of users is passed in to the function).  All of the data associated with a 
    user will be generated and inserted into the Users table.
    """
    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    i =0
    user_id = 0
    for i in range(amount_to_generate):
        # Generate fake User information.
        faker = Faker()
        user_id = user_id + 1
        print(f'user_id: {user_id}')
        fname = faker.first_name()
        print(f'fname: {fname}')
        lname = faker.last_name()
        print(f'last_name: {lname}')
        email = faker.email()
        print(f'email: {email}')
        password = faker.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
        print(f'passw: {password}')

        username = fname[0] + lname
        print(f'username: {username}')

        # insert generated User into ManageMyHoard db
        user = User(user_id=user_id,
                    username=username,
                    fname=fname,
                    lname=lname,
                    email=email,
                    password=password)
        i += 1
   
   

        # Add the User object to the session so it will be stored.
        db.session.add(user)

    # Once we're done inserting all the users, commit the changes to the 
    # database
    db.session.commit()

def load_inventory():
    """method to open the inventory ods spreadsheet and create inventory
    objects from each row
    """
    path = "inventory.ods"

    # load a sheet based on its index (1 based)
    sheet_idx = 1
    df = read_ods(path, sheet_idx)

    # load a sheet based on its name
    sheet_name = "Sheet1"
    df = read_ods(path, sheet_name)

    # load a file that does not contain a header row
    # if no columns are provided, they will be numbered
    df = read_ods(path, 1, headers=False)

    # load a file and provide custom column names
    # if headers is True (the default), the header row will be overwritten
    df = read_ods(path, 1, columns=["user_id", "inv_id", "name", "inv_type",
                                    "description", "manufacturer", "price",
                                    "count_per_package", "size", "picture_path",
                                    "keywords" ])

    print(len(df))
    i = 1
    while i < len(df):
        print(df.loc[i])
        #print(df.loc[i].inv_type)
        
        inventory_item = Inventory(inv_id=df.loc[i].inv_id,
                                   user_id=int(df.loc[i].user_id),
                                   name=df.loc[i].name,
                                   inv_type=df.loc[i].inv_type,
                                   description=df.loc[i].description,
                                   price=df.loc[i].price,
                                   count_per_package=df.loc[i].count_per_package,
                                   manufacturer=df.loc[i].manufacturer,
                                   size=df.loc[i].size,
                                   picture_path=df.loc[i].picture_path,
                                   keywords=df.loc[i].keywords)
        i += 1
        #print(inventory_item)
        # Add the User object to the session so it will be stored.
        db.session.add(inventory_item)
        
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
    num_to_gen = 3
    load_users(num_to_gen)
    load_inventory()
    
    set_val_user_id()
