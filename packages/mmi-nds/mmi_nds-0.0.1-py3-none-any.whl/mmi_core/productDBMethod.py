from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *
from mmi_constants.productConstants import *
from mmi_dbMethods.commonFunctions import *

class buildingBlockTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[0]
    
    def insertIntoBuildingBlockTable(database, TABLE_NAME):
        """Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples"""
        buildingBlockId = buildingBlockTableList[0][0]
        buildingBlockName = buildingBlockTableList[0][1]
        buildingBlockType = BuildingBlockType.SHARED_DATA
        buildingBlockDetailedType = buildingBlockTableList[0][3]
        globalBuildingBlockMetadata = buildingBlockTableList[0][4]
        buildingblocktableRow = [(buildingBlockId,	buildingBlockName,	buildingBlockType, buildingBlockDetailedType, globalBuildingBlockMetadata)]
        writeDbTable(buildingblocktableRow, database, TABLE_NAME)
       
        buildingBlockId = buildingBlockTableList[1][0]
        buildingBlockName = buildingBlockTableList[1][1]
        buildingBlockType = BuildingBlockType.ROUTING
        buildingBlockDetailedType = buildingBlockTableList[1][3]
        globalBuildingBlockMetadata = buildingBlockTableList[1][4]
        buildingblocktableRow = [(buildingBlockId,	buildingBlockName,	buildingBlockType, buildingBlockDetailedType, globalBuildingBlockMetadata)]
        writeDbTable(buildingblocktableRow, database, TABLE_NAME)
        
        buildingBlockId = buildingBlockTableList[2][0]
        buildingBlockName = buildingBlockTableList[2][1]
        buildingBlockType = BuildingBlockType.LANE
        buildingBlockDetailedType = buildingBlockTableList[2][3]
        globalBuildingBlockMetadata = buildingBlockTableList[2][4]
        buildingblocktableRow = [(buildingBlockId,	buildingBlockName,	buildingBlockType, buildingBlockDetailedType, globalBuildingBlockMetadata)]
        writeDbTable(buildingblocktableRow, database, TABLE_NAME)
        
        buildingBlockId = buildingBlockTableList[3][0]
        buildingBlockName = buildingBlockTableList[3][1]
        buildingBlockType = BuildingBlockType.LANDMARK
        buildingBlockDetailedType = buildingBlockTableList[3][3]
        globalBuildingBlockMetadata = buildingBlockTableList[3][4]
        buildingblocktableRow = [(buildingBlockId,	buildingBlockName,	buildingBlockType, buildingBlockDetailedType, globalBuildingBlockMetadata)]
        writeDbTable(buildingblocktableRow, database, TABLE_NAME)
        
        buildingBlockId = buildingBlockTableList[4][0]
        buildingBlockName = buildingBlockTableList[4][1]
        buildingBlockType = BuildingBlockType.OBSTACLE
        buildingBlockDetailedType = buildingBlockTableList[4][3]
        globalBuildingBlockMetadata = buildingBlockTableList[4][4]
        buildingblocktableRow = [(buildingBlockId,	buildingBlockName,	buildingBlockType, buildingBlockDetailedType, globalBuildingBlockMetadata)]
        writeDbTable(buildingblocktableRow, database, TABLE_NAME)

    def readBuildingBlockTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteBuildingBlockTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)

class bBlockCompVersionTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[9]
    # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
    
    def insertIntobBlockCompVersionTable(database, TABLE_NAME):
        """Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples"""
        for block in bBlockList: 
            updateRegionId = block[0]
            updateAreaId = block[1]
            buildingBlockId = block[2]
            tableName = block[3]
            columnName = block[4]
            versionId = block[5]
            isDirty = block[6]
            uri = block[7]
            bblockCompVersionTableRows = [(updateRegionId, updateAreaId, buildingBlockId, tableName, columnName,	versionId, isDirty,	uri)]    
            writeDbTable(bblockCompVersionTableRows, database, TABLE_NAME)
            
    def readbBlockCompVersionTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deletebBlockCompVersionTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
class urbuildingBlockVersionTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[8]
    # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
    def insertIntourbuildingBlockVersionTable(database, TABLE_NAME):
        """Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples"""
        for block in urBuildingBlockTableList:
            updateRegionId = block[0]
            updaAreaId = block[1]
            buildingBlockId = block[2]
            versionId = block[3]
            isDirty = block[4]
            isPartialyFielled = block[5]
            checkSumAvailable = block[6]
            encryptionKeyId = block[7]
            buildingBlockMetadata = block[8]
            uri = block[9]
            dataModelVersion = block[10]
            buildingBlockRow = [(updateRegionId, updaAreaId, buildingBlockId, versionId, isDirty, isPartialyFielled, checkSumAvailable, encryptionKeyId, buildingBlockMetadata, uri, dataModelVersion)]
            writeDbTable(buildingBlockRow, database, TABLE_NAME)
        
    def readurBuildingBlockTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteurBuildingBlockTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
class dataModelVersionTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[26]
    def insertIntoDataModelVersionTable(database, TABLE_NAME):
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
        for block in dataModelVersionList:
            dataModelVersionId = block[0]
            dataModelVersion = block[1]
            datascriptVersionName = block[2]
            hasAdaptation = block[3]
            uri = block[4]
            dataModelVersionRow = [(dataModelVersionId, dataModelVersion, datascriptVersionName, hasAdaptation, uri)]
            writeDbTable(dataModelVersionRow, database, TABLE_NAME)

    def readDataModelVersionTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteDataModelVersionTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
           
class updateRegionTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[1]
    def insertIntoUpdateRegionTable(database, TABLE_NAME):
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
        for block in updateRegionTableList:
            updateRegionId = block[0]
            versionId = block[1]
            isDirty = block[2]
            mapDataReleaseDate = block[3]
            releaseMonth = block[4]
            releaseYear = block[5]
            iconeSetId = block[6]
            updateRegionRow = [(updateRegionId, versionId, isDirty, mapDataReleaseDate, releaseMonth, releaseYear, iconeSetId)]
            writeDbTable(updateRegionRow, database, TABLE_NAME)

    def readUpdateRegionTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
    
    def deleteUpdateRegionTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
   
class updateProductNameTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[29]
    def insertIntoUpdateProductNameTable(database, TABLE_NAME):
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
        for block in updateProductNameTableList:
            languageCode = block[0]
            nameString = block[1]
            updateProductNameRow = [(languageCode, nameString)]
            writeDbTable(updateProductNameRow, database, TABLE_NAME)

    def readUpdateProductNameTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteUpdateProductNameTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)

class languageTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[19]
    def insertIntoLanguageTable(database, TABLE_NAME):
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
        for block in languageTableList:
            languageCode = block[0]
            isoCountryCode = block[1]
            isoLanguageCode = block[2]
            isoScriptCode = block[3]
            isTransliterationOf = block[4]
            isDiacriticTransliterationOf = block[5]
            
            langObj = LanguageNames()
            langObj.setLanguageName(None) 
            langObj.setNumNames(0)

            charObj = CharacterChartCodeColl()
            charObj.setCharacterChartCode(None)
            charObj.setNumElements(0)

            languageTableRows = [(languageCode, isoCountryCode, isoLanguageCode, isoScriptCode, isTransliterationOf, isDiacriticTransliterationOf, langObj, charObj)]
            writeDbwithBlob(languageTableRows, database, TABLE_NAME)
    def readLanguageTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
    def deleteLanguageTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)

class tileContentIndexTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[5]

    def insertIntoTileContentIndexTable(database, TABLE_NAME):
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
        for block in tileContentIndexTableList:
            southWestTileId = executeCustomQuery(databaseList[4],routingDbTableNames[0], "SELECT \"{}\" FROM".format("id"))
            for oneId in southWestTileId[0]:
                updateRegionId = block[0]
                updateAreaId = block[1]
                buildingBlockId = block[2]
                levelNumber = block[3]
                sequenceNumber = block[4]
                sId = int(oneId)
                numRows = 1
                numColumns = 2
                tileContentIndexInstance = TileContentIndex(numRows, numColumns)
                tempList = []
                for i in range((numRows * numColumns)): tempList.append((1))
                tileContentIndexInstance.setAvailableTiles(tempList)
                tileContentIndex = tileContentIndexInstance
                """updateRegionId	updateAreaId	buildingBlockId	levelNumber	sequenceNumber	southWestTileId	numRows	numColumns	tileContentIndex"""
                tileContentIndexRow = [(updateRegionId, updateAreaId, buildingBlockId, levelNumber, sequenceNumber, sId, numRows, numColumns, tileContentIndex)]
                writeDbTable(tileContentIndexRow, database, TABLE_NAME)
    
    def deleteTileContentIndexTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
    def readTileContentIndexTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))

class updateRegionViewSetTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[15] 
    
    def insertIntoUpdateRegionViewSetTable(database, TABLE_NAME):
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
        for block in updateRegionViewSetTableList:
            disputantId = block[0]
            updateRegionId = block[1]
            updateRegionViewSetRow = [(disputantId, updateRegionId)]
            writeDbTable(updateRegionViewSetRow, database, TABLE_NAME)
    
    def deleteUpdateRegionViewSetTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
    def readUpdateRegionViewSetTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))

class versionTable:
    database = databaseList[1]
    TABLE_NAME = productDbTableNames[7]
    
    def insertIntoVersionTable(database, TABLE_NAME):
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
        for block in versionTableList:
            versionId = block[0]
            versionName = block[1]
            compilerVersion = block[2]
            compilerConfiguration = block[3]
            creationDateTime = block[4]
            versionRow = [(versionId, versionName, compilerVersion, compilerConfiguration, creationDateTime)]
            writeDbTable(versionRow, database, TABLE_NAME)
    
    def deleteVersionTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
    def readVersionTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
    

if __name__ == '__main__':
    database = databaseList[1]
    buildingBlockTable.deleteBuildingBlockTable(database, buildingBlockTable.TABLE_NAME)
    buildingBlockTable.insertIntoBuildingBlockTable(database, buildingBlockTable.TABLE_NAME)
    
    bBlockCompVersionTable.deletebBlockCompVersionTable(database, bBlockCompVersionTable.TABLE_NAME)
    bBlockCompVersionTable.insertIntobBlockCompVersionTable(database, bBlockCompVersionTable.TABLE_NAME)
    
    urbuildingBlockVersionTable.deleteurBuildingBlockTable(database, urbuildingBlockVersionTable.TABLE_NAME)
    urbuildingBlockVersionTable.insertIntourbuildingBlockVersionTable(database, urbuildingBlockVersionTable.TABLE_NAME)
    
    dataModelVersionTable.deleteDataModelVersionTable(database, dataModelVersionTable.TABLE_NAME)
    dataModelVersionTable.insertIntoDataModelVersionTable(database, dataModelVersionTable.TABLE_NAME)
    
    updateRegionTable.deleteUpdateRegionTable(database, updateRegionTable.TABLE_NAME)
    updateRegionTable.insertIntoUpdateRegionTable(database, updateRegionTable.TABLE_NAME)
    
    updateProductNameTable.deleteUpdateProductNameTable(database, updateProductNameTable.TABLE_NAME)
    updateProductNameTable.insertIntoUpdateProductNameTable(database, updateProductNameTable.TABLE_NAME)
    
    languageTable.deleteLanguageTable(database, languageTable.TABLE_NAME)
    languageTable.insertIntoLanguageTable(database, languageTable.TABLE_NAME)
    
    tileContentIndexTable.deleteTileContentIndexTable(database, tileContentIndexTable.TABLE_NAME)
    tileContentIndexTable.insertIntoTileContentIndexTable(database, tileContentIndexTable.TABLE_NAME, tileContentIndexTable.tileContentIndexInstance)
    
    updateRegionViewSetTable.deleteUpdateRegionViewSetTable(database, updateRegionViewSetTable.TABLE_NAME)
    updateRegionViewSetTable.insertIntoUpdateRegionViewSetTable(database, updateRegionViewSetTable.TABLE_NAME)
    
    versionTable.deleteVersionTable(database, versionTable.TABLE_NAME)
    versionTable.insertIntoVersionTable(database, versionTable.TABLE_NAME)