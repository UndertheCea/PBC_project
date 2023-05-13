import mysql.connector

def store_invoice_data(invoice_number, cost, invoice_time):
    # Establish connection to the SQL Server
    cnx = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    cursor = cnx.cursor()

    # Insert the invoice data into the database
    query = "INSERT INTO invoices (invoice_number, cost, invoice_time) VALUES (%s, %s, %s)"
    values = (invoice_number, cost, invoice_time)
    cursor.execute(query, values)

    # Commit the changes and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()

def check_invoice_number(invoice_number):
    # Establish connection to the SQL Server
    cnx = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    cursor = cnx.cursor()

    # Search for the invoice number in the database
    query = "SELECT * FROM invoices WHERE invoice_number = %s"
    values = (invoice_number,)
    cursor.execute(query, values)
    result = cursor.fetchall()

    # Process the result
    if len(result) > 0:
        print("Invoice number found!")
        # Do something with the matching data
    else:
        print("Invoice number not found.")

    # Close the connection
    cursor.close()
    cnx.close()

# Example usage
store_invoice_data('INV001', 100.50, '2023-05-12')
check_invoice_number('INV001')
