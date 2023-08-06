from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *
from mmi_constants.rootConstants import *

class supplierTable:
    database = databaseList[0]
    TABLE_NAME = rootDbTableNames[0]
    rows = [(ndsDbSupplierId, ndsSupplierName)]
    
    def insertIntoSupplierTable(rows, database, TABLE_NAME):
        writeDbTable(rows, database, TABLE_NAME)
        
    def readSupplierTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteSupplierTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)

class productTable:
    database = databaseList[0]
    TABLE_NAME = rootDbTableNames[1]
    rows = [(productId, ndsDbSupplierId, referencedProductID, referencedNdsDbSupplierId, ndsTopRootName, baseLineMapId, productGroupId, productTypeMask, additionalProductTypeMask, relationMask, versionId, isDirty, productUriReference, loadableServiceIdentifier, copyrightString, dataModelVersion)] 
    def insertIntoProductTable(rows, database, TABLE_NAME):
        """Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples"""
        writeDbTable(rows, database, TABLE_NAME)
        
    def readProductTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteProductTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)

class overallMetadataTable:
    database = databaseList[0]
    TABLE_NAME = rootDbTableNames[2]
    rows = [(dataModelVersion,)]
    def insertIntoOverallMetadataTable(rows, database, TABLE_NAME):
        """Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples"""
        writeDbTable(rows, database, TABLE_NAME)
        
    def readOverallMetadataTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteOverallMetadataTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)

if __name__ == "__main__":
    database = databaseList[0]
    supplierTable.deleteSupplierTable(database, supplierTable.TABLE_NAME)
    supplierTable.insertIntoSupplierTable(supplierTable.rows, database, supplierTable.TABLE_NAME)
    
    productTable.deleteProductTable(database, productTable.TABLE_NAME)
    productTable.insertIntoProductTable(productTable.rows, database, productTable.TABLE_NAME)
    
    overallMetadataTable.deleteOverallMetadataTable(database, overallMetadataTable.TABLE_NAME)
    overallMetadataTable.insertIntoOverallMetadataTable(overallMetadataTable.rows, database, overallMetadataTable.TABLE_NAME)