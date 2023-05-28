# PBC_project

## goal 
We want to scan the invoice and provide some serivce with the line bot 
Our stuff will be stored on a server. Basically, the data we need to receive includes line commands (e.g. February invoice) and photos recognized by Line. Then, we put the recognized numbers into the database on the server.

We need to output data to that Line platform, which means we output the corresponding things depending on what the command is.



## example 
``` python
if __name__ == "__main__":
    # example 
    date = "2020/01/01"
    # create table 
    create_table()
    insert_user("A123456789")
    insert_invoice("A123456789", "AA12345678", date, 100, "invoice")     
    insert_expense("B123456789", date, 200, "expense")
    
    # list all user
    print(list_users())
    # list two table 
    display_table("users")
    display_table("invoices")

    # reform the date
    day_new = strip_day(date) # day_new = "2020/01"
    
    # show the result 
    print(count_normal("AA12345678", "A123456789", day_new))
    print(add_up_persons_monthly_cost("A123456789", day_ new))
    print(count_special("AA12345678", "A123456789", day_new))
    print(count_super("AA12345678", "A123456789", day_new))

    # delete table
    drop_table("invoices")
    drop_table("users")
    
```


## function information !!! 

Only insert function takes the date with three parameters,
other funcitons including 
``` python
def count_normal():  
def add_up_persons_monthly_cost():  
def count_special():
def count_super ():
```
should only take the date with year and month, it can be easily convert by ```strip_day(date)```. 

## function usage 
```
connect_to_SQL()
```
You do not need it, I've wrapped it in other functions

```
create_table()
```
Create two table called users and invoices. 

```
split_date_3(date_string)
```
It split YYYY/MM/DD to YYYY, MM, DD. 

```
split_date_2(date_string)
```
It split YYYY/MM to YYYY, MM. 

```
strip_day(date)
```
Strip the day from YYYY/MM/DD to YYYY/MM.

> Note that ```split_date_2(date_string)```cannot take YYYY/MM/DD, so you may need this function to transfer the date

```
insert_user(user_id)
```
It is also wrapped in ```insert_invoice()```, so don't mind it. 

```
list_users()
```
List all the users in the database, and return a dict with sequence number as key and user_id as value. 

```
insert_invoice(user_id, invoice_number, invoice_date, invoice_amount, invoice_tag)
```
Just follow the format, and it will insert the invoice into the database. 

> Note that the date should be in the format of YYYY/MM/DD.

```
insert_expense(user_id, invoice_date, invoice_amount, invoice_tag)
``` 
If it is not a invoice, you can use this function to insert the expense.

```
drop_table(table_name)
```
Delete table from the database. 

```
display_table(table_name)
```
Print table in the terminal.

```
sort_table(table_name)
```
Sort the table by user_id, then invoce_date.

I think it is not necessary in this project.
```
update_invoice_amount(invoice_id, invoice_amount)
```
It update the invoice amount by invoice_id.

```
count_normal(invoice_number, user_id, date)
```
It count the price within (200, 1000, 4000, 10000, 40000, 200000). 

It returns a dict with the key is the invoice_number and the value is the the winning price of the invoice number.

> Note that the date should be in the format of YYYY/MM

```
add_up_persons_monthly_cost(user_id, date)
```
Add up both invoice and expense of the user_id in certain month.

It return a integer named total and a list showing the invoice and expense in this month.

> Note that the date should be in the format of YYYY/MM. 

```
count_special(invoice_number, user_id, date)
```
It count the price within (10000000).

It return a dict with the key is the invoice_number and the value is 10000000. also one key is called "total", shows the totale price he wins.

> Note that the date should be in the format of YYYY/MM.

```
count_super (invoice_number, user_id, date)
```
Mainly the same as ```count_special```
but the price is within (20000000). 

> Note that the date should be in the format of YYYY/MM. 


## procedure of controlling directly using SQL 
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