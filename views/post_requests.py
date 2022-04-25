import sqlite3
import json
from models import Post, User, PostTag, Category


def get_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.id user_id_new,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            pt.id post_tag_id_new,
            pt.post_id,
            pt.tag_id,
            c.id category_id_new,
            c.label
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        LEFT OUTER JOIN PostTags pt
            ON p.id = pt.post_id
        JOIN Categories c
            ON p.category_id = c.id
        """)
        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            user = User(row['user_id_new'], row['first_name'], row['last_name'], row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])

            postTag = PostTag(row['post_tag_id_new'], row['post_id'], row['tag_id'])

            category = Category(row['category_id_new'], row['label'])

            post.user = user.__dict__
            post.postTag = postTag.__dict__
            post.category = category.__dict__
            posts.append(post.__dict__)
    return json.dumps(posts)


def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        """, (id, ))
        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                    data['publication_date'], data['image_url'], data['content'], data['approved'])
        return json.dumps(post.__dict__)


def get_posts_by_user_id(user_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.id user_id_new,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM Posts p
        JOIN Users u
            ON u.id = p.user_id
        WHERE p.user_id = ?
        """, (user_id, ))

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['bio'],
                        row['username'], row['password'], row['profile_image_url'], row['created_on'], row['active'])

            post.user = user.__dict__
            posts.append(post.__dict__)
    return json.dumps(posts)


def get_posts_by_tag_id(tag_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            pt.id post_tag_id_new,
            pt.post_id,
            pt.tag_id
        FROM Posts p
        JOIN PostTags pt
            ON p.id = pt.post_id
        WHERE pt.tag_id = ?
        """, (tag_id, ))

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])
            postTag = PostTag(row['id'], row['post_id'], row['tag_id'])

            post.postTag = postTag.__dict__
            posts.append(post.__dict__)
    return json.dumps(posts)


def get_posts_by_category_id(category_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            c.id category_id_new,
            c.label
        FROM Posts p
        JOIN Categories c
            ON p.category_id = c.id
        WHERE c.id = ?
        """, (category_id, ))

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])
            category = Category(row['id'], row['label'])

            post.category = category.__dict__
            posts.append(post.__dict__)
    return json.dumps(posts)


def get_posts_by_title(title):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        WHERE p.title LIKE ?
        """, (f"%{title}%", ))
        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])
            posts.append(post.__dict__)
    return json.dumps(posts)


def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['content'], new_post['approved'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the post dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id

    return json.dumps(new_post)


def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))


def update_post(id, new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], new_post['publication_date'],
              new_post['image_url'], new_post['image_url'],
              new_post['content'], new_post['approved'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
