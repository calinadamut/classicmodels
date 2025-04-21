from flask import Flask, render_template, request, g, url_for, redirect, get_flashed_messages, flash
import mysql.connector
# import datetime
from datetime import datetime
import logging

# Configure logging to log messages to the console (and optionally to a file)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('app.log')  # Log to a file named app.log
    ]
)

logging.info("Logging is working!")

app = Flask(__name__)
app.secret_key = '123'  # Set this to something random and secure!

# Database connection with error handling
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='debian-server-vm.home.arpa',
            user='mariadb_user',
            password='123',
            database='classicmodels'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# This runs before each request to add `current_time` to the template context
@app.before_request
def before_request():
    # Set current time globally before every route
    # current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.now().strftime('%b %d, %Y')
    # Attach current_time to the global context (accessible in every template)
    g.current_time = current_time


# Index page route
@app.route('/', methods=['GET'])
def index():
    # Render the "index.html" page
    return render_template('index.html', title="Index")

# 1. HOME
# =============================================================================
# Home page route
@app.route('/home', methods=['GET'])
def home():
    # Render the "home.html" page
    return render_template('home.html', title="Home")

# 2. CUSTOMERS
# =============================================================================
# READ - Get all customers and render them in a table with filtering
@app.route('/customers', methods=['GET'])
def get_customers():
    customer_number_filter = request.args.get('customerNumber')
    customer_name_filter = request.args.get('customerName')

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed", 500  # Handle connection error
    
    cursor = connection.cursor(dictionary=True)

    # Basic query
    query = 'SELECT * FROM customers WHERE 1=1'
    params = []

    # Add conditions if filters are applied
    if customer_number_filter:
        query += " AND customerNumber LIKE %s"
        params.append(f'%{customer_number_filter}%')
    if customer_name_filter:
        query += " AND customerName LIKE %s"
        params.append(f'%{customer_name_filter}%')

    cursor.execute(query, params)
    customers = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # Render the HTML page with customer data
    return render_template('customers.html', customers=customers, title="Customers")

#EDIT - Route to display the EDIT form for a specific customer
@app.route('/edit_customer/<int:customer_id>', methods=['GET'])
def edit_customer(customer_id):
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed", 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM customers WHERE customerNumber = %s', (customer_id,))
    customer = cursor.fetchone()

    cursor.close()
    connection.close()

    if not customer:
        return "Customer not found", 404

    return render_template('edit_customer.html', customer=customer)

#UPDATE - Route to handle UPDATING a customer
@app.route('/update_customer/<int:customer_id>', methods=['POST'])
def update_customer(customer_id):
    customer_Name = request.form['customer_Name']
    contact_Last_Name = request.form['contact_Last_Name']
    contact_First_Name = request.form['contact_First_Name']
    phone = request.form['phone']
    address_Line1 = request.form['address_Line1']
    address_Line2 = request.form['address_Line2']
    city = request.form['city']
    state = request.form['state']
    postal_Code = request.form['postal_Code']
    country = request.form['country']
    salesRepEmployeeNumber = request.form['salesRepEmployeeNumber']
    credit_Limit = request.form['credit_Limit']

    connection = get_db_connection()
    if connection is None:
        return "Database connection failed", 500

    cursor = connection.cursor()

    query = '''
        UPDATE customers
        SET customerName=%s, contactLastName=%s, contactFirstName=%s,
            phone=%s, addressLine1=%s, addressLine2=%s, city=%s,
            state=%s, postalCode=%s, country=%s, salesRepEmployeeNumber=%s,
            creditLimit=%s
        WHERE customerNumber = %s
    '''
    # Adding customer_id at the end of the parameters to match the WHERE clause
    params = (
        customer_Name, contact_Last_Name, contact_First_Name, phone,
        address_Line1, address_Line2, city, state, postal_Code, country,
        salesRepEmployeeNumber, credit_Limit, customer_id
    )

    cursor.execute(query, params)
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('get_customers'))

#DELETE - Route to delete a customer - tbd

# 3. EMPLOYEES
# =============================================================================
# Get all employees and render them in a table with filtering
@app.route('/employees', methods=['GET'])
def get_employees():
    employee_number_filter = request.args.get('employeeNumber')
    last_name_filter = request.args.get('lastName')

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed", 500  # Handle connection error
    
    cursor = connection.cursor(dictionary=True)

    # Basic query
    query = 'SELECT * FROM employees WHERE 1=1'
    params = []

    # Add conditions if filters are applied
    if employee_number_filter:
        query += " AND employeeNumber LIKE %s"
        params.append(f'%{employee_number_filter}%')
    if last_name_filter:
        query += " AND lastName LIKE %s"
        params.append(f'%{last_name_filter}%')

    cursor.execute(query, params)
    employees = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # Render the HTML page with employee data
    return render_template('employees.html', employees=employees, title="Employees")

# 4. OFFICES
# =============================================================================
# READ - Get all Offices and render them in a table with filtering
@app.route('/offices', methods=['GET'])
def get_offices():
    city_filter = request.args.get('city')
    postal_code_filter = request.args.get('postalCode')

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed", 500  # Handle connection error
    
    cursor = connection.cursor(dictionary=True)

    # Basic query
    query = 'SELECT * FROM offices WHERE 1=1'
    params = []

    # Add conditions if filters are applied
    if city_filter:
        query += " AND city LIKE %s"
        params.append(f'%{city_filter}%')
    if postal_code_filter:
        query += " AND postalCode LIKE %s"
        params.append(f'%{postal_code_filter}%')

    cursor.execute(query, params)
    offices = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # Render the HTML page with employee data
    return render_template('offices.html', offices=offices, title="Offices")

# EDIT - Route to display the EDIT form for a specific office
@app.route('/edit_office/<int:office_id>', methods=['GET'])
def edit_office(office_id):
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed", 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM offices WHERE officeCode = %s', (office_id,))
    office = cursor.fetchone()

    cursor.close()
    connection.close()

    if not office:
        return "Office not found", 404

    return render_template('edit_office.html', office=office)

# UPDATE - Route to handle UPDATING an office
@app.route('/update_office/<int:office_id>', methods=['POST'])
def update_office(office_id):
    # Get the updated values from the form
    city = request.form['city']
    phone = request.form['phone']
    address_Line1 = request.form['address_Line1']
    address_Line2 = request.form['address_Line2']
    state = request.form['state']
    country = request.form['country']
    postal_Code = request.form['postal_Code']
    territory = request.form['territory']

    # Establish a database connection
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed", 500

    cursor = connection.cursor()

    # SQL query to update the office data
    query = '''
        UPDATE offices
        SET city=%s, phone=%s, addressLine1=%s, addressLine2=%s, 
            state=%s, country=%s, postalCode=%s, territory=%s
        WHERE officeCode = %s
    '''
    
    # Ensure the order of parameters matches the query placeholders
    params = (
        city, phone, address_Line1, address_Line2, state, country, postal_Code, territory, office_id
    )

    try:
        cursor.execute(query, params)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Print the error for debugging
        return "Failed to update office", 500
    finally:
        cursor.close()
        connection.close()

    # Redirect back to the list of offices
    return redirect(url_for('get_offices'))

# INSERT - Route to handle Inserting an office
@app.route('/insert_office', methods=['GET', 'POST'])
def insert_office():
    connection = get_db_connection()
    if connection is None:
        return "Database connection failed", 500
    cursor = connection.cursor()
    
    if request.method == 'POST':
        # Recalculate the next officeCode to ensure consistency
        cursor.execute("SELECT MAX(officeCode) FROM offices")
        result = cursor.fetchone()
        next_office_code = result[0] + 1 if result[0] is not None else 1

        # Retrieve form data (officeCode is not sent by the form)
        city = request.form['city']
        phone = request.form['phone']
        address_Line1 = request.form['address_Line1']
        address_Line2 = request.form['address_Line2']
        state = request.form['state']
        country = request.form['country']
        postal_Code = request.form['postal_Code']
        territory = request.form['territory']

        # SQL query to insert the new office with the auto-generated officeCode
        query = '''
            INSERT INTO offices (officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (
            next_office_code, city, phone, address_Line1, address_Line2,
            state, country, postal_Code, territory
        )
        cursor.execute(query, params)
        connection.commit()

        cursor.close()
        connection.close()

        # Redirect to the list of offices
        return redirect(url_for('get_offices'))
    else:
        # GET method: calculate the next officeCode and pass it to the template
        cursor.execute("SELECT MAX(officeCode) FROM offices")
        result = cursor.fetchone()
        next_office_code = result[0] + 1 if result[0] is not None else 1

        cursor.close()
        connection.close()

        # Render the insert office form with the auto-generated officeCode
        return render_template('insert_office.html', office_code=next_office_code)





# DELETE - Route to handle Deleting an office
@app.route('/delete_office/<int:office_code>', methods=['POST'])
def delete_office(office_code):
    logging.info(f"DELETE route triggered for officeCode: {office_code}")

    # Get database connection
    connection = get_db_connection()
    if connection is None:
        logging.error("Database connection failed")
        flash("Database connection failed, please try again.", "error")
        return redirect(url_for('get_offices'))

    try:
        # Create a cursor to interact with the database
        cursor = connection.cursor()

        # Log the query execution
        logging.info(f"Executing DELETE query for officeCode: {office_code}")
        query = 'DELETE FROM offices WHERE officeCode = %s'
        cursor.execute(query, (office_code,))

        # Log the number of rows affected by the DELETE operation
        rows_affected = cursor.rowcount
        logging.info(f"Rows affected by DELETE query: {rows_affected}")

        if rows_affected > 0:
            logging.info(f"Deleted {rows_affected} office(s) with officeCode {office_code}")
            flash(f"Successfully deleted office with officeCode {office_code}.", "success")
        else:
            logging.warning(f"No office found with officeCode {office_code}")
            flash(f"No office found with officeCode {office_code}.", "warning")

        # Commit the changes
        connection.commit()

    except Exception as e:
        logging.error(f"Error occurred while deleting officeCode {office_code}: {e}")
        flash(f"Error occurred while deleting office with officeCode {office_code}.", "error")
        return redirect(url_for('get_offices'))

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

    logging.info(f"Office with officeCode {office_code} deletion completed.")
    return redirect(url_for('get_offices'))

















# 5. ORDERS
# =============================================================================
# Orders page
@app.route('/orders', methods=['GET'])
def orders():
    order_number_filter = request.args.get('orderNumber')
    status_filter = request.args.get('status')

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed", 500  # Handle connection error
    
    cursor = connection.cursor(dictionary=True)

    # Basic query
    query = 'SELECT * FROM orders WHERE 1=1'
    params = []

    # Add conditions if filters are applied
    if order_number_filter:
        query += " AND orderNumber LIKE %s"
        params.append(f'%{order_number_filter}%')
    if status_filter:
        query += " AND status LIKE %s"
        params.append(f'%{status_filter}%')

    cursor.execute(query, params)
    orders = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # Render the HTML page with orders data
    return render_template('orders.html', orders=orders, title="Orders")

# 6. ORDER DETAILS
# =============================================================================
# Order details page
@app.route('/orderdetails', methods=['GET'])
def orderdetails():
    orderNumber_filter = request.args.get('orderNumber')
    productCode_filter = request.args.get('productCode')

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed", 500  # Handle connection error
    
    cursor = connection.cursor(dictionary=True)

    # Basic query
    query = 'SELECT * FROM orderdetails WHERE 1=1'
    params = []

    # Add conditions if filters are applied
    if orderNumber_filter:
        query += " AND orderNumber LIKE %s"
        params.append(f'%{orderNumber_filter}%')
    if productCode_filter:
        query += " AND productCode LIKE %s"  # Correct the column name here
        params.append(f'%{productCode_filter}%')

    cursor.execute(query, params)
    orderdetails = cursor.fetchall()

    cursor.close()
    connection.close()
    
    # Render the HTML page with order details data
    return render_template('orderdetails.html', orderdetails=orderdetails, title="Order Details")

# 7. PAYMENTS
# =============================================================================
# Payments page
@app.route('/payments', methods=['GET'])
def payments():
    # Render the "payments.html" page
    return render_template('payments.html', title="Payments")

# 8. PRODUCT LINES
# =============================================================================
# Product Lines page
@app.route('/productlines', methods=['GET'])
def productlines():
    # Render the "about.html" page
    return render_template('productlines.html', title="Product Lines")

# 9. PRODUCTS
# =============================================================================
# Products page
@app.route('/products', methods=['GET'])
def products():
    # Render the "about.html" page
    return render_template('products.html', title="Products")

# 10. ABOUT
# =============================================================================
# About page
@app.route('/about', methods=['GET'])
def about():
    # Render the "about.html" page
    return render_template('about.html', title="About")

if __name__ == '__main__':
    app.run(debug=True)
