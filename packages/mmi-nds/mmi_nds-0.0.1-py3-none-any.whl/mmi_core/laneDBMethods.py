from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *
from mmi_dbMethods.commonFunctions import *
from mmi_dbMethods.laneTileTable import *
from mmi_dbMethods.laneGeoTileTable import *
from mmi_dbMethods.laneBoundaryTileTable import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mmi_functions.conversionlib import *
from mmi_dbConnections.postgresConnection import *

def dynamicInsertLaneTiletable():
    TileIds = executeCustomQuery(databaseList[4],routingDbTableNames[0], "SELECT \"{}\" FROM".format("id"))
    for tileID in TileIds:
        """For each tile Insert NDS Data and Road Area Layer which is AttributeLayer"""

        tempexternalTileIdList = executeQueryWithReturn(f'select isexternal from nds.link_ where isexternal = 1 and mastertileid = {tileID} limit 1')
        if not tempexternalTileIdList == []:
            hasExternalTileIdList = True
            if hasExternalTileIdList == True:
                a = executeQueryWithReturn(f'with tab as (select linkstarttileid as tileid from nds.link_ union select linkendtileid  as tileid from nds.link_) select * from tab where tileid !={tileID} group by tileid order by tileid')
                externalTileIdListInstance = sorted([i[0] for i in list(a)])
                numOfExternalTile = len(externalTileIdListInstance)
                finalExternalTileIdList = getExternalTileIdList(numOfExternalTile , externalTileIdListInstance)
        else:
            hasExternalTileIdList = False
    
    # Attribute TypeRef Object to be set in getAttributeMapLis Functions Start
        numOfMaps = 1
        attrTypeRefList = []
        for i in range(numOfMaps):
            numOfAttributeCodes = 1
            referenceType = ReferenceType.ROUTING_LINK_DIRECTED
            attrTypeOffset = 0
            attributeTypeCodeList = []
            for j in range(numOfAttributeCodes):
                typeCode = 1009 # This Should come from DB
                attributeTypeCodeList.append(getAttributeTypeCode(typeCode))
            attrTypeRefList.append(getAttrTypeRef(numOfAttributeCodes, attributeTypeCodeList, referenceType, attrTypeOffset))
    # Attribute TypeRef Object to be set in getAttributeMapLis Functions Ends

    # Attribute Map List

        id = id
        versionId = laneList[0]
        roadAreaLayerVersionId = laneList[1]
        lastConfirmedVersionId = laneList[2]
        roadAreaLayerLastConfirmedVersionId = laneList[3]
        crc32c = laneList[4]
        roadAreaLayerCrc32c = laneList[5]
        # ndsData = #blob

        
        
        
        
        
        
        attrMapInstance= 's'
        attrMapObject = getAttributeMapList(numOfMaps, attrTypeRefList, attrMapInstance)
        roadAreaLayer = finalroadAreaLayer = getAttributeLayer(hasExternalTileIdList, attrMapObject, finalExternalTileIdList) 

