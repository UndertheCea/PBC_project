import mysql.connector

# Connect to the MySQL server
cnx = mysql.connector.connect(
    host="localhost",
    user="pbc",
    password="jeffrey",
    database="invoice"
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Example query to insert data into the "invoice" table
query = "INSERT INTO invoice (invoice_number, customer_name, total_amount) VALUES (%s, %s, %s)"
values = (1234, "John Doe", 100.50)

create_table_query = """
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2)
)
"""

cursor.execute(create_table_query)

insert_query = "INSERT INTO items (name, price) VALUES (%s, %s)"
item = ("Product A", 9.99)

cursor.execute(insert_query, item)

# Commit the changes to the database
cnx.commit()

# Close the cursor and the database connection
cursor.close()
cnx.close()
