#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import mysql.connector

app = Flask(__name__)


reservation_id = 0
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
    ##todo: get reservation id here

    sql_cmd_get_num_seats_available = f'select num_seats_available from restaurant where restaurant_id = {restaurant_id};'
    num_seats_available = db_conn_read(sql_cmd_input=sql_cmd_get_num_seats_available)
    if party_size <= num_seats_available:
        global reservation_id
        reservation_id += 1
        reservation = {
            'id': reservation_id,
            'restaurant': restaurant_id,
            'party_size': party_size,
            'done': True
        }
        reservations.append(reservation)

        # write to database
        num_seats_available = num_seats_available - party_size
        sql_cmd_update_num_seats_available = f'update restaurant set num_seats_available = {num_seats_available} where restaurant_id = {restaurant_id};'
        db_conn_write(sql_cmd_input=sql_cmd_update_num_seats_available)

        return jsonify({'task': reservation}), 201
    else:
        raise ValueError(f"The restaurant {restaurant_id} is full.")

# @app.route('/reservations', methods=['POST'])
# def update_reservation(reservation_id, new_party_size):
#     exist_reservation = get_reservation(reservation_id)
#     exist_party_size = exist_reservation["party_size"]
#     restaurant_id = exist_reservation["restaurant"]
#     if exist_party_size > new_party_size:
#         print("can reserve")
#     else:
#         sql_cmd_get_num_seats_available = f'select num_seats_available from restaurant where restaurant_id = {restaurant_id};'
#         num_seats_available = db_conn_read(sql_cmd_input=sql_cmd_get_num_seats_available)
#         current_capacity = num_seats_available + exist_party_size
#         reserve()





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

def db_conn():
    # establishing the connection
    conn = mysql.connector.connect(
        user='shay', password='12345', host='127.0.0.1', database='mysql')
    return conn


def db_conn_read(sql_cmd_input):
    # establishing the connection
    conn = db_conn()

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    try:
        # Executing the SQL command
        cursor.execute(sql_cmd_input)
        res = cursor.fetchall()

        # Commit your changes in the database
        conn.commit()
        return res[0][0]

    except Exception as e:
        print(e)
        # Rolling back in case of error
        conn.rollback()

    # Closing the connection
    conn.close()

def db_conn_write(sql_cmd_input):
    # establishing the connection
    conn = db_conn()

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    try:
        # Executing the SQL command
        cursor.execute(sql_cmd_input)

        conn.commit()

    except Exception as e:
        print(e)
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
