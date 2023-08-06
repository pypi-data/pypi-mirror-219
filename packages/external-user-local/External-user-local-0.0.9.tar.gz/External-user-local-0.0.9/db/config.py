from dotenv import load_dotenv
from circles_local_database_python import database
load_dotenv()

def db_connection():
    database_conn = database
    con=database_conn.database()
    db = con.connect_to_database()
    return db
