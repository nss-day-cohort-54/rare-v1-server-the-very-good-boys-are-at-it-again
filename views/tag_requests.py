import json
import sqlite3
from models import Tag

def get_all_tags():
    """This function will return all tags in list in json format
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        # convert rowfactory to Row to provide both index-based
        # and case-insensitive name-based access to columns
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # execute SQL query for tags
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        ORDER BY label ASC
        """)

        tags = []

        # turn data from query into python iterable
        dataset = db_cursor.fetchall()
        # loop over data and create an object for each row
        for row in dataset:
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    return json.dumps(tags)

def get_single_tag(id):
    """This function will return a single row from tags table based on id
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM tags t
        WHERE id = ?
        """, (id,))

        data = db_cursor.fetchone()

        tag = Tag(data['id'], data['label'],)

        return json.dumps(tag.__dict__)

def delete_tag(id):
    """This function will delete a tag at specific id
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM tags
        WHERE id = ?
        """,(id,))

def update_tag(id, new_tag):
    """This function will edit/update a tag at specific id
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE tags
            SET
                label = ?
        WHERE id = ?
        """,(new_tag['label'], id,))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    return True

def create_tag(new_tag):
    """This function will create a new tag row in tags table
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO tags
                (label)
            VALUES
                (?)
        """, (new_tag['label'],))

        id = db_cursor.lastrowid
        new_tag['id'] = id

    return json.dumps(new_tag)
