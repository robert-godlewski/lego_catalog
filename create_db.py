import sqlite3


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

# For lego_theme
try:
    cur.execute("SELECT * FROM lego_theme")
    print("lego_theme already exists.")
except sqlite3.OperationalError:
    msg = ""
    try:
        print("Creating a lego_theme table...")
        cur.execute("""CREATE TABLE IF NOT EXISTS lego_theme (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    group_id REFERENCES lego_group (id) ON DELETE CASCADE
        )""")
        msg += "Successfully created "
    except:
        msg += "Failed to create "
    msg += "new lego_theme table."
    print(msg)

# For lego_series
try:
    cur.execute("SELECT * FROM lego_series")
    print("lego_series already exists.")
except sqlite3.OperationalError:
    msg = ""
    try:
        print("Creating a lego_series table...")
        cur.execute("""CREATE TABLE IF NOT EXISTS lego_series (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    theme_id REFERENCES lego_theme (id) ON DELETE CASCADE
        )""")
        msg += "Successfully created "
    except:
        msg += "Failed to create "
    msg += "new lego_series table."
    print(msg)

# For lego_kit
try:
    cur.execute("SELECT * FROM lego_kit")
    print("lego_kit already exists.")
except sqlite3.OperationalError:
    msg = ""
    try:
        print("Creating a lego_kit table...")
        # Might need to fix this actually
        # * complete_kit and for_sale should be a boolean
        cur.execute("""CREATE TABLE IF NOT EXISTS lego_kit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    number_duplicates INTEGER DEFAULT 1,
                    complete_kit INTEGER DEFAULT 0,
                    for_sale INTEGER DEFAULT 0,
                    box_location TEXT,
                    notes TEXT
                    series_id REFERENCES lego_series (id) ON DELETE CASCADE
        )""")
        msg += "Successfully created "
    except:
        msg += "Failed to create "
    msg += "new lego_kit table."
    print(msg)

con.commit()
con.close()