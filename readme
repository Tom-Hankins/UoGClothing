# UoG Clothing Shop Management Application

A Level 4 university assignment project implementing a transaction management and inventory system for a high-street clothing brand.  
The application supports separate login permissions for standard users, sales staff, and admin staff, with an integrated SQLite database and QR code–based receipt system.

## Features

### User Login
- Search for items by code or name
- Make purchases with multiple items in a single transaction
- Generate receipts with unique QR codes
- View quantity of specific items or the entire inventory
- Retrieve old transactions via receipt number or QR code
- Return purchased items (returned stock is added back to inventory with a return receipt)

### Admin Login
- Add, remove, or edit items
- Review sales data and reports
- Generate reports
- Track most popular items
- Apply offers to specific items
- Track inventory
- Add or remove sales staff

### Sales Staff Login
- Check available items
- Make invoices
- Process item returns

## Database
- SQLite
- Stores registered users, admin staff, and sales staff
- Tracks all store items with code, name, quantity, and remaining stock
- Records reference numbers of all transactions
- QR codes for receipts are saved locally in the application directory

## Tech Stack
- Language: Python 3.10
- Libraries:  
  `qrcode`, `Pillow`, `fpdf`, `bcrypt`, `opencv-python`,  
  `pandas`, `pandastable`, `matplotlib`, `pyautogui`, `tkcalendar`

## Setup and Demonstration

**Pre-requisites:**  
- Python 3.10 installed  
- Required libraries installed (see above list)  

**Setup Process:**
1. Run `setup.py`
2. When prompted to set up for demonstration mode, type `Y`
3. Setup completes in under 1 minute
4. Run `uogclothing.py` to start the application

**Demo Accounts:**

| User Type | Email Address | Password |
|-----------|---------------|----------|
| Standard  | standard.user@uogclothing.com | 123 |
| Sales     | sales.user@uogclothing.com    | 123 |
| Admin     | admin.user@uogclothing.com    | 123 |

All randomly created accounts use password `123` and can be viewed via the admin login in the User Management section.

**Backup Database:**  
If setup fails to create the database, copy `clothing_company.db` from the `backup_database` folder into the main application folder.

## Original Assignment Specification

Every business needs a mechanism to manage and track its transactions, which should be robust and efficient. You are hired by a new high-street clothing brand to develop software that manages and tracks every transaction.

You are required to develop an interactive application (software) that enables the user, admin staff, and sales staff to have login access to the application by using email and password registration that will be saved in their corresponding databases. Their login has limited permissions as the following:

**User Login Permissions:**
- User should be able to enter item code or item name to select a specific item
- There can be multiple items in a single purchase
- Every transaction should generate a receipt with a unique QR code
- User should be able to view the quantity of a specific item, along with the entire inventory
- User should be able to retrieve an old transaction by either entering receipt number or by scanning the generated QR code
- User should be able to return a purchased item. Any item returned should be added to the inventory and a return receipt should be generated

**Admin Login Permissions:**
- Add/Remove/Edit Items
- Check and Review Sales Data and Reports
- Generate Reports
- Track Most Popular Items
- Apply Offers on Specific Items
- Track Inventory
- Add/Remove Sales Staff

**Sales Staff Login Permissions:**
- Check Available Items
- Make Invoice
- Return Items

The software should have a backend SQLite database that contains the registered users, admin staff, and sales staff. 
Also, the database should have all the items in store with their corresponding code, name, quantity, and quantity left. In addition, the database should save the reference number of all transactions made.

QR codes of generated purchase or return receipts should be saved in the local directory of your developed software (application).
