import sqlite3
import numpy as np # type: ignore
import pandas as pd # type: ignore


# Creating a sqlite database
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
# Creating our tables - need to add in all of the others
try:
    cur.execute("SELECT * FROM lego_group")
    print("lego_group already exists.")
except sqlite3.OperationalError:
    try:
        print("Creating a group table:")
        cur.execute("""CREATE TABLE IF NOT EXISTS lego_group (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name TEXT UNIQUE
        )""")
        print("New Table created successfully")
    except:
        print("Create new table failed")

filename = input("What is the name of the csv file (without adding in csv at the end)? ")
# Mainly for testing
if len(filename) < 1:
    filename = "MyLegoSets - Tolkien"
filename += ".csv"

try:
    data_raw = pd.read_csv(filename).values
    print(f"Shape of data = {data_raw.shape}")
    print(f"Number of data points in the data = {data_raw.shape[0]}")
    # Header - Need to find something that actually takes the header info out
    header = data_raw[0]
    print(header)
    group = {} # Maybe make a function to get this since it looks pretty repetitive
    # Might need to get more sections to add in later for Theme and Series
    theme = {}
    series = {}
    if len(header) < 11:
        group_prompt = "What is the group called that we are specifically uploading to (leave blank if there is not a specific group)? "
        group_name = input(group_prompt)
        # ***Repeat start***
        cur.execute("INSERT OR IGNORE INTO lego_group (name) VALUES ( ? )", (group_name, ))
        cur.execute("SELECT * FROM lego_group WHERE name = ? ", (group_name, ))
        group_data = cur.fetchone()
        group = {
            "id": group_data[0],
            "name": group_data[1]
        }
        # ***Repeat end****
    data = np.delete(data_raw, 0, 0)
    # print(type(data))
    # print(data)
    # Need to go through each piece of data and add it to the database
    for row in range(len(data)-1):
        print(f"row {row} = {data[row]}")
        if "id" not in group:
            group_name = data[row][0]
            print(group_name)
            # ***Repeat start***
            cur.execute("INSERT OR IGNORE INTO lego_group (name) VALUES ( ? )", (group_name, ))
            cur.execute("SELECT * FROM lego_group WHERE name = ? ", (group_name, ))
            group_data = cur.fetchone()
            group = {
                "id": group_data[0],
                "name": group_data[1]
            }
            # ***Repeat end****
        print(f"Lego Group = {group}")
        # Need the theme, series, kit, and parts here
except:
    print("There is nothing to upload here.")

con.commit()
con.close()
