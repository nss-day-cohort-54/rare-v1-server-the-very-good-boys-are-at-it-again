import sqlite3
import json
from models import User


def get_all_users():
    """getting all users"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM users u
        """)

        # Initialize an empty list to hold all animal representations
        users = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            user = User(row['id'], row['first_name'], row['last_name'],
                            row['email'], row['bio'],
                            row['username'], row['password'], 
                            row['profile_image_url'], row['created_on'],
                            row['active'])

            users.append(user.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(users)

def get_single_user(id):
    """gets single user"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM users u
        WHERE u.id = ?
        """, ( id, ))
        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        user = User(data['id'], data['first_name'], data['last_name'],
                            data['email'], data['bio'],
                            data['username'], data['password'], 
                            data['profile_image_url'], data['created_on'],
                            data['active'])

        return json.dumps(user.__dict__)

def delete_user(id):
    """deletes users"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Users
        WHERE id = ?
        """, (id, ))