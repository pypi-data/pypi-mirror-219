from mmi_dbMethods.dbconfig import *



def writeDbTable(rows, database, TABLE_NAME):
    conn = dbConnection(database)
    try:
        TABLE_NAME.u
    except Exception as e:
        tempDbTableName = str(str(e).split(" ")[2].split("\'")[1])
    rootobj = TABLE_NAME(conn, tempDbTableName)
    rootobj.write(rows)

def readDbTable(database, TABLE_NAME):
    conn = dbConnection(database)
    try:
        TABLE_NAME.u
    except Exception as e:
        tempDbTableName = str(str(e).split(" ")[2].split("\'")[1])
    rootobj = TABLE_NAME(conn, tempDbTableName)
    datalist = []
    for row in rootobj.read():
        datalist.append(row)
    return datalist

def deleteDbTableRow(database, TABLE_NAME):
    conn = dbConnection(database)
    try:
        TABLE_NAME.u
    except Exception as e:
        tempDbTableName = str(str(e).split(" ")[2].split("\'")[1])
    rootobj = TABLE_NAME(conn, tempDbTableName)
    sqlQuery = "DELETE FROM "
    sqlQuery += tempDbTableName
    cursor = conn.cursor()
    cursor.execute(sqlQuery)
    
def executeCustomQuery(database,TABLE_NAME, sqlQuery):
    

    """ Description : This function is used to Query the Built in NDS Database Structure
      and returns the value in Tupples.
    :type database: 
    :param database: Name of the Database on which we have to Query -> (NDS-DATABASE-INSTANCE)

    :type TABLE_NAME :
    :param TABLE_NAME: Name of the Table of the Database on which we have to Query -> (NDS-TABLE-INSTANCE)

    :type sqlQuery :
    :param sqlQuery: Sqlite3 Type RDBMS Query String -> (String)

    :raises: Exception Used to Get the Table Name.

    :rtype:
    """

    conn = dbConnection(database)
    try:
        TABLE_NAME.u
    except Exception as e:
        tempDbTableName = str(str(e).split(" ")[2].split("\'")[1])
    sqlQuery +=" "
    sqlQuery += tempDbTableName
    cursor = conn.cursor()
    cursor.execute(sqlQuery)
    datalist = []
    for row in cursor:
        datalist.append(row)
    return datalist

def executeQueryOnNDS(database, TABLE_NAME, sqlQuery, condition):
    conn = dbConnection(database)
    try:
        TABLE_NAME.u
    except Exception as e:
        tempDbTableName = str(str(e).split(" ")[2].split("\'")[1])
    sqlQuery +=" "
    sqlQuery += tempDbTableName
    sqlQuery += " "
    sqlQuery += condition
    cursor = conn.cursor()
    cursor.execute(sqlQuery)
    datalist = []
    for row in cursor:
        datalist.append(row)
    return datalist

def writeDbwithBlob(rows, database, TABLE_NAME):
    conn = dbConnection(database)
    try:
        TABLE_NAME.u
    except Exception as e:
        tempDbTableName = str(str(e).split(" ")[2].split("\'")[1])
    rootobj = TABLE_NAME(conn, tempDbTableName)
    rootobj.write(rows)