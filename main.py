from flask import Flask
import sqlite3 
from flask import flash, session, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/Login')
def Login():
    return render_template('Login.html')

@app.route('/Customer/', methods=['GET', 'POST'])
def Customer():

    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
       
        con = sqlite3.connect('products.db')
        sql_query="SELECT * FROM users WHERE username = '%s' AND password = '%s'"%(username, password)
        cursor = con.execute(sql_query)
       
        account = cursor.fetchone()
        
        if account:
           
            session['loggedin'] = True
            session['username'] = username
            session['id'] = account[0]
          
            return redirect('/Customerlogin', 302)
        else:
            msg = 'Incorrect username/password!'
            return render_template('Customer.html', msg=msg)
    else: 
        return render_template('Customer.html', msg=msg)
     
    
    

@app.route('/Admin/', methods=['GET', 'POST'])
def Admin():
    msg = ''

    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        
        username = request.form['username']
        password = request.form['password']
       
        con = sqlite3.connect('products.db')
        sql_query="SELECT * FROM administrator WHERE username = '%s' AND password = '%s'"%(username, password)
        cursor = con.execute(sql_query)
       
        account = cursor.fetchone()
        
        if account:
           
            session['loggedin'] = True
            session['username'] = username
            session['id'] = account[0]
          
            return redirect('/ADDADMIN', 302)
        else:
            msg = 'Incorrect username/password!'
            return render_template('Admin.html', msg=msg)
    else: 
        return render_template('Admin.html', msg=msg)
    

@app.route('/ADDADMIN/', methods=['GET', 'POST'])
def ADD_Admin():
    if request.method == 'POST':
        bname = request.form.get('bname')
        aname = request.form.get('aname')
        ISBN = request.form.get('ISBN')
        DESCP = request.form.get('DESCP')
        Quantity = request.form.get('Quantity')
        img = request.form.get('img')
        rangeValue = request.form.get('rangeValue')

        con = sqlite3.connect('products.db')
        try:
            con.execute('CREATE TABLE added_items (bname TEXT, aname TEXT, ISBN INT primary, DESCP TEXT, Quantity INT, img image, rangeValue range)')
            print ('Table created successfully');
        except:
            pass
        
        con.close()  
        con = sqlite3.connect('products.db')
        con.execute("INSERT INTO added_items VALUES('{}','{}',{},'{}',{},'{}','{}');".format(bname, aname, int(ISBN), DESCP, int(Quantity), img, range(rangeValue)))
        con.commit()
        con.close()  
    
    return render_template('ADDADMIN.html')    


@app.route('/Customerlogin')
def Customer_login():
    try:
        con = sqlite3.connect('products.db')
        cur = con.cursor();
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return render_template('Customerlogin.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()


@app.route('/payment')
def payment():
    return render_template('payment.html')


@app.route('/add', methods=['POST'])
def add_product_to_cart():
    cursor = None
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        
        if _quantity and _code and request.method == 'POST':
            con = sqlite3.connect('products.db')
            cur = con.cursor();
            cur.execute("SELECT * FROM products WHERE code=?;", [_code])
            row = cur.fetchone()
            itemArray = { row[2] : {'name' : row[1], 'code' : row[2], 'quantity' : _quantity, 'price' : row[4], 'image' : row[3], 'total_price': _quantity * row[4]}}
            print('itemArray is', itemArray)
            
            all_total_price = 0
            all_total_quantity = 0
            
            session.modified = True
            
            if 'cart_item' in session:
                print('in session')
                if row[2] in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if row[2] == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * row[4]
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)
                    
                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = all_total_price + _quantity * row[4]
                
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            
            return redirect(url_for('.products'))
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
		
@app.route('/')
def products():
    try:
        con = sqlite3.connect('products.db')
        cur = con.cursor();
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return render_template('products.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()

@app.route('/empty')
def empty_cart():
	try:
		session.clear()
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		for item in session['cart_item'].items():
			if item[0] == code:				
				session['cart_item'].pop(item[0], None)
				if 'cart_item' in session:
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		
		if all_total_quantity == 0:
			session.clear()
		else:
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		
if __name__ == "__main__":
    app.run()
