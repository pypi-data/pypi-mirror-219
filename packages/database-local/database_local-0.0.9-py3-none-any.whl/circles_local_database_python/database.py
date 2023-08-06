import mysql.connector
import os
from dotenv import load_dotenv
from LoggerLocalPythonPackage.LocalLogger import _Local_Logger
load_dotenv()

local_logger=_Local_Logger


class database():
    
    def connect_to_database(self):
        try:
            host=os.getenv("RDS_HOSTNAME")
            user=os.getenv("RDS_USERNAME")
            local_logger.start("database-without-orm-local-python-package database.connect_to_database() "+"host= "+host+" user= "+user)
            mydb = mysql.connector.connect(
            host=os.getenv("RDS_HOSTNAME"),
            user=os.getenv("RDS_USERNAME"),
            password=os.getenv("RDS_PASSWORD")
        )
            local_logger.end("database-without-orm-local-python-package database.connect_to_database()")
            return mydb
        except Exception as e:
            st=str(os.getenv("RDS_HOSTNAME")+" "+os.getenv("RDS_USERNAME"))
            local_logger.exception(st,object=e)

        
