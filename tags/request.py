import sqlite3
import json
from models import Tag

def get_all_tags():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                t.id,
                t.label
            FROM Tags t
            Order By label ASC
        """)

        # Initialize an empty list to hold all tag representations
        tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an tag instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # tag class above.
            tag = Tag(row['id'], row['label'])

            tags.append(tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)

# Function with a single parameter
def get_single_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            t.id,
            t.label
        FROM Tags t
        WHERE c.id = ?
        Order By label ASC
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an tag instance from the current row
        tag = Tag(data['id'], data['label'])

    return json.dumps(tag.__dict__)

def create_tag(new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert Into Tags
            ( label )
        Values
            ( ? );
        """, (new_tag['label'],))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the category dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_tag['id'] = id

    return json.dumps(new_tag)

def delete_tag(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Delete From Tags
        Where id = ?
        """, (id, ))

def update_tag(id, new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Update Tag
            Set
                label = ?
        Where id = 
        """, (new_tag['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True