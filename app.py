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
        'CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, amount TEXT, gender TEXT, type TEXT, sizes TEXT, price TEXT, image TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()

app = Flask(__name__)
CORS(app)


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
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
                    "INSERT INTO products (name, amount, gender, type, sizes, price, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
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
            cur = con.cursor()
            cur.execute("SELECT * FROM products")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return jsonify(records)


"""@app.route('/delete-student/<int:student_id>/', methods=["GET"])
def delete_student(student_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE id=" + str(student_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return render_template('delete-success.html', msg=msg)"""
