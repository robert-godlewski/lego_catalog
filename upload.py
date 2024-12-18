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

# Saving and creating lego_series data as a hash
def _getLegoSeries(name: str, theme_id: int) -> dict:
    cur.execute("INSERT OR IGNORE INTO lego_series (name, theme_id) VALUES ( ?, ? )", (name, theme_id,))
    cur.execute("SELECT * FROM lego_series WHERE name = ? ", (name,))
    series_data = cur.fetchone()
    return {
        "id": series_data[0],
        "name": series_data[1]
    }

# Saving and creating lego_kit data as a hash
def _getLegoKit(id: int, name: str, number_duplicates: int, complete_kit: bool, for_sale: bool, box_location: str, notes: str, series_id: int) -> dict:
    if complete_kit:
        comp_num = 1
    else:
        comp_num = 0
    if for_sale:
        sale_num = 1
    else:
        sale_num = 0
    cur.execute("INSERT OR IGNORE INTO lego_kit (id, name, number_duplicates, complete_kit, for_sale, box_location, notes, series_id) VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )", (id, name, number_duplicates, comp_num, sale_num, box_location, notes, series_id,))
    cur.execute("SELECT * FROM lego_kit WHERE id = ? ", (id,))
    kit_data = cur.fetchone()
    print(kit_data)
    return {
        "id": kit_data[0],
        "name": kit_data[1],
        # Add in more if needed
    }

try:
    cur.execute("SELECT * FROM lego_group")
    cur.execute("SELECT * FROM lego_theme")
    cur.execute("SELECT * FROM lego_series")
    print("lego_group, lego_theme, and lego_series tables exist.")
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
        series = {}
        series_name = ""
        # Determines if the series is the same throughout the data upload or not
        has_same_series = False
        # kit = {}
        data = np.delete(data_raw, 0, 0)
        # print(type(data))
        # print(data)
        # Need to go through each piece of data and add it to the database
        for row in range(len(data)-1):
            print(f"row {row} = {data[row]}")
            column_i = 0 # use to keep track of the column index to save and add in the db
            # For all spreadsheets neet to split out missing parts from the notes
            # This will adjust the maximum number of columns to 12
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
                    if len(header) < 9:
                        if not has_same_series:
                            # We need to actually define the series since it's not with the data
                            series_prompt = "What is the series" + prompt_base
                            series_name = input(series_prompt)
                            has_same_series = True
            if not has_same_group and group_name == "":
                group_name = data[row][column_i]
                column_i += 1
            if "id" not in group:
                group = _getLegoGroup(group_name)
            if not has_same_theme and theme_name == "":
                theme_name = data[row][column_i]
                column_i += 1
            if "id" not in theme:
                theme = _getLegoTheme(theme_name, group["id"])
            if not has_same_series and series_name == "":
                series_name = data[row][column_i]
                column_i += 1
            if "id" not in series:
                series = _getLegoSeries(series_name, theme["id"])
            print(f"Lego Group = {group}")
            print(f"Lego Theme = {theme}")
            print(f"Lego Series = {series}")
            # Need the kit and parts here
            # Clearing variables that change
            if not has_same_group:
                group = {}
                group_name = ""
            if not has_same_theme:
                theme = {}
                theme_name = ""
            if not has_same_series:
                series = {}
                series_name = ""
    except:
        print("There is nothing to upload here.")
else:
    print("db not working!")

con.commit()
con.close()
