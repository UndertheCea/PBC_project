import mysql.connector

def connect_to_SQL():
    # Connect to the MySQL server
    cnx = mysql.connector.connect(
        host="localhost",
        user="pbc",
        password="jeffrey",
        database="invoice"
    )

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()
    return cnx, cursor



def create_table():
    
    create_table_query = """
    CREATE TABLE users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255),
        -- Additional user information columns...
    );

    CREATE TABLE invoices (
        invoice_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        invoice_number VARCHAR(255),
        invoice_date DATE,
        -- Additional invoice information columns...
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    """
    return create_table_query

if __name__ == "__main__":
    cnx, cursor = connect_to_SQL()
    cursor.execute(create_table())

    # example 
    user_id = 1
    insert_query = "INSERT INTO invoices (user_id, invoice_number, invoice_date) VALUES (%s, %s, %s)"
    invoice_data = (user_id, "MK-88888888", "2023-05-14")  
    cursor.execute(insert_query, invoice_data)
    




    # Execute the query to drop the table
    # drop_table_query = "DROP TABLE items;"
    # cursor.execute(drop_table_query)

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and the database connection
    cursor.close()
    cnx.close()
