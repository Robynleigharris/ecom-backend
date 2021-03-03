import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute(
        'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, amount TEXT, gender TEXT, type TEXT, sizes TEXT, price TEXT, image TEXT)')
    print("items Table created successfully")
    conn.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT)')
    print(" users Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)

@app.route('/creating-an-account/', methods=['POST'])
def add_new_user():
    msg = None
    try:
        post_data = request.get_json()
        username = post_data['username']
        email = post_data['email']
        password = post_data['password']

        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            con.commit()
            msg = username + " was successfully added to the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)
    finally:
        con.close()
        return jsonify(msg)



@app.route('/logging-into-account/', methods=['GET'])
def log_accounts():
    records = {}
    if request.method == "GET":
        msg = None
        try:
            post_data = request.get_json()
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                sql = "SELECT * FROM accounts WHERE username = ? and password = ?"
                cur.execute(sql, [username, email, password])
                records = cur.fetchall()
        except Exception as e:
            con.rollback()
            msg = "Error while fetching data: " + str(e)

        finally:
            con.close()
            return jsonify(records)

@app.route('/show-user/', methods=['GET'])
def showing_users():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("Error fetching users database " + str(e))
    finally:
        con.close()
        return jsonify(records)







@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    msg = None
    if request.method == "POST":

        try:
            post_data = request.get_json()
            name = post_data['name']
            amount = post_data['amount']
            gender = post_data['gender']
            type = post_data['type']
            sizes = post_data['sizes']
            price = post_data['price']
            image = post_data['image']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO items (name, amount, gender, type, sizes, price, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (name, amount, gender, type, sizes, price, image))
                con.commit()
                msg = name + " was successfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return jsonify(msg)


@app.route('/show-records/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory=dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM items")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return jsonify(records)


"""@app.route('/delete-record/<int:item_id>/', methods=["GET"])
def delete_record(item_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM items WHERE id=" + str(item_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting an item in the database: " + str(e)
    finally:
        con.close()
        return jsonify(records)"""
