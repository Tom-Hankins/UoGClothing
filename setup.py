import datetime
import random
import sqlite3
from dataaccess import DBAccess
import random_data
from security import Security
from PIL import Image
import os
import pyautogui


class USR:
    def __init__(self, email_address, first_name, last_name, address, city, postcode, password, user_type, is_disabled):
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.postcode = postcode
        self.password = password
        self.user_type = user_type
        self.is_disabled = is_disabled


def create_database():
    conn = sqlite3.connect("clothing_company.db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER NOT NULL PRIMARY KEY,
        email_address TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        address TEXT,
        city TEXT,
        postcode TEXT,
        password TEXT,
        user_type TEXT,
        is_disabled BOOLEAN DEFAULT 0 NOT NULL CHECK (is_disabled IN (0,1))
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stock (
        item_code INTEGER PRIMARY KEY,
        item_name TEXT,
        quantity INTEGER,
        price REAL,
        offer_price REAL,
        is_available BOOLEAN DEFAULT 1 NOT NULL CHECK (is_available IN (0,1))
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_images (
        image_id INTEGER PRIMARY KEY,
        item_code INTEGER,
        image BLOB NOT NULL,
        CONSTRAINT fk_stock
        FOREIGN KEY (item_code) REFERENCES stock(item_code)
        ON DELETE CASCADE
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
        receipt_number INTEGER PRIMARY KEY,
        user_id INTEGER,
        order_date TEXT,
        order_status TEXT,
        qr_code BLOB,
        CONSTRAINT fk_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_orders (
        stock_order_id INTEGER PRIMARY KEY,
        receipt_number INTEGER,
        item_code INTEGER,
        return_status TEXT,
        return_date TEXT,
        CONSTRAINT fk_orders
        FOREIGN KEY (receipt_number) REFERENCES orders(receipt_number)
        ON DELETE CASCADE
        CONSTRAINT fk_stock
        FOREIGN KEY (item_code) REFERENCES stock(item_code)
        ON DELETE SET NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS price_changes (
        price_change_id INTEGER PRIMARY KEY,
        item_code INTEGER,
        price REAL,
        valid_to TEXT,
        valid_from TEXT,
        CONSTRAINT fk_stock
        FOREIGN KEY (item_code) REFERENCES stock(item_code)
        ON DELETE CASCADE
        )
        """)

    conn.commit()
    cur.close()
    conn.close()

def check_data_exists():
    db = DBAccess()
    if db.fetch_all_db("SELECT * FROM users", []):
        print("Data already exists\n"
              "Please delete or rename database file if you wish to set up a new file")
        return False
    return True

def create_demonstration_users():

    user1 = USR(
        "sales.user@uogclothing.com",
        "Julie",
        "Price",
        "106 Winchcombe St, Cheltenham",
        "Gloucestershire",
        "GL52 2NW",
        Security.get_hashed_password("123"),
        "SALES",
        0
    )
    user2 = USR(
        "admin.user@uogclothing.com",
        "Anna",
        "Harris",
        "2 North Place, Cinderford",
        "Gloucestershire",
        "GL50 4DW",
        Security.get_hashed_password("123"),
        "ADMIN",
        0
    )
    user3 = USR(
        "standard.user@uogclothing.com",
        "John",
        "Smith",
        "10 High Street, Cinderford",
        "Gloucestershire",
        "GL14 2SH",
        Security.get_hashed_password("123"),
        "STANDARD",
        0
    )

    users = [user1, user2, user3]

    print("Creating Users ...")
    db = DBAccess()

    for user in users:
        sql, params = user_insert_query(user)
        db.insert(sql, params)

    db.close_connection()
    return True


def create_additional_users(num_users):
    users = []
    for i in range(num_users):
        print('\rProgress [%d%%]' % int(float((i + 1) / num_users) * 100), end="")
        first = random_data.get_random_first_name()
        last = random_data.get_random_last_name()
        email = f"{first}.{last}{random_data.get_random_email_provider()}"
        address = random_data.get_random_address()

        user = USR(
            email,
            first,
            last,
            address[0],
            address[1],
            address[2],
            Security.get_hashed_password("123"),
            "STANDARD",
            0
        )
        users.append(user)

    db = DBAccess()
    for user in users:
        sql, params = user_insert_query(user)
        db.insert(sql, params)

    db.close_connection()


def user_insert_query(user):
    params = [
        user.email_address,
        user.first_name,
        user.last_name,
        user.address,
        user.city,
        user.postcode,
        user.password,
        user.user_type,
        user.is_disabled
    ]
    sql = """INSERT INTO users 
            (email_address, first_name, last_name, address, city, postcode, password, user_type, is_disabled) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

    return sql, params


def create_stock():
    stock = [
        [1, 'UOG Brand, Mens Calf Socks', 2, 12.5, 0, 1],
        [2, 'Red Converse All Star', 6, 69.99, 59.99, 1],
        [3, 'UOG Brand Unisex Winter Beanie hat', 3, 14.99, 0, 1],
        [4, 'G-STAR RAW, Womens Noxer Straight Jeans', 4, 79, 0, 1],
        [5, "Levi's Men's 511 Slim Fit Jeans", 0, 69, 0, 0],
        [6, 'JOGAL Mens Flower Casual Button Down Short Sleeve Hawaiian Shirt', 6, 49.99, 0, 1],
        [7, 'NIKE Boys Air Max Ivo Running Shoes', 3, 69.95, 0, 1],
        [8, "Levi's Men's 511 Slim Fit Rigid Dragon Jeans", 4, 25, 18, 0],
        [9, "UOG Essentials Men's Athletic - Fit Stretch Jean", 7, 27.4, 17, 1],
        [10, 'UNIQUEBELLA Travel Raincoat Rain Jacket', 21, 15.98, 0, 1],
        [11, 'TRETORN Wings Rainjacket for Unisex', 5, 22.95, 0, 1],
        [12, "Jack & Jones Men's Jjebasic Knit Crew Neck Noos Jumper", 7, 18, 0, 1],
        [13, 'Tansozer Mens Gym Shorts Summer Running Shorts with Zip Pockets', 11, 21.99, 0, 1],
        [14, 'Izabel London Ditsy Print Tiered Skater Dress for Women', 4, 40, 0, 1],
        [15, "Men's Reversible Leather Dress Belt 1.3\" Wide Rotated Buckle", 6, 10.39, 0, 1],
        [16, 'UOG Brand Camisole', 8, 12.5, 0, 1],
        [17, 'UOG Brand Slippers', 8, 69.99, 0, 1],
        [18, 'UOG Robe', 9, 14.99, 0, 1],
        [19, 'Sarong', 10, 79, 0, 1],
        [20, 'UOG Brand Cravat', 0, 69, 0, 1],
        [21, 'Dinner Jacket', 6, 49.99, 25.99, 1],
        [22, 'Sweatshirt', 5, 69.95, 31.5, 1],
        [23, 'Socks', 0, 25, 0, 1],
        [24, 'Swimwear', 7, 27.4, 0, 1],
        [25, 'Coat', 23, 15.98, 0, 1],
        [26, 'Jacket', 6, 22.95, 0, 1],
        [27, 'Cummerbund', 9, 19, 0, 1],
        [28, 'Kilt', 5, 21.99, 0, 1],
        [29, 'Sandals', 4, 40, 22, 1],
        [30, 'Hat', 6, 10.39, 0, 1],
        [31, 'Cufflinks', 8, 12.5, 0, 1],
        [32, 'Lingerie', 6, 69.99, 0, 1],
        [33, 'Blazer', 9, 14.99, 0, 1],
        [34, 'Stockings', 10, 79, 48, 1],
        [35, 'Jeans', 0, 69, 0, 1],
        [36, 'Shawl', 8, 49.99, 0, 1],
        [37, 'Shoes', 6, 69.95, 15.95, 1],
        [38, 'Bikini', 4, 25, 0, 1],
        [39, 'Blouse', 8, 27.4, 0, 1],
        [40, 'Overalls', 24, 15.98, 0, 1],
        [41, 'Skirt', 6, 22.95, 0, 1],
        [42, 'Poncho', 8, 18, 0, 1],
        [43, 'T-Shirt', 12, 21.99, 0, 1],
        [44, 'Bow Tie', 4, 40, 0, 1],
        [45, 'Gown', 6, 10.39, 0, 1],
        [46, 'Tights', 9, 12.5, 0, 1],
        [47, 'Boxers', 8, 69.99, 49.99, 1],
        [48, 'Waistcoat', 9, 14.99, 0, 1],
        [49, 'Cardigan', 10, 79, 0, 1],
        [50, 'Dress', 0, 69, 0, 1],
        [51, 'Gloves', 10, 49.99, 0, 1],
        [52, 'Pyjamas', 6, 69.95, 0, 1],
        [53, 'Tankini', 4, 25, 0, 1],
        [54, 'Top', 8, 27.4, 0, 1],
        [55, 'Cargos', 24, 15.98, 0, 1],
        [56, 'Briefs', 6, 22.95, 0, 1],
        [57, 'Shirt', 8, 18, 0, 1],
        [58, 'Tracksuit', 12, 21.99, 15, 1],
        [59, 'Nightgown', 4, 40, 0, 1],
        [60, 'Swimming Shorts', 6, 10.39, 0, 1],
        [61, 'Sunglasses', 9, 12.5, 0, 1],
        [62, 'Bra', 8, 69.99, 0, 1],
        [63, 'Corset', 9, 14.99, 0, 1],
        [64, 'Polo Shirt', 10, 79, 0, 1],
        [65, 'Knickers', 0, 69, 0, 1],
        [66, 'Tie', 10, 49.99, 20, 1],
        [67, 'Boots', 6, 69.95, 0, 1],
        [68, 'Underwear', 4, 25, 0, 1],
        [69, 'Shorts', 8, 27.4, 0, 1],
        [70, 'Scarf', 24, 15.98, 0, 1],
        [71, 'Thong', 6, 22.95, 0, 1],
        [72, 'Hoody', 8, 18, 4, 1],
        [73, 'Suit', 12, 21.99, 0, 1],
        [74, 'Belt', 4, 40, 0, 1],
        [75, 'Jogging Suit', 6, 10.39, 0, 1],
        [76, 'Fleece', 2, 18.5, 12, 1]
    ]

    db = DBAccess()
    sql = "INSERT INTO stock VALUES (?, ?, ?, ?, ?, ?)"
    print("Creating Stock Entries ...")
    for item in stock:
        db.insert(sql, item)
    db.close_connection()


def add_stock_images():
    db = DBAccess()
    image_list = [
        [15, 'belt1.png'],
        [15, 'belt2.png'],
        [16, 'camisole.png'],
        [20, 'cravat.png'],
        [14, 'dress1.png'],
        [14, 'dress2.png'],
        [14, 'dress3.png'],
        [3, 'hat1.png'],
        [3, 'hat2.png'],
        [3, 'hat3.png'],
        [5, 'Jeans1.png'],
        [9, 'Jeans1.png'],
        [9, 'Jeans2.png'],
        [9, 'Jeans3.png'],
        [9, 'Jeans4.png'],
        [12, 'jumper1.png'],
        [12, 'jumper2.png'],
        [12, 'jumper3.png'],
        [11, 'menraincoat1.png'],
        [11, 'menraincoat2.png'],
        [11, 'menraincoat3.png'],
        [11, 'menraincoat4.png'],
        [10, 'raincoat1.png'],
        [10, 'raincoat2.png'],
        [10, 'raincoat3.png'],
        [18, 'robe.png'],
        [19, 'sarong.png'],
        [6, 'shirt1.png'],
        [6, 'shirt2.png'],
        [2, 'shoe1.png'],
        [2, 'shoe2.png'],
        [2, 'shoe3.png'],
        [2, 'shoe4.png'],
        [2, 'shoe5.png'],
        [13, 'shorts1.png'],
        [13, 'shorts2.png'],
        [17, 'slippers.png'],
        [1, 'socks1.png'],
        [1, 'socks2.png'],
        [7, 'trainer1.png'],
        [7, 'trainer2.png'],
        [7, 'trainer3.png'],
        [4, 'wjeans1.png'],
        [4, 'wjeans2.png'],
        [4, 'wjeans3.png'],
        [4, 'wjeans4.png'],
        [4, 'wjeans5.png'],
        [4, 'wjeans6.png']
    ]
    print("Adding image to database ...")
    for image in image_list:
        path = f"{os.getcwd()}\\images\\stock_images\\{image[1]}"
        print(f"{image[1]}")
        img = Image.open(path)
        blob_image = db.convert_to_blob(img)
        params = [image[0], blob_image]
        sql = """INSERT INTO stock_images (item_code, image) VALUES (?, ?)"""
        db.insert(sql, params)

    db.close_connection()


def create_dummy_orders(num_orders):
    print("Creating Dummy Orders ...")
    db = DBAccess()
    result = db.fetch_all_db("SELECT * FROM users", [])

    sql = "INSERT INTO orders (user_id, order_date, order_status) VALUES (?, ?, ?)"
    for i in range(num_orders):
        print('\rProgress [%d%%]' % int(float((i + 1) / num_orders) * 100), end="")
        user_id = random.randint(2, len(result))
        order_date = random_data.get_random_date()
        if str(order_date) > "2022-12-01":
            order_status = "INVOICE REQUIRED"
        else:
            order_status = "INVOICED"
        params = [user_id, order_date, order_status]
        db.insert(sql, params)


def add_items_to_orders():
    print("\nAdding items to orders ...")
    db = DBAccess()
    orders = db.fetch_all_db("SELECT * FROM orders", [])
    item_codes = db.fetch_all_db("SELECT * FROM stock", [])

    items_in_order = ["1"] * 25 + ["2"] * 20 + ["3"] * 15 + ["4"] * 10 + ["5"] * 5 + \
                     ["6"] * 5 + ["7"] * 5 + ["8"] * 5 + ["9"] * 5 + ["10"] * 5

    sql = "INSERT INTO stock_orders (receipt_number, item_code, return_status, return_date) VALUES (?, ?, ?, ?)"
    j = 0
    for order in orders:
        j += 1
        print('\rProgress [%d%%]' % int(float(j / len(orders)) * 100), end="")
        for i in range(int(random.choice(items_in_order))):
            item_code = random.choice(item_codes)
            item_code = item_code[0]
            return_date = None
            if random.randint(0, 100) < 5:
                return_status = "Pending"
                return_date = datetime.datetime.strptime(order[2], '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                    minutes=random.randint(1600, 4600))
                return_date = datetime.datetime.strptime(
                    str(return_date), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
                if str(order[2]) < "2022-05-01 00:00:00":
                    return_status = "Returned"
                if random.randint(0, 100) < 30:
                    return_status = "Returned"
            else:
                return_status = ""

            params = [order[0], item_code, return_status, return_date]
            db.insert(sql, params)

    db.close_connection()

def create_admin_user():
    pwd_ok = False
    pwd = ""
    while not pwd_ok:
        print("Enter an Admin Password")
        pwd = pyautogui.password(text='Enter Password', title='Enter Password', default='', mask="*")
        if Security.check_password_strength(pwd) == "":
            pwd_ok = True
        else:
            print(Security.check_password_strength(pwd))

    db = DBAccess()
    user = USR(
        "admin",
        "",
        "",
        "",
        "",
        "",
        Security.get_hashed_password(pwd),
        "ADMIN",
        0
    )
    sql, params = user_insert_query(user)
    db.insert(sql, params)

print("UoG Clothing, Database Setup:")
install_type = input("Set up for demonstration mode? (Y/N)")
create_database()

if install_type == "Y" or install_type == "y":
    if check_data_exists():
        create_demonstration_users()
        create_additional_users(97)
        create_stock()
        add_stock_images()
        create_dummy_orders(2500)
        add_items_to_orders()
else:
    if check_data_exists():
        create_demonstration_users()
        create_admin_user()
        create_stock()
        add_stock_images()

