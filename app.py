import sqlite3
from flask import Flask, render_template, request, jsonify


def init_sqlite_db():

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, amount TEXT, sizes TEXT, price TEXT)')
    print("Table created successfully")
    conn.close()


init_sqlite_db()


app = Flask(__name__)

@app.route('/')
@app.route('/registration-form/')
def enter_new_student():
    return render_template('registration-form.html')


@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            name = post_data['name']
            amount = post_data['amount']
            sizes = post_data['sizes']
            price = post_data['price']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO products (name, address, city, pin_code) VALUES (?, ?, ?, ?)", (name, amount, sizes, price))
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
            cur.execute("SELECT * FROM student")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return render_template('records.html', records=records)


@app.route('/delete-student/<int:student_id>/', methods=["GET"])
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
        return render_template('delete-success.html', msg=msg)
