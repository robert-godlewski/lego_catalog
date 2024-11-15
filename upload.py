import sqlite3
import numpy # type: ignore
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
filename += ".csv"

group_prompt = "What is the group called that we are specifically uploading to (leave blank if there is not a specific group)? "
group_name = input(group_prompt)
cur.execute("INSERT OR IGNORE INTO lego_group (name) VALUES ( ? )", (group_name, ))
cur.execute("SELECT * FROM lego_group WHERE name = ? ", (group_name, ))
group_data = cur.fetchone()
group = {
    "id": group_data[0],
    "name": group_data[1]
}
print(group)

try:
    data = pd.read_csv(filename, header=0).values
    print(type(data))
    print(data)
    print(f"Shape of data = {data.shape}")
    print(f"Number of data points in the data = {data.shape[0]}")
    # Need to go through each piece of data and add it to the database
except:
    print("There is nothing to upload here.")

con.commit()
con.close()
