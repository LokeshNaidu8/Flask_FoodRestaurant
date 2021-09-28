from flask import *
from database import *


app=Flask('LewRestaurant')
app.secret_key="hello"


@app.route('/')
def login():
    return render_template('login.html')



@app.route('/index')
def index():
    if('name' in session and session['name']!='admin'):
        name=session['name']
        foods=viewAllFoods()
        msg=request.args.get('msg')
        return render_template('index.html',foods=foods,name=name,msg=msg)
    else:
        return redirect(url_for('login'))

# user Filter FoodS
@app.route('/filterfoodbyname')
def filterFoodByName():
    if('name' in session and session['name']!='admin'):
        name=session['name']
        foods=FilterFoodByName()
        # return redirect(url_for('index',foods=foods))
        return render_template('index.html',foods=foods,name=name)

@app.route('/filterfoodbyprice')
def filterFoodByPrice():
    if('name' in session and session['name']!='admin'):
        name=session['name']
        foods=FilterFoodByPrice()
        # return redirect(url_for('index',foods=foods))
        return render_template('index.html',foods=foods,name=name)

@app.route('/filterfoodbypricedesc')
def filterFoodByPriceDesc():
    if('name' in session and session['name']!='admin'):
        name=session['name']
        foods=FilterFoodByPriceDesc()
        # return redirect(url_for('index',foods=foods))
        return render_template('index.html',foods=foods,name=name)


# Clear Order List after user Logout
@app.route('/index/clearorder')
def clearorderIndex():
    mobile=session['mobile']
    clearOrdersHistory(mobile)
    return redirect(url_for('index'))

# Admin 
@app.route('/allfoods')
def adminallfoodsIndex():
    if(session['name']=='admin' and session['password']=='admin'):
        foods=viewAllFoods()
        return render_template('adminIndex.html',foods=foods)
    else:
        return redirect(url_for('login'))

# ADMIN Filter FoodS
@app.route('/adminfilterfoodbyname')
def adminfilterFoodByName():
        name=session['name']
        foods=FilterFoodByName()
        # return redirect(url_for('index',foods=foods))
        return render_template('adminIndex.html',foods=foods,name=name)

@app.route('/adminfilterfoodbyprice')
def adminfilterFoodByPrice():
        name=session['name']
        foods=FilterFoodByPrice()
        # return redirect(url_for('index',foods=foods))
        return render_template('adminIndex.html',foods=foods,name=name)

@app.route('/adminfilterfoodbypricedesc')
def adminfilterFoodByPriceDesc():
        name=session['name']
        foods=FilterFoodByPriceDesc()
        # return redirect(url_for('index',foods=foods))
        return render_template('adminIndex.html',foods=foods,name=name)

@app.route('/adminIndex.html')
def adminIndex():
    if(session['name']=='admin' and session['password']=='admin'):
        return redirect(url_for('adminallfoodsIndex'))
    else:
        return redirect(url_for('login'))

# Main Registeration or authentication Function
@app.route('/authenticate',methods=["POST"])
def register():
    if request.method=="POST":
        username=request.form['username']
        session['name']=username
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& username= ",username)
        mobile=int(request.form['mobileNo'])
        session['mobile']=mobile
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& mobileno= ",mobile)
        password=request.form['password']
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& password= ",password)
        session['password']=password
        user=User(username,mobile,password)
        userdetail=addUser(user)
        print("---------------------------------",userdetail,"---------------------------------")
        
        if((username=="admin") and (mobile==1234567890) and (password=="admin")):
            return redirect(url_for('adminallfoodsIndex'))
        elif(len(userdetail)==3):
            return redirect(url_for('index',msg=userdetail[2]))
        elif(len(userdetail)==4):
            return redirect(url_for('index',msg=userdetail[1]))
        else:
            return redirect('/authenticationFailed')


# Invalid login returns Authentication Failed page
@app.route('/authenticationFailed')
def authFailed():
    return render_template('authfailed.html',ermsg="The Mobile Number is already Registered So please check your Username OR Password")

#Template for addFood
@app.route('/addfood')
def addfoodPage():
    if('name' in session and session['name']=='admin' and session['password']=='admin'):
        return render_template('addfood.html')
    else:
        return redirect(url_for('login'))    

#Adding food in database Function
@app.route('/addFoodInDatabase',methods=['POST'])
def addFoodInDatabase():
    
    if ((request.method=="POST") and (session['name']=='admin')):
        fid=int(request.form['foodid'])
        fname=request.form['foodname']
        ftype=request.form['foodtype']
        fprice=int(request.form['foodprice'])
        food=Food(fid,fname,ftype,fprice)
        msg=addNewFood(food)
        return redirect(url_for('.addfoodPage',msg=msg))

# Just return updateFoods page
@app.route('/updateFoods')
def updateFoods():
    if(session['name']=='admin' and session['password']=='admin'):
        foods=viewAllFoods()
        return render_template('adminupdatefoods.html',foods=foods)

#Updating Foods
@app.route('/updatingFood',methods=["POST"])
def foodUpdater():
    if(request.method=="POST"):
        id=request.form['updatefoodid']
        name=request.form['updatefoodname']
        type=request.form['updatefoodtype']
        price=request.form['updatefoodprice']
        food=Food(id,name,type,price)
        msg=updateFood(food)
        return redirect(url_for('updateFoods',msg=msg))

#Deleting Food
@app.route('/deleteFoods/<int:id>')
def deleteFoods(id):
    msg=deleteFood(id)
    return redirect(url_for('updateFoods'))

@app.route('/updaterFoodFetcher/<int:id>')
def foodupdaterfetcher(id):
    foodAttr=updateFoodFetcher(id)
    return render_template('foodupdater.html',food=foodAttr)

# User Order page
@app.route('/yourorder')
def yourOrderPage():
    name=session['name']
    mobile=session['mobile']
    orders=fetchorderfromuser(mobile)
    return render_template('yourorder.html',name=name,orders=orders)

@app.route('/orderfood/<int:id>')
def orderFood(id):
    mobile=session['mobile']
    foodOrder(id,mobile)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    mobile=session['mobile']
    clearOrdersHistory(mobile)
    print("logout mobile number is ",mobile)
    return redirect('/')

@app.route('/checkbalance')
def checkBalance():
    if('name' in session and 'mobile' in session):
        mobile=session["mobile"]
        name=session['name']
        balance=displayBalance(mobile)
        return render_template('balancepage.html',balance=balance,name=name)
    else:
        return redirect(url_for('login'))

@app.route('/paythemoney',methods=["POST"])
def payRemainingBalance():
    if(request.method=="POST"):
        balance=int(request.form['balance'])
        mobile=session["mobile"]
        name=session["name"]
        msg=payment(mobile,balance)
        if(msg!=0):
            return render_template('paymentsuccessfull.html',msg=msg,name=name)
        else:
            return redirect(url_for('checkBalance',msg="Something Went Wrong"))   

if __name__=='__main__':
    app.run(debug=True)
    

