import psycopg2
from psycopg2 import *
host = "localhost"
port = "5432"
database = "mmi_nds_classic"
user = "postgres"
password= "postgres"

#execute sql query
def executeQuery(query):
    """
    It create the connection object and execute query on the database by the provided query.
    Args:
        query (string): Postgres Supported Query
    """
    try:
        conn = psycopg2.connect(host= host, port=port, database=database, user=user, password=password)
        cur = conn.cursor()
        cur = cur.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(e)

def executeQueryWithReturn(query):
    """
    It create the connection object and execute query on the database by the provided query and return the result as tuples.
    Args:
        query (string): Postgres Supported Query

    Returns:
        _type_: tuples
        result: query execution result
    """
    query = query
    conn = psycopg2.connect(host= host, port=port, database=database, user=user, password=password)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data

def executeQueryToAnotherDB(query, dbName):
    """
    It create the connection object and execute query on the database by the provided query
    also it requries additional parameter which contains the name of databse over which the qurery has to fire 
    and return the result as tuples.
    Args:
        query (string): Postgres Supported Query
        dbName (string): Name of database in smaller case as string.
    """
    conn = psycopg2.connect(host= host, port=port, database=dbName, user=user, password=password)
    cur = conn.cursor()
    cur = cur.execute(query)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    executeQuery('SELECT schema_name FROM information_schema.schemata; ')

