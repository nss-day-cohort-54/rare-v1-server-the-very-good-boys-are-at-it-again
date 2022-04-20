import json
import sqlite3
from models import Reaction

def get_all_reactions():
    """This function will return all reactions in a list in json format
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        # convert rowfactory to Row to provide both index-based
        # and case-insensitive name-based access to columns
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            r.id,
            r.label,
            r.image_url
        FROM reactions r
        """)

        reactions = []

        # convert data from query into python iterable
        dataset = db_cursor.fetchall()

        # for each row of data create an instance of reaction class
        for row in dataset:
            reaction = Reaction(row['id'], row['label'], row['image_url'])

            reactions.append(reaction.__dict__)

    return json.dumps(reactions)
