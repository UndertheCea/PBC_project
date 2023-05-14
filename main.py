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
        username VARCHAR(255)

    );

    CREATE TABLE invoices (
        invoice_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        invoice_number VARCHAR(255),
        invoice_date DATE,

        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    """
    return create_table_query

if __name__ == "__main__":
    cnx, cursor = connect_to_SQL()
    # create_table_query = create_table()
    # for query in create_table_query.split(";"):
    #     cursor.execute(query)
    # cnx.commit()

    # example 
    user_id = 1
    insert_query = "INSERT INTO users (user_id) VALUES (%s)"
    user_data = (user_id,)
    cursor.execute(insert_query, user_data)
    cnx.commit()
    insert_query = "INSERT INTO invoices (user_id, invoice_number, invoice_date) VALUES (%s, %s, %s)"
    invoice_data = (user_id, "MK-88888888", "2023-05-14")  
    cursor.execute(insert_query, invoice_data)
    cnx.commit()
    


    # Execute the query to drop the table
    # drop_table_query = "DROP TABLE items;"
    # cursor.execute(drop_table_query)



    # Close the cursor and the database connection
    cursor.close()
    cnx.close()
