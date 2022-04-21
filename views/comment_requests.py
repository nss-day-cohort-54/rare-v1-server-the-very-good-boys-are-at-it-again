import sqlite3
import json
from models import Comment


def get_all_comments():
    """getting all coments"""
    # Open a connection to the database
    with sqlite3.connect("./db.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            co.id,
            co.author_id,
            co.post_id,
            co.content    
        FROM comments co
        """)

        # Initialize an empty list to hold all animal representations
        comments = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            comment = Comment(row['id'], row['author_id'], row['post_id'],
                            row['content'])

            comments.append(comment.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(comments)

def get_single_comment(id):
    """gets single user"""
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            co.id,
            co.author_id,
            co.post_id,
            co.content  
        FROM comments co
        WHERE co.id = ?
        """, ( id, ))
        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        comment = Comment(data['id'], data['author_id'], data['post_id'],
                            data['content'])

        return json.dumps(comment.__dict__)

def delete_comment(id):
    """deletes comment"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM comments
        WHERE id = ?
        """, (id, ))

def update_comment(id, new_comment):
    '''update animal function'''
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE comments
            co.id,
            co.author_id,
            co.post_id,
            co.content         
        WHERE id = ?
        """, (new_comment['author_id'], new_comment['post_id'],
              new_comment['content'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def create_comment(new_comment):
    """creates comment"""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO comments
            ( author_id, post_id, content )
        VALUES
            ( ?, ?, ?);
        """, (new_comment['author_id'], new_comment['post_id'],
              new_comment['content'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id


    return json.dumps(new_comment)