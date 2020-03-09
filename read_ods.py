from pandas_ods_reader import read_ods
from model import Inventory

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
                                "keywords"])

print(len(df))
i = 1
while i < len(df):
    #print(df.loc[i])
    #print(df.loc[i].inv_type)
    inventory_item = Inventory(inv_id=df.loc[i].inv_id,
                               user_id=df.loc[i].user_id,
                               name=df.loc[i].name,
                               inv_type=df.loc[i].inv_type,
                               description=df.loc[i].description,
                               manufacturer=df.loc[i].manufacturer,
                               price=df.loc[i].price,
                               count_per_package=df.loc[i].count_per_package,
                               size=df.loc[i].size,
                               picture_path=df.loc[i].picture_path,
                               keywords=df.loc[i].keywords
                               )
    i = i + 1


