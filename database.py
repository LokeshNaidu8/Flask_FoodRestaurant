import pymysql
import re


conn=pymysql.connect(database='restaurant',host='localhost',user='root',password='')

cursor=conn.cursor()

class User:
    def __init__(self,username,mobilenumber,password,orders=None,balance=0):
        self.username=username
        self.mobilenumber=mobilenumber
        self.password=password
        self.orders=orders
        self.balance=balance

class Food:
    def __init__(self,fid,fname,ftype,fprice):
        self.fid=fid
        self.fname=fname
        self.ftype=ftype
        self.fprice=fprice


# Adding User 
def addUser(user):
    try:
        cursor.execute(f'select id,name,mobile,password from users where mobile={user.mobilenumber}')
        listOfusers=cursor.fetchone()
        print("++++++++++++++++++++++++++++++++++++++++++++++++ LIST OF USERS ",listOfusers)
        
        idchecker=conn.cursor()
        idchecker.execute("select id from users")
        idlist=idchecker.fetchall()
        if(idlist==None):
            id=1
        else:
            id=len(idlist)

        if(listOfusers==None):
            cursor.execute(f"insert into users values({id},'{user.username}',{user.mobilenumber},'{user.password}','{user.orders}','{user.balance}')")
            conn.commit()
            li=[user.username,user.mobilenumber,"You're Newly Registered to our Restaurant"]
            return li

        elif(len(listOfusers)==4):
            if(listOfusers[1]!=user.username or listOfusers[2]!=user.mobilenumber or listOfusers[3]!=user.password):
                li=[1]
                return li
            else:
                valid=conn.cursor()
                valid.execute(f"select name,mobile,password from users where mobile={user.mobilenumber}")
                a=valid.fetchone()
                li=[a[0],"You're successfully validated",a[1],a[2]]
                return li
        else:
            li=[1]
            return li
    except Exception as e:
        print("Error:- ",e)
    

# self.fid=fid, self.fname=fname, self.ftype=ftype, self.fprice=fprice

# CRUD Operations on Food 
def addNewFood(foodObj):
    foodcursor=conn.cursor()
    foodcursor.execute(f"insert into foods values({foodObj.fid},'{foodObj.fname}','{foodObj.ftype}',{foodObj.fprice})")
    conn.commit()
    return "New Food Added"

def viewAllFoods():
    viewallFoodcursor=conn.cursor()
    viewallFoodcursor.execute(f"select fid,fname,ftype,fprice from foods")
    allfoods=viewallFoodcursor.fetchall()
    return allfoods

def deleteFood(id):
    cursor.execute(f"select fname from foods where fid={id}")
    foodname=cursor.fetchone()
    print(foodname)
    deletecursor=conn.cursor()
    deletecursor.execute(f"delete from foods where fid={id}")
    conn.commit()
    return f"{foodname[0]} Deleted"

def updateFoodFetcher(id):
    updater=conn.cursor()
    updater.execute(f"select * from foods where fid={id}")
    return updater.fetchone()

def updateFood(food):
    updatecursor=conn.cursor()
    updatecursor.execute(f"update foods set fname='{food.fname}',ftype='{food.ftype}',fprice={food.fprice} where fid={food.fid}")
    conn.commit()
    return f"{food.fname} updated successfully"

# Ordering Food
def foodOrder(id,mobile):
    try:
        foodorder=conn.cursor()
        
        foodorder.execute(f"select * from foods where fid={id}")
        food=foodorder.fetchone()
        foodList=conn.cursor()
        
        foodList.execute(f"select orders from users where mobile={mobile}")
        orderhistory=foodList.fetchone()[0]

        neworder=conn.cursor()
        historystring=f"{str(food[0])},{food[1]},{food[2]},{str(food[3])}\n"
        stmt=f"update users set orders='{orderhistory+historystring}' where mobile={mobile}"
        neworder.execute(stmt)
        conn.commit()

        
        balancefetcher=conn.cursor()
        balancefetcher.execute(f"select balance from users where mobile={mobile}")
        balancehistory=balancefetcher.fetchone()[0]
        
        newconnection=pymysql.connect(user="root",host="localhost",database="restaurant",password='')
        balance=newconnection.cursor()
        balance.execute(f"update users set balance={balancehistory+food[3]} where mobile={mobile}")
        newconnection.commit()
        return f"{food[1]} is ordered"
        
    except Exception as e:
        print("Error :- ",e)


# Orders List In user Order Page
def fetchorderfromuser(mobile):
    fetcher=pymysql.connect(database='restaurant',host='localhost',user='root',password='')
    cur=fetcher.cursor()
    cur.execute(f"select orders from users where mobile={mobile}")
    orderstring=cur.fetchone()[0]
    newList=[]
    for i in orderstring.split('\n'):
        insidelist=[]
        for j in i.split(','):
            insidelist.append(j)
        newList.append(insidelist)
    newList.pop()
    return newList
    





# Balance
def displayBalance(mobile):
    balanceconnection=pymysql.connect(database='restaurant',host='localhost',user='root',password='')
    remainingBalance=balanceconnection.cursor()
    remainingBalance.execute(f"select balance from users where mobile={mobile}")
    balan=remainingBalance.fetchone()[0]
    return balan  

def payment(mobile,paid):
    paymentconn=pymysql.connect(database='restaurant',host='localhost',user='root',password='')
    paymentcursor=paymentconn.cursor()
    remainingbalance=displayBalance(mobile)
    print("\n\n\n\nRemaining balance is ",remainingbalance)
    try:
        if(paid==0):
            return 0
        elif(remainingbalance>=paid):
            cut=remainingbalance-paid
            print("\n\n---------------------------\nBalance LEft is",cut)
            paymentcursor.execute(f"update users set balance={cut} where mobile={mobile}")
            paymentconn.commit()
            return f"Amount {paid} .Rs is paid"
        else:
            return 0
    except Exception as e:
        print("Error:- ",e)


# Clear Order
def clearOrdersHistory(mobile):
    clear=conn.cursor()
    clear.execute(f"update users set orders='' where mobile={mobile}")
    conn.commit()
    return "Your order history is cleared"


#Filters
def FilterFoodByName():
    viewallFoodcursor=conn.cursor()
    viewallFoodcursor.execute(f"select fid,fname,ftype,fprice from foods order by fname")
    allfoods=viewallFoodcursor.fetchall()
    return allfoods

def FilterFoodByPrice():
    viewallFoodcursor=conn.cursor()
    viewallFoodcursor.execute(f"select fid,fname,ftype,fprice from foods order by fprice")
    allfoods=viewallFoodcursor.fetchall()
    return allfoods
def FilterFoodByPriceDesc():
    viewallFoodcursor=conn.cursor()
    viewallFoodcursor.execute(f"select fid,fname,ftype,fprice from foods order by fprice desc")
    allfoods=viewallFoodcursor.fetchall()
    return allfoods