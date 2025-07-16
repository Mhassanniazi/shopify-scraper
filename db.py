import mysql.connector as mysql
import os
import sys

if sys.platform == "win32":
    from dotenv import load_dotenv
    load_dotenv()
class DatabaseConnection():
    """`Database Connection` class"""

    def __init__(self, host, databasename, user, password, port="3306"):
        self.host = host
        self.databasename = databasename
        self.user = user
        self.password = password
        self.port = port

    def __str__(self):
        return f"Database Connection:\n" \
               f"DB_NAME: {self.databasename}\n" \
               f"USER_NAME: {self.user}\n" \
               f"DB_PORT: {self.port}\n" \
               f"DB_HOST: {self.host}" \

    def create_connection(self, parse=False):
        """create `Database Connection`"""
        try:
            db = mysql.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.databasename,
                port=self.port
            )
            cursor = db.cursor(dictionary=parse)
            print("Database Connection Formed")
        except:
            print("Error in Database Connection")

        return db, cursor

    def close_connection(self, cursor, db):
        """close `Database Connection` using cursor & db object"""
        cursor.close()
        db.close()
        print("Connection Succesfully Closed")


# create instance of a class
database = DatabaseConnection(host=os.getenv('db_host'),
                                databasename=os.getenv('db_name'),
                                user=os.getenv('db_username'),
                                password=os.getenv('db_password'),
                                port=os.getenv('db_port'))