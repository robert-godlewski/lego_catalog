import sqlite3
import numpy as np # type: ignore
import pandas as pd # type: ignore


# Creating a sqlite database
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
# Creating our tables - need to add in all of the others - Might be able to make a function or make a separate script for this.
# For lego_group
try:
    cur.execute("SELECT * FROM lego_group")
    print("lego_group already exists.")
except sqlite3.OperationalError:
    msg = ""
    try:
        print("Creating a lego_group table...")
        cur.execute("""CREATE TABLE IF NOT EXISTS lego_group (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT UNIQUE
        )""")
        msg += "Successfully created "
    except:
        msg += "Failed to create "
    msg += "new lego_group table."
    print(msg)

# For lego_theme - Need to fix this
# try:
#     cur.execute("SELECT * FROM lego_theme")
#     print("lego_theme already exists.")
# except sqlite3.OperationalError:
#     msg = ""
#     try:
#         print("Creating a lego_theme table...")
#         cur.execute("""CREATE TABLE IF NOT EXISTS lego_theme (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     name TEXT UNIQUE,
#                     group_id FOREIGN KEY REFERENCES lego_group ON DELETE CASCADE
#         )""")
#         msg += "Successfully created "
#     except:
#         msg += "Failed to create "
#     msg += "new lego_theme table."
#     print(msg)

# Getting the file name to upload
filename = input("What is the name of the csv file (without adding in csv at the end)? ")
# Mainly for testing
if len(filename) < 1:
    filename = "MyLegoSets - Tolkien"
filename += ".csv"

# Saving and creating lego_group data as a hash
def _getLegoGroup(name: str) -> dict:
    cur.execute("INSERT OR IGNORE INTO lego_group (name) VALUES ( ? )", (name,))
    cur.execute("SELECT * FROM lego_group WHERE name = ? ", (name,))
    group_data = cur.fetchone()
    return {
        "id": group_data[0],
        "name": group_data[1]
    }

# Mining the data
try:
    data_raw = pd.read_csv(filename).values
    print(f"Shape of data = {data_raw.shape}")
    print(f"Number of data points in the data = {data_raw.shape[0]}")
    # Header - Need to find something that actually takes the header info out
    header = data_raw[0]
    print(header)
    group = {}
    group_name = ""
    has_group = False
    # Might need to get more sections to add in later for Theme and Series
    theme = {}
    series = {}
    #....More variables here if needed....
    data = np.delete(data_raw, 0, 0)
    # print(type(data))
    # print(data)
    # Need to go through each piece of data and add it to the database
    for row in range(len(data)-1):
        print(f"row {row} = {data[row]}")
        if len(header) < 11:
            if not has_group:
                # We need to actually define the group since it's not with the data
                group_prompt = "What is the group called that we are specifically uploading to (leave blank if there is not a specific group)? "
                group_name = input(group_prompt)
                has_group = True
            # check for others here
        else:
            group_name = data[row][0]
            # theme_name = data[row][1]
            # series_name = data[row][2]
        print(group_name)
        if "id" not in group:
            group = _getLegoGroup(group_name)
        print(f"Lego Group = {group}")
        # Need the theme, series, kit, and parts here
except:
    print("There is nothing to upload here.")

con.commit()
con.close()
