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
    cnx, cursor = connect_to_SQL()
    cursor.execute("SHOW TABLES LIKE 'users';")
    users_table_exists = cursor.fetchone() is not None

    cursor.execute("SHOW TABLES LIKE 'invoices'")
    invoices_table_exists = cursor.fetchone() is not None
    
    if not users_table_exists:
        
        # create the user table
        create_table_query = """
        CREATE TABLE users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255)

        ); 
        """
        cursor.execute(create_table_query)
        cnx.commit 

        
    if not invoices_table_exists: 
        # create the invoices table
        create_table_query = """
        CREATE TABLE invoices (
            invoice_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            invoice_number VARCHAR(255),
            invoice_date DATE,
            invoice_amount DECIMAL(10,2),

            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        """
        cursor.execute(create_table_query)
        cnx.commit
        
    # Close the cursor and connection
    cursor.close()
    cnx.close()

def add_column(table_name, column_name):
    cnx, cursor = connect_to_SQL()
    add_column_query = "ALTER TABLE " + table_name + " ADD COLUMN " + column_name + " VARCHAR(255)"
    cursor.execute(add_column_query)
    cnx.commit()
    print(f"Column '{column_name}' added successfully to table '{table_name}'.")
    
    # Close the cursor and connection
    cursor.close()
    cnx.close()
            

def insert_user(user_id):
    cnx, cursor = connect_to_SQL()
    insert_query = "INSERT INTO users (user_id) VALUES (%s)"
    user_data = (user_id,)
    cursor.execute(insert_query,user_data)
    cnx.commit()
    
    # Close the cursor and connection
    cursor.close()
    cnx.close()

def insert_invoice(user_id, invoice_number, invoice_date):
    cnx, cursor = connect_to_SQL()
    
    select_query = "SELECT * FROM users WHERE user_id = %s"
    user_data = (user_id,)
    cursor.execute(select_query, user_data)
    user_exists = cursor.fetchone() is not None
    if not user_exists:
        insert_query = "INSERT INTO invoices (user_id, invoice_number, invoice_date) VALUES (%s, %s, %s)"
        invoice_data = (user_id, invoice_number, invoice_date)
        cursor.execute(insert_query, invoice_data)
        cnx.commit()
        print("Invoice inserted successfully")
    else:
        print("User does not exist")
        insert_user(user_id)
        insert_invoice(user_id, invoice_number, invoice_date)
        
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
def drop_table(table_name):
    cnx, cursor = connect_to_SQL()
    drop_table_query = "DROP TABLE " + table_name + ";"
    cursor.execute(drop_table_query)
    cnx.commit()
    print(f"Table '{table_name}' dropped successfully.")
    
    # Close the cursor and connection
    cursor.close()
    cnx.close()
def display_table(table_name):
    cnx, cursor = connect_to_SQL()
    select_query = "SELECT * FROM " + table_name + ";"
    cursor.execute(select_query)   
    result = cursor.fetchall()
    
    for row in result:
        print(row)
        
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
def sort_invoices():
    cnx, cursor = connect_to_SQL()
    select_query = "SELECT * FROM invoices ORDER BY invoice_date;"
    cursor.execute(select_query)   
      
    # Close the cursor and connection
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    # example 
    drop_table("invoices")
    drop_table("users")
    create_table()
    # insert_invoice(1, "1234", "2021-01-01")
    insert_invoice(2, "5678", "2021-01-02")
    insert_invoice(3, "9101", "2021-01-03")
    display_table("invoices")
    sort_invoices()
    display_table("invoices")
    


    # Execute the query to drop the table
    # drop_table_query = "DROP TABLE items;"
    # cursor.execute(drop_table_query)
    
