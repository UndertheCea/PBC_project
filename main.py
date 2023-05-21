import mysql.connector
from datetime import datetime

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
            user_sequnce INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255) UNIQUE

        ); 
        """
        cursor.execute(create_table_query)
        cnx.commit 

        
    if not invoices_table_exists: 
        # create the invoices table
        create_table_query = """
        CREATE TABLE invoices (
            invoice_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            invoice_number VARCHAR(255),
            invoice_date DATE,
            invoice_month INT,
            invoice_year INT,
            invoice_amount DECIMAL(10,2),
            invoice_number_last_three INT,
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
    
def split_date_3(date_string):
    year, month, day = date_string.split('/')
    return int(year), int(month), int(day)
    
def split_date_2(date_string):
    year, month = date_string.split('/')
    return int(year), int(month)


def strip_day(date_str):
    year, month, _ = date_str.split('/')
    return year + '/' + month

            

def insert_user(user_id):
    cnx, cursor = connect_to_SQL()
    
    select_query = "SELECT * FROM users WHERE user_id = %s"
    user_data = (user_id,)
    cursor.execute(select_query, user_data)
    user_exists = cursor.fetchone() is not None
    
    if not user_exists:
        insert_query = "INSERT INTO users (user_id) VALUES (%s)"
        cursor.execute(insert_query, user_data)
        cnx.commit()
        print("User inserted successfully")
    else:
        print("User already exists")
    
    # Close the cursor and connection
    cursor.close()
    cnx.close()

def insert_invoice(user_id, invoice_number, invoice_date, invoice_amount):
    cnx, cursor = connect_to_SQL()
    
    select_query = "SELECT * FROM users WHERE user_id = %s"
    user_data = (user_id,)
    cursor.execute(select_query, user_data)
    user_exists = cursor.fetchone() is not None
    year, month, day = split_date_3(invoice_date)
    if user_exists:
        insert_query = """INSERT INTO invoices (user_id, invoice_number, invoice_date, 
                                                invoice_number_last_three, invoice_amount,
                                                invoice_year, invoice_month) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        invoice_data = (user_id, invoice_number, invoice_date, invoice_number[-3:], invoice_amount, year, month)
        cursor.execute(insert_query, invoice_data)
        cnx.commit()
        print("Invoice inserted successfully")
    else:
        print("User does not exist")
        insert_user(user_id)
        invoice_data = (user_id, invoice_number, invoice_date, invoice_number[-3:], invoice_amount)
        
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
def drop_table(table_name):
    cnx, cursor = connect_to_SQL()
    cursor.execute("SHOW TABLES LIKE %s;", (table_name,))
    table_exists = cursor.fetchone() is not None

    if table_exists:
        drop_table_query = "DROP TABLE " + table_name + ";"
        cursor.execute(drop_table_query)
        cnx.commit()
        print(f"Table '{table_name}' dropped successfully.")
    else:
        print(f"Table '{table_name}' does not exist.")

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
    select_query = "SELECT * FROM invoices ORDER BY user_id, invoice_date;"
    cursor.execute(select_query)   
    result = cursor.fetchall()
      
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
def update_invoice_amount(invoice_id, invoice_amount):
    cnx, cursor = connect_to_SQL()
    update_query = "UPDATE invoices SET invoice_amount = %s WHERE invoice_id = %s"
    invoice_data = (invoice_amount, invoice_id)
    cursor.execute(update_query, invoice_data)
    cnx.commit()
    print("Invoice amount updated successfully")
    
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
def count_normal(invoice_number, user_id, date):
    cnx, cursor = connect_to_SQL()
    year, month = split_date_2(date)
    select_query = """SELECT * FROM invoices 
                      WHERE invoice_number_last_three = %s 
                      AND user_id = %s 
                      AND invoice_year = %s
                      AND invoice_month = %s;"""
    invoice_data = (invoice_number[-3:], user_id, year, month)
    cursor.execute(select_query, invoice_data)
    result = cursor.fetchall()

    # Process and print the matching invoices
    total = 0
    for row in result:
        this_number = 0
        length = 0
        for i in range(1, len(invoice_number) + 1):
            if row[2][-i] != invoice_number[-i] or i > 8:
                break
            else:
                length += 1
        if length == 3:
            this_number = 200
        elif length == 4:
            this_number = 1000
        elif length == 5:
            this_number = 4000
        elif length == 6:
            this_number = 10000
        elif length == 7:
            this_number = 40000
        elif length == 8:
            this_number = 200000   
        total += this_number

    # Close the cursor and connection
    cursor.close()
    cnx.close()
    return total
    
def add_up_persons_monthly_cost(user_id, date):
    cnx, cursor = connect_to_SQL()
    year, month = split_date_2(date)
    select_query = """SELECT * FROM invoices WHERE user_id = %s 
                      AND invoice_year = %s
                      AND invoice_month = %s;"""
    invoice_data = (user_id, year, month)
    cursor.execute(select_query, invoice_data)
    result = cursor.fetchall()
    total = 0
    for row in result:
        total += row[6] # represent the invoice amount 
        
    print(f"The total amount for {user_id} in {date} is: {total}")
    
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    return total
        
def count_special(invoice_number, user_id, date):
    cnx, cursor = connect_to_SQL()
    year, month = split_date_2(date)
    select_query = """SELECT * FROM invoices WHERE invoice_number = %s 
                      AND user_id = %s 
                      AND invoice_year = %s
                      AND invoice_month = %s;"""
    invoice_data = (invoice_number, user_id, year, month)
    cursor.execute(select_query, invoice_data)
    result = cursor.fetchall()
    
    count = 0
    for _ in result:
        count += 1
    
    money = 10000000*count

    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
    return money


def count_super (invoice_number, user_id, date):
    cnx, cursor = connect_to_SQL()
    year, month = split_date_2(date)
    select_query = """SELECT * FROM invoices WHERE invoice_number = %s 
                      AND user_id = %s
                      AND invoice_year = %s
                      AND invoice_month = %s;"""
    invoice_data = (invoice_number, user_id, year, month)
    cursor.execute(select_query, invoice_data)
    result = cursor.fetchall()
    
    count = 0
    for _ in result:
        count += 1
    
    money = 2000000*count

    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
    return money


if __name__ == "__main__":
    # example 
    drop_table("invoices")
    drop_table("users")
    create_table()
    insert_user("A123456789")
    # insert_invoice(user_id, invoice_number, invoice_date, invoice_amount):
    insert_invoice("A123456789", "AA12345678", "2020/01/01", 100)     
    insert_invoice("A123456789", "AA12345243", "2020/02/01", 200)
    insert_invoice("A123456789", "AA12245245", "2020/03/01", 300)
    insert_invoice("A123456789", "AA24545678", "2020/04/01", 400)
    insert_invoice("A123456789", "AA12345670", "2020/01/01", 100) 
    
    insert_invoice("B123456789", "BB12345678", "2020/01/01", 100)     
    insert_invoice("B123456789", "BB12345243", "2020/02/01", 200)
    insert_invoice("B123456789", "BB12245245", "2020/03/01", 300)
    insert_invoice("B123456789", "BB24545678", "2020/04/01", 400)
    display_table("users")
    print("before sort: ")
    display_table("invoices")
    print("after sort:")
    sort_invoices()
    display_table("invoices")
    print("start to print the finding:")
    
    # count_normal(invoice_number, user_id, date)
    print(count_normal("AA12345678", "A123456789", "2020/01"))
    print(add_up_persons_monthly_cost("A123456789", "2020/01"))
    print(count_special("AA12345678", "A123456789", "2020/01"))
    print(count_super("AA12345678", "A123456789", "2020/01"))
    
    
    

    
