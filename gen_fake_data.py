from faker import Faker
from sqlalchemy import func
from model import User
from model import Inventory
from model import Project
from model import connect_to_db, db
from server import app
from pandas_ods_reader import read_ods
import csv
import random
import pdb

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

    # # load a sheet based on its index (1 based)
    # sheet_idx = 1
    # df = read_ods(path, sheet_idx)

    # # load a sheet based on its name
    # sheet_name = "Sheet1"
    # df = read_ods(path, sheet_name)

    # # load a file that does not contain a header row
    # # if no columns are provided, they will be numbered
    # df = read_ods(path, 1, headers=False)

    # load a file and provide custom column names
    # if headers is True (the default), the header row will be overwritten
    df = read_ods(path, 1, columns=["user_id", "inv_id", "inv_name", "inv_type",
                                    "description", "manufacturer", "price",
                                    "count_per_package", "size", "picture_path",
                                    "keywords" ])

    #print(len(df))
    i = 1
    while i < len(df):
        
        
        pdb.set_trace()
        inventory_item = Inventory(inv_id=df.loc[i].inv_id,
                                   user_id=int(df.loc[i].user_id),
                                   inv_name=df.loc[i].inv_name,
                                   inv_type=df.loc[i].inv_type,
                                   description=df.loc[i].description,
                                   price=df.loc[i].price,
                                   count_per_package=df.loc[i].count_per_package,
                                   manufacturer=df.loc[i].manufacturer,
                                   size=df.loc[i].size,
                                   picture_path=df.loc[i].picture_path,
                                   keywords=df.loc[i].keywords)
        i += 1
        print(inventory_item)
        # Add the User object to the session so it will be stored.
        db.session.add(inventory_item)
        
    db.session.commit()




def load_projects():
    """function to seed database with projects"""
    # user Faker Module to generate some fake fields
    faker = Faker()

    names = ['hat','cowl', 'scarf', 'sweater', 'amigurumi dragon', "mittens"]


    seed_tools = ["16\" circular needles", " 6mm crochet hook" "4 mm dpns",
             "yarn needle", "scissors", "stitch markers"]
    seed_supplies = ["150 yds super chunky yarn", "500 yds sockweight yarn",
                "5 oz worsted weight yarn", "800 m of lace weight yarn"]
    seed_URLS = ["http://www.example.com/","http://www.example.com/army/bead",
            "http://www.example.org/",
            "http://www.funkychickenknits.com/chickensweater",
            "http://example.com/",
            "https://agreement.example.com/",
            "https://alarm.example.com/#bottle",
            "https://wwww.knittinkitten/pawsitivelyperfectscarf"]

    project_id = 0
    # number of fake projects to create
    num_projects = 4
    num_users = 3

    for i in range(num_users):
        user_id = i + 1
        
        # # create the set # of projects for each user
        for j in range(num_projects):
            print("user_id",user_id)

            project_id += 1
            print("project_id",project_id)

            name = random.choice(names)
            print("name=",name)

            description = faker.text()
            print("description=", description)

            picture_path = ""

            seed_keywords1 = ["knit", "crochet"]
            seed_keywords2 = ["worked_flat", "in-the-round"]
            seed_keywords3 = ["unisex," "women" "men"]

            keywords=[]
            keywords.append(random.choice(seed_keywords1))
            keywords.append(random.choice(seed_keywords2))
            keywords.append(random.choice(seed_keywords3))

            print("keywords=",keywords)

            tool_list = []
            num_tools = random.randrange(1,4)
            
            for k in range(num_tools):
                # get a random choice from the seed tools list and append it to our
                # list of tools for this fake project
                tool_to_add = random.choice(seed_tools)
                tool_list.append(tool_to_add)
                k += 1
            print("tools=",tool_list)

            num_supplies = random.randrange(1,3)
            supply_list = []

            for s in range(num_supplies):
                # get a random choice from the seed supplies list and append it to 
                # our list of supplies for this fake project
                
                supply_list.append(random.choice(seed_supplies))
                s += 1
            print("supply_list=",supply_list)

            desc_length = random.randrange(1,10)
            # make a varying length text block for directions
            directions = ""
            for d in range(desc_length):
                directions = directions + faker.text()
            print("directions=",directions)

            URL_link = random.choice(seed_URLS)
            print("URL=",URL_link)
            j +=1

            #create the project object

            project = Project(project_id=project_id,
                              user_id=user_id,
                              name=name,
                              description=description,
                              picture_path=picture_path,
                              keywords=keywords,
                              tool_list=tool_list,
                              supply_list=supply_list,
                              directions=directions,
                              URL_link=URL_link)

            # add the project item to the db session
            db.session.add(project)

        i += 1
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
    load_projects()
    
    set_val_user_id()
