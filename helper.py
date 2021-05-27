# Function to convert a list to a string separated by spaces
def listToString(s): 
    # initialize an empty string
    str1 = " " 
    
    # return string  
    return (str1.join(s))

# SQLite Commands ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
        uid             INTEGER PRIMARY KEY,
        first_name      TEXT,
        last_name       TEXT,
        current_role    TEXT,
        current_company TEXT
    );
"""

CREATE_CONNECTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS connections (
        uid1            INTEGER,
        uid2            INTEGER,
        FOREIGN KEY (uid1) REFERENCES users (uid),
        FOREIGN KEY (uid2) REFERENCES users (uid)
    );
"""

# the "OR REPLACE" accounts for if person already exists in the table
INSERT_NEW_USER = """
    INSERT OR REPLACE INTO users VALUES (?,?,?,?,?)
"""

INSERT_NEW_CONNECTION = """
    INSERT INTO connections VALUES (?,?)
"""
