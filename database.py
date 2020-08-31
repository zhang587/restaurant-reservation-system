import mysql.connector

# establishing the connection
conn = mysql.connector.connect(
    user='root', password='dbpassword', host='127.0.0.1', database='information_schema')

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Preparing SQL query to INSERT a record into the database.
sql = """INSERT INTO reservation(
   table_id, ts, reserved)
   VALUES ('1', '2020-08-02 20:27:59', 'True')"""

try:
    # Executing the SQL command
    cursor.execute(sql)

    # Commit your changes in the database
    conn.commit()

except:
    # Rolling back in case of error
    conn.rollback()

# Closing the connection
conn.close()
