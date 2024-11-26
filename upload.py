import sqlite3
import numpy as np # type: ignore
import pandas as pd # type: ignore


# Creating a sqlite database
con = sqlite3.connect("db.sqlite3")
cur = con.cursor()
db_error = False

# Saving and creating lego_group data as a hash
def _getLegoGroup(name: str) -> dict:
    cur.execute("INSERT OR IGNORE INTO lego_group (name) VALUES ( ? )", (name,))
    cur.execute("SELECT * FROM lego_group WHERE name = ? ", (name,))
    group_data = cur.fetchone()
    return {
        "id": group_data[0],
        "name": group_data[1]
    }

# Saving and creating lego_theme data as a hash
def _getLegoTheme(name: str, group_id: int) -> dict:
    cur.execute("INSERT OR IGNORE INTO lego_theme (name, group_id) VALUES ( ?, ? )", (name, group_id,))
    cur.execute("SELECT * FROM lego_theme WHERE name = ? ", (name,))
    theme_data = cur.fetchone()
    return {
        "id": theme_data[0],
        "name": theme_data[1]
    }

try:
    cur.execute("SELECT * FROM lego_group")
    print("lego_group already exists.")
except sqlite3.OperationalError:
    print("Please run: python create_db.py")
    print("Unable to run the program.")
    db_error = True

if not db_error:
    # Getting the file name to upload
    filename = input("What is the name of the csv file (without adding in csv at the end)? ")
    # Mainly for testing
    if len(filename) < 1:
        filename = "MyLegoSets - Tolkien"
    filename += ".csv"

    # Mining the data
    try:
        data_raw = pd.read_csv(filename).values
        print(f"Shape of data = {data_raw.shape}")
        print(f"Number of data points in the data = {data_raw.shape[0]}")
        # Header - Need to find something that actually takes the header info out
        header = data_raw[0]
        print(header)
        # The next variable is used to for UI prompting
        prompt_base = " called that we are specifically uploading to? "
        group = {}
        group_name = ""
        # Determines if the group is the same throughout the data upload or not
        has_same_group = False
        theme = {}
        theme_name = ""
        # Determines if the theme is the same throughout the data upload or not
        has_same_theme = False
        # Might need to get more sections to add in later for Theme and Series
        series = {}
        #....More variables here if needed....
        data = np.delete(data_raw, 0, 0)
        # print(type(data))
        # print(data)
        # Need to go through each piece of data and add it to the database
        for row in range(len(data)-1):
            print(f"row {row} = {data[row]}")
            if len(header) < 11:
                if not has_same_group:
                    # We need to actually define the group since it's not with the data
                    group_prompt = "What is the group" + prompt_base
                    group_name = input(group_prompt)
                    has_same_group = True
                if len(header) < 10:
                    if not has_same_theme:
                        # We need to actually define the theme since it's not with the data
                        theme_prompt = "What is the theme" + prompt_base
                        theme_name = input(theme_prompt)
                        has_same_theme = True
                else:
                    theme_name = data[row][0]
                    # series_name = data[row][1]
                    # check for others here
            else:
                group_name = data[row][0]
                theme_name = data[row][1]
                # series_name = data[row][2]
            # print(group_name)
            if "id" not in group:
                group = _getLegoGroup(group_name)
            print(theme_name)
            if "id" not in theme:
                theme = _getLegoTheme(theme_name, group["id"])
            print(f"Lego Group = {group}")
            print(f"Lego Theme = {theme}")
            # Need the series, kit, and parts here
            # Clearing variables that change
            if not has_same_group:
                group = {}
            if not has_same_theme:
                theme = {}
    except:
        print("There is nothing to upload here.")
else:
    print("db not working!")

con.commit()
con.close()
