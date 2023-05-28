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
            invoice_tag VARCHAR(255),
            
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
    
def list_users():
    cnx, cursor = connect_to_SQL()
    select_query = "SELECT * FROM users"
    cursor.execute(select_query)
    users = cursor.fetchall()
    user_dict = {}
    for user in users:
        user_dict[user[0]] = user[1]

    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
    return user_dict

def insert_invoice(user_id, invoice_number, invoice_date, invoice_amount, invoice_tag):
    cnx, cursor = connect_to_SQL()

    select_query = "SELECT * FROM users WHERE user_id = %s"
    user_data = (user_id,)
    cursor.execute(select_query, user_data)
    user_exists = cursor.fetchone() is not None
    year, month, day = split_date_3(invoice_date)

    if not user_exists:
        print("User does not exist")
        insert_user(user_id)
    
    select_invoice_query = "SELECT * FROM invoices WHERE user_id = %s AND invoice_number = %s"
    invoice_data = (user_id, invoice_number)
    cursor.execute(select_invoice_query, invoice_data)
    invoice_exists = cursor.fetchone() is not None
    
    if invoice_exists:
        print("Invoice already exists for this user and invoice number")
    else:
        insert_query = """INSERT INTO invoices (user_id, invoice_number, invoice_date, 
                                                invoice_number_last_three, invoice_amount,
                                                invoice_year, invoice_month, invoice_tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        invoice_data = (user_id, invoice_number, invoice_date, invoice_number[-3:], invoice_amount, year, month, invoice_tag)
        cursor.execute(insert_query, invoice_data)
        cnx.commit()
        print("Invoice inserted successfully")

    # Close the cursor and connection
    cursor.close()
    cnx.close()

def insert_expense(user_id, invoice_date, invoice_amount, invoice_tag):
    cnx, cursor = connect_to_SQL()

    select_query = "SELECT * FROM users WHERE user_id = %s"
    user_data = (user_id,)
    cursor.execute(select_query, user_data)
    user_exists = cursor.fetchone() is not None
    year, month, day = split_date_3(invoice_date)

    if not user_exists:
        print("User does not exist. Add user!")
        insert_user(user_id)
        cursor.execute(select_query, user_data)
        user_exists = cursor.fetchone() is not None

    if user_exists:
        select_expense_query = "SELECT * FROM invoices WHERE user_id = %s AND invoice_date = %s AND invoice_amount = %s AND invoice_tag = %s"
        expense_data = (user_id, invoice_date, invoice_amount, invoice_tag)
        cursor.execute(select_expense_query, expense_data)
        expense_exists = cursor.fetchone() is not None
        
        if expense_exists:
            print("Expense already exists for this user, date, amount, and tag")
        else:
            insert_query = """INSERT INTO invoices (user_id, invoice_date, 
                                                    invoice_amount,
                                                    invoice_year, invoice_month, invoice_tag) VALUES (%s, %s, %s, %s, %s, %s);"""
            invoice_data = (user_id, invoice_date, invoice_amount, year, month, invoice_tag)
            cursor.execute(insert_query, invoice_data)
            cnx.commit()
            print("Expense inserted successfully")
    else:
        print("User does not exist")

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
    Invoice_number_and_price = {}
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
            Invoice_number_and_price[row[2]] = 200
        elif length == 4:
            this_number = 1000
            Invoice_number_and_price[row[2]] = 1000
        elif length == 5:
            this_number = 4000
            Invoice_number_and_price[row[2]] = 4000
        elif length == 6:
            this_number = 10000
            Invoice_number_and_price[row[2]] = 10000
        elif length == 7:
            this_number = 40000
            Invoice_number_and_price[row[2]] = 40000
        elif length == 8:
            this_number = 200000
            Invoice_number_and_price[row[2]] = 200000   
        total += this_number
    Invoice_number_and_price['total'] = total
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    return Invoice_number_and_price
    
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
    result_list = []
    for row in result:
        total += row[6] # represent the invoice amount 
        result_list.append([row[3], row[8], row[6]])
        # row[3]: 日期, row[8]: 標籤, row[6]: 價格
    
        
    print(f"The total amount for {user_id} in {date} is: {total}")
    
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    return total, result_list
        
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
    Invoice_number_and_price = {}
    for row in result:
        count += 1
        Invoice_number_and_price[row[2]] = 1000000

    
    money = 10000000*count
    Invoice_number_and_price["total"] = money

    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
    return Invoice_number_and_price

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
    Invoice_number_and_price = {}
    for row in result:
        count += 1
        Invoice_number_and_price[row[2]] = 2000000
    
    money = 2000000*count
    Invoice_number_and_price["total"] = money
    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
    return Invoice_number_and_price


if __name__ == "__main__":
    # example 
    # drop_table("invoices")
    # drop_table("users")
    create_table()
    insert_user("A123456789")
    # insert_invoice(user_id, invoice_number, invoice_date, invoice_amount):
    insert_invoice("A123456789", "AA12345678", "2020/01/01", 100, "invoice")     
    insert_invoice("A123456789", "AA12345243", "2020/02/01", 200, "invoice")
    insert_invoice("A123456789", "AA12245245", "2020/03/01", 300, "invoice")
    insert_invoice("A123456789", "AA24545678", "2020/04/01", 400, "invoice")
    insert_invoice("A123456789", "AA12345670", "2020/01/01", 100, "invoice") 
    
    insert_invoice("B123456789", "BB12345678", "2020/01/01", 100, "invoice")     
    insert_invoice("B123456789", "BB12345243", "2020/02/01", 200, "invoice")
    insert_invoice("B123456789", "BB12245245", "2020/03/01", 300, "invoice")
    insert_invoice("B123456789", "BB24545678", "2020/04/01", 400, "invoice")
    insert_invoice("A123456789", "BBBBBB5678", "2020/01/01", 100, "invoice")
    insert_invoice("A123456789", "CCCCCC5678", "2020/01/01", 100, "invoice")
    
    # insert_expense(user_id, invoice_date, invoice_amount, invoice_tag):
    insert_expense("A123456789", "2020/01/01", 100, "expense")
    insert_expense("B123456789", "2020/02/01", 200, "expense")
    print("list users:")
    print(list_users())
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
    
    
    

    
