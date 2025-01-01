import sqlite3


con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

# Creating our tables
def _createTable(table_name: str, script: str):
    try:
        cur.execute(f"SELECT * FROM {table_name}")
        print(f"{table_name} already exists.")
    except sqlite3.OperationalError:
        msg = ""
        try:
            print(f"Creating {table_name} table...")
            cur.execute(script)
            msg += "Successfully created "
        except:
            msg += "Failed to create "
        msg += f"new {table_name} table."
        print(msg)

# For lego_group
group_script = """
CREATE TABLE IF NOT EXISTS lego_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);
"""
_createTable("lego_group",group_script)

# For lego_theme
theme_script = """
CREATE TABLE IF NOT EXISTS lego_theme (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    group_id REFERENCES lego_group (id) ON DELETE CASCADE
);
"""
_createTable("lego_theme",theme_script)

# For lego_series
series_script = """
CREATE TABLE IF NOT EXISTS lego_series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    theme_id REFERENCES lego_theme (id) ON DELETE CASCADE
);
"""
_createTable("lego_series",series_script)

# For lego_kit - Might need to fix this
# * complete_kit should be a boolean value default as false
# * for_sale should be a boolean value default as false
kit_script = """
CREATE TABLE IF NOT EXISTS lego_kit (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    number_sets INTEGER DEFAULT 1,
    complete_kit INTEGER DEFAULT 0,
    for_sale INTEGER DEFAULT 0,
    box_location TEXT,
    notes TEXT
    series_id REFERENCES lego_series (id) ON DELETE CASCADE
);
"""
_createTable("lego_kit",kit_script)

# For lego_parts
# * id (part number) - unique
# * name - unique

# For parts_to_kits
# * kit_id - foreign key
# * part_id - foreign key
# * number_of_parts - default at 1

con.commit()
con.close()