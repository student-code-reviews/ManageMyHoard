from pandas_ods_reader import read_ods

path = "inventory.ods"

# load a sheet based on its index (1 based)
sheet_idx = 1
df = read_ods(path, sheet_idx)

# load a sheet based on its name
sheet_name = "sheet1"
df = read_ods(path, sheet_name)

# load a file that does not contain a header row
# if no columns are provided, they will be numbered
df = read_ods(path, 1, headers=False)

# load a file and provide custom column names
# if headers is True (the default), the header row will be overwritten
df = read_ods(path, 1, columns=["user_id", "inv_id", "name", "inv_type", "description", "manufacturer", "price", "count_per_package", "size", "keywords" ])