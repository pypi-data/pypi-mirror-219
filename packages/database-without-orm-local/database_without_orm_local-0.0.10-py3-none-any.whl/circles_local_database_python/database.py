import mysql.connector
import os

class database():
    
    def connect_to_database(self):
        # TODO: Call logger.start("database-without-orm-local-python-package database.connect_to_database() RDS_HOSTNAME= RDS_USERNAMME=");
        mydb = mysql.connector.connect(
        host=os.getenv("RDS_HOSTNAME"),
        user=os.getenv("RDS_USERNAME"),
        password=os.getenv("RDS_PASSWORD")
        )
        # TODO: Call logger.end("database-without-orm-local-python-package database.connect_to_database()");

        # TODO: instead of returning mydb, store it in private data memeber/attribute in the class.
        return mydb
