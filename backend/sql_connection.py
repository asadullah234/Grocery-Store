import psycopg2
import datetime

__cnx = None

def get_sql_connection():
    print("Opening PostgreSQL connection")
    global __cnx

    if __cnx is None:
        try:
            __cnx = psycopg2.connect(
                user="postgres",              # Your PostgreSQL username
                password="your_password",     # Your PostgreSQL password
                host="localhost",             # Database host
                port="5432",                   # Default PostgreSQL port
                database="grocery_store"       # Your database name
            )
        except Exception as e:
            print("Error connecting to PostgreSQL:", e)
            raise e

    return __cnx
