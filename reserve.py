#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import mysql.connector

app = Flask(__name__)

reservations = [
    {
        'id': 1,
        'restaurant': 0,
        'party_size': 5,
        'done': False
    },
    {
        'id': 2,
        'restaurant': 0,
        'party_size': 6,
        'done': False
    }
]


@app.route('/reservations', methods=['POST'])
def reserve():
    if not request.json or not 'restaurant' in request.json:
        abort(400)

    party_size = request.json["party_size"]
    restaurant_id = request.json["restaurant"]

    sql_cmd_get_max_capacity = f'select max_capacity from restaurant where restaurant_id = {restaurant_id};'
    max_capacity = db_conn(sql_cmd_input=sql_cmd_get_max_capacity)
    sql_cmd_get_curr_capacity = f'select current_capacity from restaurant where restaurant_id = {restaurant_id};'
    curr_capacity = db_conn(sql_cmd_input=sql_cmd_get_curr_capacity)
    if party_size >= max_capacity - curr_capacity:
        reservation = {
            'restaurant': restaurant_id,
            'party_size': party_size,
            'done': True
        }
        reservations.append(reservation)

        # todo: write to database
        sql_cmd_get_max_capacity = f'select max_capacity from restaurant where restaurant_id = {restaurant_id};'

        return jsonify({'task': reservation}), 201
    else:
        pass


@app.route('/reservations/<int:reservation_id>', methods=['GET'])
def get_reservation(reservation_id):
    task = [task for task in reservations if task['id'] == reservation_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/reservations', methods=['GET'])
def get_tasks():
    return jsonify({'reservations': reservations})


@app.route('/')
def index():
    return "Welcome to Shay's restaurant reservation system!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def db_conn(sql_cmd_input):
    # establishing the connection
    conn = mysql.connector.connect(
        user='root', password='password', host='127.0.0.1', database='mysql')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing SQL query to INSERT a record into the database.
    sql_cmd = sql_cmd_input

    try:
        # Executing the SQL command
        cursor.execute(sql_cmd)
        res = cursor.fetchall()
        # Commit your changes in the database
        conn.commit()
        return res[0][0]

    except:
        # Rolling back in case of error
        conn.rollback()

    # Closing the connection
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)
# class Restaurant:
#
#     def __init__(self, num_tables, table_size):
#         self.num_tables = num_tables
#         self.table_size = table_size
#         self.table_flags = ["reservable"] * self.num_tables
#         self.ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
#         self.reservation_record = {}
#
#     def reserve(self, num_customers) -> bool:
#         count_table = 0
#
#         # if there are reservable tables available
#         for i in self.table_flags:
#             if i == "reservable":
#                 count_table += 1
#
#         if count_table == 0:
#             return False
#         elif count_table * self.table_size < num_customers:  # the number of people exceeded expected capacity
#             return False
#         else:
#             num_reserved = int(num_customers / self.table_size) + 1 if num_customers % self.table_size != 0 \
#                 else num_customers / self.table_size
#             count = 0
#             for i in range(len(self.table_flags)):
#                 if self.table_flags[i] == 'reservable':
#                     self.table_flags[i] = 'non-reservable'
#                     count += 1
#                 if count == num_reserved:
#                     self.reservation_record[self.ts] = ["non-reservable"]*count
#                     break
#             return True
#
#
# if __name__ == "__main__":
#     restaurant = Restaurant(3, 4)
#     print(restaurant.reserve(4))
#     print(restaurant.table_flags)
#     print(restaurant.reservation_record)
#     print(restaurant.reserve(4))
#     print(restaurant.table_flags)
#     print(restaurant.reservation_record)
#     print(restaurant.reserve(4))
#     print(restaurant.table_flags)
#     print(restaurant.reservation_record)
