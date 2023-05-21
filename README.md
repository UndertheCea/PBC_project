# PBC_project

## goal 
We want to scan the invoice and provide some serivce with the line bot 
Our stuff will be stored on a server. Basically, the data we need to receive includes line commands (e.g. February invoice) and photos recognized by Line. Then, we put the recognized numbers into the database on the server.

We need to output data to that Line platform, which means we output the corresponding things depending on what the command is.

## structure of the code 
```
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
``` 
creates the table called invoces

## procedure of controlling mysql 
log in to sql, note that pbc is the username
```
mysql -u pbc -p
```
switch to desire database 
```
USE invoice;
```
use the SELECT statement to display the data in a table.
```
SELECT * FROM invoices;
```

## problem solving 
- https://ui-code.com/archives/293
- https://www.cnblogs.com/ywb123/p/16696584.html
- https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql

## function information 

only insert function takes the date with three parameters
other funcitons including 

```
count_normal(invoice_number, user_id, date):

    
def add_up_persons_monthly_cost(user_id, date):

        
def count_special(invoice_number, user_id, date):



def count_super (invoice_number, user_id, date):
```
should only take the date with year and month, it can be easily convert by ```strip_day(date):```


