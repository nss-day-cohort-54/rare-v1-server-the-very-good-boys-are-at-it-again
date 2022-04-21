import sqlite3
import json
from models import DemotionQueue


def get_all_demotion_queues():
    """getting all ques"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            d.id,
            d.action,
            d.admin_id,
            d.approver_one_id
        FROM demotionqueue d
        """)

        # Initialize an empty list to hold all animal representations
        demotion_queues = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            demotion_queue = DemotionQueue(row['id'], row['action'], row['admin_id'], row['approver_one_id'])

            demotion_queues.append(demotion_queue.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(demotion_queues)

def get_single_demotion_queue(id):
    """gets single que"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            d.id,
            d.action,
            d.admin_id,
            d.approver_one_id
        FROM demotionqueue d
        WHERE d.id = ?
        """, ( id, ))
        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        demotion_queue = DemotionQueue(data['id'], data['action'], data['admin_id'], data['approver_one_id'])

        return json.dumps(demotion_queue.__dict__)

def delete_demotion_queue(id):
    """deletes subscriptions"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM demotionqueue d
        WHERE id = ?
        """, (id, ))

def create_demotion_queue(new_demotion_queue):
    """creates que"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO demotionqueue
            ( action, admin_id, approver_one_id )
        VALUES
            ( ?, ?, ?);
        """, (new_demotion_queue['action'], new_demotion_queue['follower_id'], new_demotion_queue['author_id'],
               ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_demotion_queue['id'] = id


    return json.dumps(new_demotion_queue)