import sqlite3
import io
class DBAccess:
    def __init__(self):
        # When the DBAccess class is initialised create a connection to our database and a cursor
        self.conn = sqlite3.connect("clothing_company.db")
        self.cur = self.conn.cursor()

    def fetch_one_db(self, sql, params):
        try:
            # execute the passed sql code with supplied parameters
            self.cur.execute(sql, params)
            # result is returned as a tuple, this method returns either the first item that matches the query or Null
            result = self.cur.fetchone()
            return result
        except sqlite3.Error as error:
            print(f"DATABASE ERROR: {error}")
            return None

    def fetch_all_db(self, sql, params):
        try:
            self.cur.execute(sql, params)
            # result will be a list of tuples
            result = self.cur.fetchall()
            return result
        except sqlite3.Error as error:
            print(f"DATABASE ERROR: {error}")
            return None

    def insert(self, sql, params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
            return self.cur.lastrowid
        except sqlite3.Error as error:
            print(f"DATABASE ERROR: {error}")

    def update(self, sql, params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except sqlite3.Error as error:
            print(f"DATABASE ERROR: {error}")

    def delete(self, sql, params):
        try:
            self.cur.execute(sql, params)
            self.conn.commit()
        except sqlite3.Error as error:
            print(f"DATABASE ERROR: {error}")

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    @staticmethod
    def convert_to_blob(img):
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    @staticmethod
    def convert_file_to_blob(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    @staticmethod
    def create_object_list(obj_type, query_result):
        # instantiates a new list of objects by passing a tuple list as parameters
        object_list = []
        for i in query_result:
            obj = obj_type(*i)
            object_list.append(obj)
        return object_list

    @staticmethod
    def create_object(obj_type, query_result):
        # instantiates a new object by passing a tuple as parameters
        obj = obj_type(*query_result)
        return obj
