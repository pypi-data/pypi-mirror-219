import sqlite3

# function to create a database connection
def createConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print('Error! Cannot create the database connection.')
    return conn


# function to disconnect from database
def sqlDisconnect(conn):
    conn.close()


# function to create a table
def createTable(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        print('Error! Cannot create the table.')

# function to create a new project
def createProject(conn, project):
    sql = ''' INSERT INTO project(name,description,created_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

