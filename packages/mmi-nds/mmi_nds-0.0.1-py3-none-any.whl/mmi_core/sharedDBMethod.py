from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *
from mmi_constants.sharedConstants  import *

class levelMetaDataTable:
    database = databaseList[2]
    TABLE_NAME = sharedDbTableNames[10]
    def insertLevelMetaDataTable(database, TABLE_NAME):
        for item in levelMetaDataList:
            updateAreaId = item[0]
            levelNumber = item[1] 
            buildingBlockId = item[2] 
            layerTypeMask = item[3] 
            coordShiftt = item[4] 
            minScaleDenominator = item[5] 
            maxScaleDenominator = item[6] 
            globalMergeOrder = item[7] 
            isMandatory = item[8] 
            scaleDenominatorList = item[9] 
            levelMetaDataTableList = [(updateAreaId, levelNumber, buildingBlockId, layerTypeMask, coordShiftt, minScaleDenominator, maxScaleDenominator, globalMergeOrder, isMandatory, scaleDenominatorList)]
        # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples
            writeDbTable(levelMetaDataTableList, database, TABLE_NAME)

    def deleteLevelMetaDataTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
    def readMetaDataTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))

class timeZoneTable:
    database = databaseList[2]
    TABLE_NAME = sharedDbTableNames[2]
    def insertTimeZoneTable(database, TABLE_NAME):
        for item in timeZoneDataList:
            timeZoneId = item[0]
            validFromDate = item[1]
            utcOffset = item[2]
            timeZoneNameId = item[3]
            timeZoneAbbreviationNameId = item[4]
            hasDaylightSavingTime = item[5]
            dstUtcOffset = item[6]
            dstNameId = item[7]
            dstAbbreviationNameId = item[8]
            dstStartTimeOfDay = item[9]
            dstStartDayOfWeek = item[10]
            dstStartWeekOfMonth = item[11]
            dstStartMonthOfYear = item[12]
            dstEndTimeOfDay = item[13]
            dstEndDayOfWeek = item[14]
            dstEndWeekOfMonth = item[15]
            dstEndMonthOfYear = item[16]  
            timeZoneList = [(timeZoneId, validFromDate, utcOffset, timeZoneNameId, timeZoneAbbreviationNameId, hasDaylightSavingTime, dstUtcOffset, dstNameId, dstAbbreviationNameId, dstStartTimeOfDay, dstStartDayOfWeek, dstStartWeekOfMonth, dstStartMonthOfYear, dstEndTimeOfDay, dstEndDayOfWeek, dstEndWeekOfMonth, dstEndMonthOfYear)]    
            # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples = item[]
            writeDbTable(timeZoneList, database, TABLE_NAME)

    def deleteTimeZoneTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
    def readTimeZoneTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))

class timeZoneNameTable:
    database = databaseList[2]
    TABLE_NAME = sharedDbTableNames[3]
    def insertTimeZoneNameTable(database, TABLE_NAME):
        for item in timeZoneNameDataList:
            timeZoneNameId = item[0]
            languageCode = item[1]
            timeZoneNameString = item[2]
            timeZoneNameList = [(timeZoneNameId, languageCode, timeZoneNameString)]
            # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples = item[]
            writeDbTable(timeZoneNameList, database, TABLE_NAME)

    def deleteTimeZoneNameTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
    def readTimeZoneNameTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))

class regionTimeZoneTable:
    database = databaseList[2]
    TABLE_NAME = sharedDbTableNames[1]
    def insertRegionTimeZoneTable(database, TABLE_NAME):
        for item in timeZoneNameDataList:
            regionId = item[0]
            timeZoneId = item[1]
            regionTimeZoneList = [(regionId, timeZoneId)]
            # Accept only tuple or Dictionary of tuples with Specific Key or List of Tupples = item[]
            writeDbTable(regionTimeZoneList, database, TABLE_NAME)

    def deleteRegionTimeZoneTable(database, TABLE_NAME):
        deleteDbTableRow(database, TABLE_NAME)
        
    def readRegionTimeZoneTable(database, TABLE_NAME):
        print(readDbTable(database, TABLE_NAME))
        
class regionMetadataTable:
    database = databaseList[2]
    TABLE_NAME = sharedDbTableNames[0]
    def insertRegionMetadataTable(database, TABLE_NAME):
        pass
    

if __name__ == '__main__':
    database = databaseList[2]
    levelMetaDataTable.deleteLevelMetaDataTable(database, levelMetaDataTable.TABLE_NAME)
    levelMetaDataTable.insertLevelMetaDataTable(database, levelMetaDataTable.TABLE_NAME)
    
    timeZoneTable.deleteTimeZoneTable(database, timeZoneTable.TABLE_NAME)
    timeZoneTable.insertTimeZoneTable(database, timeZoneTable.TABLE_NAME)
    
    timeZoneNameTable.deleteTimeZoneNameTable(database, timeZoneNameTable.TABLE_NAME)
    timeZoneNameTable.insertTimeZoneNameTable(database, timeZoneNameTable.TABLE_NAME)
    
    regionTimeZoneTable.deleteRegionTimeZoneTable(database, regionTimeZoneTable.TABLE_NAME)
    regionTimeZoneTable.insertRegionTimeZoneTable(database, regionTimeZoneTable.TABLE_NAME)
    
    # regionMetadataTable.deleteRegionMetadataTable(database, regionMetadataTable.TABLE_NAME)
    # regionMetadataTable.insertRegionMetadataTable(database, regionMetadataTable.TABLE_NAME)


