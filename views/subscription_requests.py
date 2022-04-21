import sqlite3
import json
from models import Subscription



def get_all_subscriptions():
    """getting all subscriptions"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM subscriptions s
        """)

        # Initialize an empty list to hold all animal representations
        subscriptions = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'],
                            row['created_on'])

            subscriptions.append(subscription.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(subscriptions)

def get_single_subscription(id):
    """gets single user"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM subscriptions s
        WHERE s.id = ?
        """, ( id, ))
        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        subscription = Subscription(data['id'], data['follower_id'], data['author_id'],
                            data['created_on'])

        return json.dumps(subscription.__dict__)

def delete_subscription(id):
    """deletes subscriptions"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM subscriptions
        WHERE id = ?
        """, (id, ))

def create_subscription(new_subscription):
    """creates comment"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO subscriptions
            ( follower_id, author_id, created_on )
        VALUES
            ( ?, ?, ?);
        """, (new_subscription['follower_id'], new_subscription['author_id'],
              new_subscription['created_on'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_subscription['id'] = id


    return json.dumps(new_subscription)