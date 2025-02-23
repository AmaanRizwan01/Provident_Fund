from flask import render_template, request, redirect, url_for, flash
from app import app
from app.database import get_db_connection
from flask import request, jsonify
import pandas as pd
from app.database import get_db_connection

@app.route("/employees")
def employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee;")
    employees = cursor.fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route("/test-db")
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM mysql.tables WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return str(tables)

@app.route("/")
def home():
    return render_template("update record.html")

@app.route('/loan')
def loan():
    return render_template('loan.html')

@app.route('/profit')
def profit():
    return render_template('profit.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/refund')
def refund():
    return render_template('refund.html')

@app.route('/payslip')
def payslip():
    return render_template('payslip.html')

@app.route('/userAccount')
def userAccount():
    return render_template('userAccount.html')

@app.route('/update_record')
def update_record():
    return render_template('update record.html')

@app.route("/save-loan", methods=["POST"])
def save_loan():
    employee_id = request.form.get("employeeID")
    loan_amount = request.form.get("loanAmount")
    loan_date = request.form.get("loanDate")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Loan (employee_no, loan_withdrawal, loan_date) VALUES (%s, %s, %s)", (employee_id, loan_amount, loan_date))
    conn.commit()
    conn.close()
    
    flash("Loan saved successfully!")
    return redirect(url_for("home"))

@app.route("/recover-loan", methods=["POST"])
def recover_loan():
    employee_id = request.form.get("employeeIDRecovery")
    recover_amount = request.form.get("recoverAmount")
    recover_date = request.form.get("recoverDate")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Loan (employee_no, loan_recovery, loan_date) VALUES (%s, %s, %s)", (employee_id, recover_amount, recover_date))
    conn.commit()
    conn.close()
    
    flash("Loan recovered successfully!")
    return redirect(url_for("home"))

@app.route("/save-interest", methods=["POST"])
def save_interest():
    employee_id = request.form.get("employeeIDInterest")
    interest_amount = request.form.get("interestAmount")
    interest_date = request.form.get("interestDate")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Loan (employee_no, loan_interest, loan_date) VALUES (%s, %s, %s)", (employee_id, interest_amount, interest_date))
    conn.commit()
    conn.close()
    
    flash("Interest saved successfully!")
    return redirect(url_for("home"))

# File Uploading route
@app.route('/upload-files', methods=['POST'])
def upload_files():
    from flask import request, jsonify
    import pandas as pd
    from app.database import get_db_connection

    personal_file = request.files.get('personalFile')
    provident_file = request.files.get('providentFile')

    if not personal_file and not provident_file:
        return jsonify({"success": False, "message": "No files uploaded."}), 400

    try:
        if personal_file:
            df_personal = pd.read_excel(personal_file)
            # Normalize column names (remove extra spaces and convert to lowercase)
            df_personal.columns = df_personal.columns.str.strip().str.lower().str.replace(' ', '_')
            required_columns = ['employeeid', 'empname', 'designation', 'department', 'grade', 'cnic', 'dateofappointment', 'lengthofservicemonths', 'calculateprofit']
            if not all(column in df_personal.columns for column in required_columns):
                return jsonify({"success": False, "message": "Personal file columns do not match the required format."}), 400

            # Check for duplicate EmployeeID values in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            duplicate_ids = []
            for _, row in df_personal.iterrows():
                cursor.execute("""
                    SELECT EmployeeID FROM employeepersonalfile WHERE EmployeeID = %s
                """, (row['employeeid'],))
                result = cursor.fetchone()
                if result:
                    duplicate_ids.append(row['employeeid'])

            if duplicate_ids:
                return jsonify({"success": False, "message": f"These Employee IDs already exist in the database: {', '.join(map(str, duplicate_ids))}"}), 400

            # Insert data into the database
            for _, row in df_personal.iterrows():
                cursor.execute("""
                    INSERT INTO employeepersonalfile (EmployeeID, EmpName, Designation, Department, Grade, CNIC, DateOfAppointment, LengthOfServiceMonths, CalculateProfit)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (row['employeeid'], row['empname'], row['designation'], row['department'], row['grade'], row['cnic'], row['dateofappointment'], row['lengthofservicemonths'], row['calculateprofit']))
            conn.commit()
            conn.close()

        if provident_file:
            df_provident = pd.read_excel(provident_file)
            # Normalize column names (remove extra spaces and convert to lowercase)
            df_provident.columns = df_provident.columns.str.strip().str.lower().str.replace(' ', '_')
            required_columns = ['employeeid', 'date', 'employeecontribution', 'universitycontribution', 'availablefunds']
            if not all(column in df_provident.columns for column in required_columns):
                return jsonify({"success": False, "message": "Provident file columns do not match the required format."}), 400

            # Check for duplicate EmployeeID values in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            duplicate_ids = []
            for _, row in df_provident.iterrows():
                cursor.execute("""
                    SELECT EmployeeID FROM employeeprovidentfile WHERE EmployeeID = %s AND Date = %s
                """, (row['employeeid'], row['date']))
                result = cursor.fetchone()
                if result:
                    duplicate_ids.append(row['employeeid'])

            if duplicate_ids:
                return jsonify({"success": False, "message": f"These Employee IDs already exist in the database: {', '.join(map(str, duplicate_ids))}"}), 400

            # Insert data into the database
            for _, row in df_provident.iterrows():
                cursor.execute("""
                    INSERT INTO employeeprovidentfile (EmployeeID, Date, EmployeeContribution, UniversityContribution, AvailableFunds)
                    VALUES (%s, %s, %s, %s, %s)
                """, (row['employeeid'], row['date'], row['employeecontribution'], row['universitycontribution'], row['availablefunds']))
            conn.commit()
            conn.close()

        return jsonify({"success": True, "message": "Files uploaded and data inserted successfully!"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
#Loan Addition
@app.route('/get-employee-details', methods=['GET'])
def get_employee_details():
    from flask import request, jsonify
    from app.database import get_db_connection

    employee_id = request.args.get('employee_id')

    if not employee_id:
        return jsonify({"success": False, "message": "Employee ID is required."}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch employee name from employeepersonalfile table
        cursor.execute("""
            SELECT EmpName FROM employeepersonalfile WHERE EmployeeID = %s
        """, (employee_id,))
        employee_name = cursor.fetchone()

        if not employee_name:
            return jsonify({"success": False, "message": "Employee not found."}), 404

        # Fetch the latest AvailableFunds from employeeprovidentfile table based on Date
        cursor.execute("""
            SELECT AvailableFunds FROM employeeprovidentfile
            WHERE EmployeeID = %s
            ORDER BY Date DESC
            LIMIT 1
        """, (employee_id,))
        available_funds = cursor.fetchone()

        conn.close()

        return jsonify({
            "success": True,
            "employee_name": employee_name[0],
            "available_funds": available_funds[0] if available_funds else 0
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/save-loan-addition', methods=['POST'])
def save_loan_addition():
    from flask import request, jsonify
    from app.database import get_db_connection
    import logging

    logging.basicConfig(level=logging.DEBUG)  # Enable logging

    try:
        # Get form data
        employee_id = request.form.get('employeeId')
        loan_amount = request.form.get('loanAmount')
        select_date = request.form.get('selectDate')
        available_funds = request.form.get('availableFunds')

        logging.debug(f"Received data: EmployeeID={employee_id}, LoanAmount={loan_amount}, Date={select_date}, AvailableFunds={available_funds}")

        # Validate form data
        if not all([employee_id, loan_amount, select_date, available_funds]):
            logging.error("Validation failed: All fields are required.")
            return jsonify({"success": False, "message": "All fields are required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert data into the loan table (LoanID is auto-incremented)
        cursor.execute("""
            INSERT INTO loan (EmployeeID, Date, LoanAmount, LoanRecoveryAmount, Interest)
            VALUES (%s, %s, %s, %s, %s)
        """, (employee_id, select_date, loan_amount, 0, 0))  # Default LoanRecoveryAmount and Interest to 0

        # Get the LoanID of the newly inserted loan record
        loan_id = cursor.lastrowid

        # Calculate new AvailableFunds by adding LoanAmount to the existing AvailableFunds
        new_available_funds = float(available_funds) - float(loan_amount)

        # Insert data into the employeeprovidentfile table (TransactionID is auto-incremented)
        cursor.execute("""
            INSERT INTO employeeprovidentfile (EmployeeID, LoanID, Date, EmployeeContribution, UniversityContribution, AvailableFunds)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (employee_id, loan_id, select_date, 0, 0, new_available_funds))  # Default EmployeeContribution and UniversityContribution to 0

        conn.commit()
        conn.close()

        logging.debug("Loan record saved and AvailableFunds updated successfully.")
        return jsonify({"success": True, "message": "Loan record saved and AvailableFunds updated successfully!"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
    
#Loan Recovery
@app.route('/save-loan-recovery', methods=['POST'])
def save_loan_recovery():
    from flask import request, jsonify
    from app.database import get_db_connection
    import logging

    logging.basicConfig(level=logging.DEBUG)  # Enable logging

    try:
        # Get form data
        employee_id = request.form.get('employeeId')
        recovery_amount = request.form.get('recoveryAmount')
        select_date = request.form.get('selectDate')
        available_funds = request.form.get('availableFunds')

        logging.debug(f"Received data: EmployeeID={employee_id}, RecoveryAmount={recovery_amount}, Date={select_date}, AvailableFunds={available_funds}")

        # Validate form data
        if not all([employee_id, recovery_amount, select_date, available_funds]):
            logging.error("Validation failed: All fields are required.")
            return jsonify({"success": False, "message": "All fields are required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert data into the loan table (LoanID is auto-incremented)
        cursor.execute("""
            INSERT INTO loan (EmployeeID, Date, LoanAmount, LoanRecoveryAmount, Interest)
            VALUES (%s, %s, %s, %s, %s)
        """, (employee_id, select_date, 0, recovery_amount, 0))  # Set LoanAmount and Interest to 0

        # Get the LoanID of the newly inserted loan record
        loan_id = cursor.lastrowid

        # Calculate new AvailableFunds by adding RecoveryAmount to the existing AvailableFunds
        new_available_funds = float(available_funds) + float(recovery_amount)

        # Insert data into the employeeprovidentfile table (TransactionID is auto-incremented)
        cursor.execute("""
            INSERT INTO employeeprovidentfile (EmployeeID, LoanID, Date, EmployeeContribution, UniversityContribution, AvailableFunds)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (employee_id, loan_id, select_date, 0, 0, new_available_funds))  # Default EmployeeContribution and UniversityContribution to 0

        conn.commit()
        conn.close()

        logging.debug("Loan recovery record saved and AvailableFunds updated successfully.")
        return jsonify({"success": True, "message": "Loan recovery record saved and AvailableFunds updated successfully!"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/save-interest-addition', methods=['POST'])
def save_interest_addition():
    from flask import request, jsonify
    from app.database import get_db_connection
    import logging

    logging.basicConfig(level=logging.DEBUG)  # Enable logging

    try:
        # Get form data
        employee_id = request.form.get('employeeId')
        interest_rate = float(request.form.get('interestRate'))  # Parse as float
        select_date = request.form.get('selectDate')
        available_funds = float(request.form.get('availableFunds'))  # Parse as float

        logging.debug(f"Received data: EmployeeID={employee_id}, InterestRate={interest_rate}, Date={select_date}, AvailableFunds={available_funds}")

        # Validate form data
        if not all([employee_id, interest_rate, select_date, available_funds]):
            logging.error("Validation failed: All fields are required.")
            return jsonify({"success": False, "message": "All fields are required."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Calculate interest amount
        interest_amount = (available_funds * interest_rate) / 100  # Correct calculation

        # Insert data into the loan table (LoanID is auto-incremented)
        cursor.execute("""
            INSERT INTO loan (EmployeeID, Date, LoanAmount, LoanRecoveryAmount, Interest)
            VALUES (%s, %s, %s, %s, %s)
        """, (employee_id, select_date, 0, 0, interest_rate))  # Set LoanAmount and LoanRecoveryAmount to 0

        # Get the LoanID of the newly inserted loan record
        loan_id = cursor.lastrowid

        # Calculate new AvailableFunds by adding interest amount to the existing AvailableFunds
        new_available_funds = available_funds + interest_amount

        # Insert data into the employeeprovidentfile table (TransactionID is auto-incremented)
        cursor.execute("""
            INSERT INTO employeeprovidentfile (EmployeeID, LoanID, Date, EmployeeContribution, UniversityContribution, AvailableFunds)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (employee_id, loan_id, select_date, 0, 0, new_available_funds))  # Default EmployeeContribution and UniversityContribution to 0

        conn.commit()
        conn.close()

        logging.debug("Interest record saved and AvailableFunds updated successfully.")
        return jsonify({"success": True, "message": "Interest record saved and AvailableFunds updated successfully!"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500