import mysql.connector

# establishing the connection
conn = mysql.connector.connect(
    user='root', password='password', host='127.0.0.1', database='mysql')

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Preparing SQL query to INSERT a record into the database.
sql_cmd = 'select max_capacity from restaurant where restaurant_id = 0;'

try:
    # Executing the SQL command
    cursor.execute(sql_cmd)
    res = cursor.fetchall()
    print(res[0][0], type(res), type(res[0][0]))

    # Commit your changes in the database
    conn.commit()

except:
    # Rolling back in case of error
    conn.rollback()

# Closing the connection
conn.close()
