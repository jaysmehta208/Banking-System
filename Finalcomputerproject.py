
import mysql.connector as sqltor
from prettytable import PrettyTable
import random, datetime,os, getpass
def newscreen():
    os.system('clear')
    print('''


  /$$$$$$  /$$$$$$$              /$$$$$$$   /$$$$$$  /$$   /$$ /$$   /$$
 /$$__  $$| $$__  $$            | $$__  $$ /$$__  $$| $$$ | $$| $$  /$$/
| $$  \__/| $$  \ $$            | $$  \ $$| $$  \ $$| $$$$| $$| $$ /$$/ 
| $$      | $$$$$$$/            | $$$$$$$ | $$$$$$$$| $$ $$ $$| $$$$$/  
| $$      | $$____/             | $$__  $$| $$__  $$| $$  $$$$| $$  $$  
| $$    $$| $$                  | $$  \ $$| $$  | $$| $$\  $$$| $$\  $$ 
|  $$$$$$/| $$                  | $$$$$$$/| $$  | $$| $$ \  $$| $$ \  $$
 \______/ |__/                  |_______/ |__/  |__/|__/  \__/|__/  \__/
                                                                        
                                                                        
                                                                        


''')
#creating and checking modules
con=sqltor.connect(host='localhost',user='root',password='jay',auth_plugin='mysql_native_password',database='computer_project')                      
if con.is_connected():
    print('connection success')
    cursor=con.cursor()
else:
    print("false")


def indate():
    y = int(input("Enter Year(yyyy): "))
    m = int(input("Enter Month (mm): "))
    d = int(input("Enter Date (dd): "))
    return "{}-{}-{}".format(y,m,d)

#loan
def loan(cursor,accid):
    while True:
        newscreen()
        ch=int(input("Input your choice: \n1) View loan details\n2) Take a loan\n3) Pay interest\n4)Quit\n"))
        if ch==1:
            #viewing loan details
            cursor.execute("Select * from loans where user_id={}".format(accid))
            details=cursor.fetchall()
            if len(details)==0:
                print("No loans")
            else:
                x = PrettyTable(['Loan Number','User ID','Principal Borrowed','Interest Rate','Date Borrowed','Date Last Active'])
                x.add_row(list(details[0]))
                print("The details of your loan:\n",x)             
            con.commit()
            isdjf = input("Press enter to continue: ")
        if ch==2:
            #checking for unique loan
            while True:
                loan_no = random.randint(100000000, 999999999)
                cursor.execute("select loan_number from loans")
                data=cursor.fetchall()
                tab_uidl = [j for i in data for j in i]
                if loan_no in tab_uidl:
                    continue
                else:
                    break

            #entering data for new loan
            principle=int(input("Enter principle being borrowed:"))
            if principle>10000:
                interestrate=10.00
            else:
                interestrate=5.00
            date=datetime.datetime.now().strftime("%Y-%m-%d")
            addingval="Insert into loans values({},{},{},{},'{}',null)".format(loan_no,accid,principle,interestrate,date)
            cursor.execute(addingval)
            cursor.execute("Update accounts set balance = balance + {} where user_id = {}".format(principle,accid))
            con.commit() 
            cursor.execute("select max(sno) from transacts")
            maxlis = cursor.fetchall()
            try:
                maxs = int(maxlis[0][0]) + 1
            except:
                maxs = 1
            cursor.execute("select balance from accounts where user_id = {}".format(accid))
            ballis=cursor.fetchall()
            bals=ballis[0][0]
            cursor.execute("Insert into transacts VALUES({},{},'{}','deposit',{},{})".format(maxs,accid,date,principle,bals))
            con.commit()
            isdjf = input("Press enter to continue: ")
        if ch==3:
            interest(cursor,accid)
            isdjf = input("Press enter to continue: ")
        if ch==4:
            break
def interest (cursor,accid):
    cursor.execute("Select * from loans where user_id={}".format(accid))    
    details=cursor.fetchall()
    row=details[0]
    print(row)
    principle=row[2]
    interestrate=row[3]
    cursor.execute("Select year(curdate())")
    a=cursor.fetchall()
    todayyear=a[0][0]
    if row[5] is not None:
        lastactive=row[5].year
    else:
        lastactive=row[4].year
    interesttobepaidnow=(todayyear-lastactive)*(interestrate/100)*principle
    print("Since the last time this account was active was in the year ",lastactive,", interest to be paid since then is Rs",int(interesttobepaidnow))
    if int(interesttobepaidnow)==0:
        print('''You are returning to the main menu. No interest needs to be paid.
Thank you!''')
        return  
    choice=input("Will you be paying this amount today?\n")
    if choice in "yesYes":
        cursor.execute("Update accounts set balance = balance - {} where user_id = {}".format(int(interesttobepaidnow),accid))
        print("Thank you for your payment! The amount is deducted from your account")
        con.commit()
        cursor.execute("select max(sno) from transacts")
        maxlis = cursor.fetchall()
        try:
            maxs = int(maxlis[0][0]) + 1
        except:
            maxs = 1
        cursor.execute("select balance from accounts where user_id = {}".format(accid))
        ballis=cursor.fetchall()
        bals=ballis[0][0]
        cursor.execute("Select curdate()")
        b=cursor.fetchall()
        dateb = b[0][0]
        cursor.execute("Insert into transacts VALUES({},{},'{}','withdraw',{},{})".format(maxs,accid,dateb,interesttobepaidnow,bals))
        con.commit()
        
    else:
        print("Please come back next time with the required amount. Thank you!")
        return
    cursor.execute("Select curdate()")
    a=cursor.fetchall()
    temp=str(a[0][0].year)+'-'+str(a[0][0].month)+'-'+str(a[0][0].day)
    cursor.execute('update loans set date_last_active="{}" where user_id={}'.format(temp,accid))
    con.commit()
    cursor.execute("Select * from loans where user_id={}".format(accid))    
    details=cursor.fetchall()
    row=details[0]
    x1 = PrettyTable(['Loan Number','User ID','Principal Borrowed','Interest Rate','Date Borrowed','Date Last Active'])
    x1.add_row(list(row))
    print('These are the updated details of your current contract ' )
    print(x1)               
    return


#transaction
def transact(cursor, accid):
    ch = int(input("Input your choice: \n1) Deposit\n2)Withdraw\n"))
    cursor.execute("select max(sno) from transacts")
    maxlis = cursor.fetchall()
    try:
        maxs = int(maxlis[0][0]) + 1
    except:
        maxs = 1
    dateb = indate()
    if ch==1:
        amt = int(input("Enter Amount to be deposited: "))
        cursor.execute("Update accounts set balance = balance + {} where user_id = {}".format(amt,accid))
        con.commit()
        cursor.execute("select balance from accounts where user_id = {}".format(accid))
        ballis=cursor.fetchall()
        bals=ballis[0][0]
        cursor.execute("Insert into transacts VALUES({},{},'{}','deposit',{},{})".format(maxs,accid,dateb,amt,bals))
    elif ch==2:
        amt = int(input("Enter Amount to be withdrawn: "))
        cursor.execute("Update accounts set balance = balance - {} where user_id = {}".format(amt,accid))
        con.commit()
        cursor.execute("select balance from accounts where user_id = {}".format(accid))
        ballis=cursor.fetchall()
        bals=ballis[0][0]
        cursor.execute("Insert into transacts (sno, user_id, date, type, amt, balance) VALUES({},{},'{}','withdraw',{},{})".format(maxs,accid,dateb,amt,bals))
    con.commit()
    rojt=input("Transaction complete, press enter to continue...")

#PASSBOOK
def passbook(cursor, accid):
    ch = int(input("Input your choice: \n1) View entire passbook history\n2) View in between a date range\n"))
    if ch==1:
        cursor.execute("Select * from transacts where user_id = {}".format(accid))
    else:
        sd = indate()
        ed = indate()
        cursor.execute("Select * from transacts where date >= '{}' and date <= '{}' and user_id = {}".format(sd,ed,accid))
    a = cursor.fetchall()
    con.commit()
    x = PrettyTable()
    x.field_names = ['S.NO','USER ID','DATE','TYPE','AMOUNT','BALANCE']
    bh = 0
    for i in a:
        x.add_row(list(i))
    print(x)
    ofile = open("Passbook_{}.txt".format(accid),'w')
    ofile.write(str(x))
    ofile.close()
    print("Passbook saved to file")
    itghi = input("press enter to continue... ")


# admin menu
def view_all():
    tname=input('Enter Table name: ')
    query='select * from '+tname
    cursor.execute(query)
    records=cursor.fetchall()
    for rec in records :
        print(rec)
    ojpgtj = input("Press enter to continue: ")

def viewacc():
    uid=input('enter the user id: ')
    query ='select * from accounts where user_id = '+uid
    cursor.execute(query)
    myrecord=cursor.fetchone()
    print(myrecord)
    ojpgtj = input("Press enter to continue: ")

def del_all():
    tname = input ('Enter the table name to be deleted: ')
    ans=input('Do you want to delete all records from this table? enter y/n: ')
    if ans=='y':
        cursor.execute('delete from '+ tname)
        con.commit()
        print('all records deleted ')
        ojpgtj = input("Press enter to continue: ")
def delone():
    uid=input('enter user id to delete: ')
    query='delete from accounts where user_id = '+ uid 
    cursor.execute(query)
    con.commit()
    print("User deleted.")
    ojpgtj = input("Press enter to continue: ")
def modify():
    uid=input('enter user id : ')
    query ='select * from accounts where user_id = '+ uid
    cursor.execute(query)
    record=cursor.fetchone()
    name=record[1]
    balance=record[2]
    address=record[3]
    eaddress =record[4]
    phoneno=record[5]
    password = record[6]
    print('user id: ',record[0])
    print('username: ',record[1])
    print('balance: ',record[2])
    print('address: ',record[3])
    print('email address: ' ,record[4])
    print('phone no : ', record[5])
    print('password: ',record[6])
    print('username is unique for each customer and hence it can not be changed for anyone ')
    print('type value to modify or press enter for no change ')
    x=input('enter name ')
    if len (x)>0:
        name =x
    x=input('enter the address: ')
    if len(x)>0:
        address=x
    x=input('enter email address: ')
    if len (x)>0:
        eaddress=x
    x=input('enter phone number: ')
    if len (x)>0:
        phoneno=x
    x=input('enter password: ')
    if len (x)>0:
        password=x
    #query ='update accounts set uname ='+"'"name"'"+','+'balance='+"'"balance"'"+','+'address='+"'"address"'"+','+'email_address='+"'"+eaddress"'"+','+'phone_no='+"'"+phoneno+"'"+'where user_id='+uid
    query = "update accounts set uname = '{}' , balance = {}, address = '{}', email_address = '{}' , phone_no = {}, password = '{}' where user_id = {} ".format(name,balance,address,eaddress,phoneno,password,uid)
    cursor.execute(query)
    con.commit()
    print('data is updated successfully ')
    fdjog = input("Press enter to continue...")

        

    

#add accounts
def addacc():
    global cursor
    while True:
        uid = random.randint(100000000, 999999999)
        cursor.execute("select user_id from accounts")
        tab_uid=cursor.fetchall()
        tab_uidl = [j for i in tab_uid for j in i]
        if uid in tab_uid:
            continue
        else:
            break
    name = input("enter full name: ")
    
    add = input("enter your home address: ")
    eadd = input("enter your email address: ")
    amt = 0
    pnum = int(input("Enter your phone number: "))
    while True:
        pwd = input("Enter new password: ")
        pwd1 = input("confirm password: ")
        if pwd!=pwd1:
            print("passwords do not match")
        else:
            print("Thank you")
            break
    cursor.execute("insert into accounts values({},'{}',{},'{}','{}',{},'{}')".format(uid,name,amt,add,eadd,pnum,pwd))
    con.commit()
    amt = int(input("enter opening balance(5000 minimum): "))
    while amt<5000:
        print("Opening Balance must be atleast 5000...")
        amt = int(input("enter opening balance(5000 minimum): "))
    cursor.execute("select max(sno) from transacts")
    maxlis = cursor.fetchall()
    try:
        maxs = int(maxlis[0][0]) + 1
    except:
        maxs = 1
    dateb = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("Update accounts set balance = balance + {} where user_id = {}".format(amt,uid))
    con.commit()
    cursor.execute("select balance from accounts where user_id = {}".format(uid))
    ballis=cursor.fetchall()
    bals=ballis[0][0]
    cursor.execute("Insert into transacts VALUES({},{},'{}','deposit',{},{})".format(maxs,uid,dateb,amt,bals))
    print("Your User ID: ", uid)
    sdfjk = input("Account CREATED!!\n press enter to continue...")
    con.commit()


    
apw = "123456"    
while True:
    newscreen()
    ch = int(input("Input your choice:\n1) Create an account\n2) I already have an account\n3) Quit\n"))
    if ch==1:
        newscreen()
        addacc()
    elif ch==2:
        boo = True
        while boo:
            newscreen()
            accid = int(input("Enter user id: "))
            
            cursor.execute("select user_id from accounts")
            acc = cursor.fetchall()
            accl = [j for i in acc for j in i]
            pwd_login=getpass.getpass(prompt = "Enter Password: ")
            cursor.execute("select password from accounts where user_id={}".format(accid))
            tb_pwd=cursor.fetchall()
            if accid == 11111 and pwd_login==apw:
                ogjo=1
                while ogjo==1:
                    newscreen()
                    print(''' Select the desired option:
1. to view the entire table
2. to view a selected record
3. to delete the entire table
4. to delete a specific record
5. to modify data in a table
6. Exit\n''')
                    ans=int(input())
                    if ans==1:
                        view_all()
                    elif ans==2:
                        viewacc()
                    elif ans==3:
                         del_all()
                    elif ans==4:
                         delone()
                    elif ans==5:
                         modify()
                    else:
                         ogjo=2
                         continue
            elif pwd_login==tb_pwd[0][0]:
                temp = 1
                while temp == 1:
                    newscreen()
                    ch1 = int(input("Input your choice:\n1) Make a Transaction\n2) View Passbook\n3) Open loan menu\n4) Go to previous menu\n"))
                    if ch1==1:
                        newscreen()
                        transact(cursor,accid)
                    elif ch1 == 2:
                        newscreen()
                        passbook(cursor,accid)
                    elif ch1==3:
                        newscreen()
                        loan(cursor,accid)
                    else:
                        temp=2
                        boo = False
            
            
                    
                                   
            elif accid not in accl:
                print("User does not exist, Try again")
                continue
            
            else:
                print("invalid password, Please try again: ")
                boo = False
                continue
    else:
        break
