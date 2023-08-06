import mysql.connector
import os
from dotenv import load_dotenv 

load_dotenv() # Loads the credentials from the .env file as key value pair

cnx = mysql.connector.connect(user=os.environ.get('user'), password = os.environ.get('password'), 
                              host = os.environ.get('host'),  
                              database = os.environ.get('database')) 





