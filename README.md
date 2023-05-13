# PBC_project

## goal 
we want to scan the invoice and provide some serivce with the line bot 
Our stuff will be stored on a server. Basically, the data we need to receive includes line commands (e.g. February invoice) and photos recognized by Line. Then, we put the recognized numbers into the database on the server.

We need to output data to that Line platform, which means we output the corresponding things depending on what the command is.

## structure of the code 
```
create_table_query = """
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    price DECIMAL(10, 2)
)
"""
``` 
creates the table called item 

## procedure of controlling mysql 
log in to sql 
```
mysql -u username -p
```
switch to desire database 
```
USE invoice;
```
use the SELECT statement to display the data in a table.
```
SELECT * FROM items;
```

## problem solving 
https://ui-code.com/archives/293
https://www.cnblogs.com/ywb123/p/16696584.html