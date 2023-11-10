# Banking-System
INTRODUCTION

With the help of our program, one can create bank accounts, update accounts, view transaction histories, deposit or withdraw money, apply for loans and view their loan status, all from a single application.
We have made use of SQL databases to store account details, transactions and loan details, and have use python mySQL connectivity to store and retrieve the data. We have used text files to return passbook statements. Modules like random and get pass were used to generate account IDs and to input passwords respectively.




ALGORITHM:
1.	Menu containing the login option / creating a new account option
2.	If new account option is selected, user is asked to enter details, and is provided with an account ID for login, and record entered into ‘accounts’ table
3.	If login option is selected, user is asked for account ID and password
4.	ID and password are checked with the database, if they match, 2nd menu is shown, else user asked to input details again
5.	Admin menu can also be accessed if pre-defined credentials are inputted. Admin menu allows the admin to modify, delete or view all account details.
6.	2nd menu contains options to make a transaction, view passbook, go to the loan menu.
7.	If transaction option is selected, user gets options to deposit/withdraw money. On completion, record is entered into ‘transacts’ table.
8.	If passbook option is selected, user gets options to view entire passbook history or history within a date range. Data is printed in a tabular form and also written to a text file.
9.	If loan option is selected, user is taken to the loan menu, where he may view his current loan status, queried from the ‘loans’ table, take a new loan and pay interest.
10.	If new loan option is selected, user is asked for details and loan amount, and is assigned with a loan number.
11.	 If pay interest option is selected, interest is calculated and amount is deducted from the account balance on confirmation.


FILES, FUNCTIONS AND TABLES USED:
Tables:
1.	Accounts: to store account details
2.	Transacts: to store transaction details 
3.	Loans: to store loan details






Functions:
1.	Loan: contains the loan menu and all of its sub options.
2.	Interest: calculates interest on the loan 
3.	Transact: carries out transactions
4.	Passbook: displays transaction history and prints it to a file
5.	Addacc: accepts details to create a new account
6.	Admin menu: contains options for all admin options
7.	Newscreen: clears the screen and prints a new one

Files:
1.	Text file used to store passbook output

Modules:
1.	Getpass: for inputting passwords
2.	Random: for generating account and loan numbers
3.	Mysql connector: for database connection
4.	Prettytable: to print data in tabular format
5.	Os: to clear the terminal’s screen
