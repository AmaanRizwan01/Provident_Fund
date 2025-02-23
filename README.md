# Provident Fund Management System

This is a Flask-based web application for managing employee provident funds. It allows administrators to upload employee data, manage loans, and calculate interest on available funds.

## Features
- **Employee Data Management**: Upload and manage employee personal and provident fund data.
- **Loan Management**: Add loans, recoveries, and calculate interest on available funds.
- **Data Validation**: Ensure data integrity by validating uploaded files and employee IDs.
- **Dynamic Updates**: Automatically update available funds based on loans, recoveries, and interest calculations.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, JQuery
- **Database**: MySQL
- **Other Tools**: Pandas (for Excel file handling)

## Setup Instructions

### Prerequisites
1. **Python 3.x**: Ensure Python is installed on your system.
2. **MySQL**: Install and set up a MySQL database.
3. **Git**: Install Git to clone the repository.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AmaanRizwan01/Provident_Fund.git
   cd Provident_Fund
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the MySQL database:
   - Create a database named `provident_fund`.
   - Import the schema from `provident_fund.sql`.

5. Configure the database connection:
   - Open `app/database.py` and update the database credentials:
     ```python
     def get_db_connection():
         return mysql.connector.connect(
             host="localhost",
             user="your-username",
             password="your-password",
             database="provident_fund"
         )
     ```

6. Run the Flask application:
   ```bash
   python app.py
   ```

7. Access the application in your browser:
   ```
   http://localhost:5000
   ```

## Usage

### Uploading Employee Data
1. Navigate to the **"Update Record"** section.
2. Upload the employee personal and provident fund files in Excel format.
3. The system will validate the data and insert it into the database.

### Managing Loans
1. Navigate to the **"Loan Addition"** section.
2. Enter the employee ID, loan amount, and select the date.
3. The system will calculate the new available funds and update the database.

### Managing Interest
1. Navigate to the **"Interest"** section.
2. Enter the employee ID, interest rate, and select the date.
3. The system will calculate the interest amount and update the available funds.

### Managing Loan Recoveries
1. Navigate to the **"Loan Recovery"** section.
2. Enter the employee ID, recovery amount, and select the date.
3. The system will update the available funds and loan recovery records.

## File Structure
```
Provident_Fund/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── routes.py
│   ├── static/
│   └── templates/
├── app.py
├── provident_fund.sql
├── requirements.txt
└── README.md
```

## Contact
For any questions or feedback, please get in touch with **Amaan Rizwan**.
