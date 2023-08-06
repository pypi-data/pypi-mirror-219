import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Additional Imports
from mmi_dbMethods.dbconfig import *
from mmi_dbConnections.postgresConnection import *
from pathlib import Path
import shutil
from  uploadCSV import main as uploadCSV, uploadAttribute

class intiDatabase:
    """ 
    This Class is used to create Database and Tables Used in the Project;
    It also provides a method for droping the tables and dropping the database.
    It overwrites the existing database with a prompt to user if the user specifies the input as
    Y or y then It will remove the existing database and create fresh database, with empty tables.
    """
    def main():
        try:
            if Path(dbPath).exists():
                if Path(dbPath+"/MMI").exists():
                    auth = str(input("If You Processed this will remove any previous Database file and generate new Database? (y/n): "))
                    auth = auth.lower()
                    if auth == "y":
                        shutil.rmtree(dbPath+"/MMI")
                        shutil.rmtree(dbPath)
                        os.mkdir(dbPath)
                        os.mkdir(dbPath+"/MMI")
                        for database in databaseList:
                            createDatabase(database)
                        return True
                    elif auth == "n" or "N":
                        return False
                else:
                    os.mkdir(dbPath+"/MMI")
                    for database in databaseList:
                        createDatabase(database)
                    return True
        except Exception as issues:
            print(issues)
        pass

class createDatabaseStructure():
    """ 
    This Class is used to create create all the required database 
    structure and tables needed for the program to function.
    
    It first create database using the postgres as admin, then create requried extension;
    After that it creates schema on that database which we have created.
    """
    def __init__(self, dataBaseName:str):
        """
        This __init__ method is used to initialize the class variables.
        Args:
            dataBaseName (String): Name of the database which has to be created
        """
        self.dataBaseName = dataBaseName
        
    def executeQueryByPostgres(self,query:str):
        """
        Execute qurery on postgres database with the same connection listed on Postgres Config file.
        Args:
            query (String): Postgres supported Query.
        """
        conn = psycopg2.connect(host= host, port=port, database='postgres', user=user, password=password)
        cur = conn.cursor()
        conn.autocommit = True
        cur = cur.execute(query)
        conn.commit()
        conn.close()

    def create(self):
    
        """ Description: Setup all the required database and Extension
        :type self:
        :param self:
    
        :raises:
    
        :rtype:
        
        """
        # self.executeQueryByPostgres(f'drop database if exists '+str(self.dataBaseName)+'')
        # self.executeQueryByPostgres(f'create database '+str(self.dataBaseName)+'')
        # self.executeQueryByPostgres(f'CREATE EXTENSION if not exists postgis;')
        # self.executeQueryByPostgres(f'CREATE EXTENSION if not exists postgis_sfcgal;')
        # executeQuery(f'create schema nds')
        # uploadCSV()
        uploadAttribute()
        time.sleep(2)  # import time
        print('DB Manupulation')
        executeQuery(f'UPDATE nds.link_ as a SET shapecount = b.nodecount-2 from nds.startend_ as b where a.linkid = b.linkid and a.mastertileid = b.tileid')
        executeQuery(f'UPDATE nds.link_  SET shapetype=1 where shapecount >0;')
        executeQuery(f'UPDATE nds.link_  SET shapetype=2 where isexternal=1;')
        # executeQuery(f'alter table nds.intersection_ add column isexternallinkref integer default (0)')
        # executeQuery(f'update  nds.intersection_  a set isexternallinkref = 1 from nds.link_ b  where b.endintersectionid = a.isec_id and b.linkstarttileid != b.linkendtileid')
        # executeQuery(f'alter table nds.intersection_  add column seflag integer')
        # executeQuery(f'update nds.intersection_ a set seflag = 1 from nds.link_ b  where a.isec_id =b.startintersectionid or a.isec_id =b.endintersectionid')
        

#  Method to Create NDS Standard Database
if __name__ == "__main__":
    p= createDatabaseStructure('mmi_nds_classic').create()
    intiDatabase.main()

