import datetime
# from datetime import datetime
from datetime import date

"""updateRegionId	updateAreaId	buildingBlockId	tableName	columnName	versionId	isDirty	uri bBlockCompVersionTable"""
bBlockList = [
[-1,-1,-1,"bBlockCompVersionTable","" ,1,0,"" ,],
[-1,-1,-1,"buildingBlockRelationTable","" ,1,0,"" ,],
[-1,-1,-1,"buildingBlockTable","" ,1,0,"" ,],
[-1,-1,-1,"colorTable","" ,1,0,"" ,],
[-1,-1,-1,"compatibilityMatrixTable","" ,1,0,"" ,],
[-1,-1,-1,"dataModelVersionTable","" ,1,0,"" ,],
[-1,-1,-1,"disputantDefinitionTable","" ,1,0,"" ,],
[-1,-1,-1,"extCompatibilityMatrixTable","" ,1,0,"" ,],
[-1,-1,-1,"fontTable","" ,1,0,"" ,],
[-1,-1,-1,"ftxCompatibilityMatrixTable","" ,1,0,"" ,],
[-1,-1,-1,"globalGatewayTable","" ,1,0,"" ,],
[-1,-1,-1,"globalTmcGatewayTable","" ,1,0,"" ,],
[-1,-1,-1,"globalTollGatewayTable","" ,1,0,"" ,],
[-1,-1,-1,"iconCollectionNameTable","" ,1,0,"" ,],
[-1,-1,-1,"iconCollectionTable","" ,1,0,"" ,],
[-1,-1,-1,"languageTable","" ,1,0,"" ,],
[-1,-1,-1,"namedObjectXrefTable","" ,1,0,"" ,],
[-1,-1,-1,"productNameTable","" ,1,0,"" ,],
[-1,-1,-1,"textureMapCollectionTable","" ,1,0,"" ,],
[-1,-1,-1,"tileContentIndexTable","" ,1,0,"" ,],
[-1,-1,-1,"tmcLocationTableIdTable","" ,1,0,"" ,],
[-1,-1,-1,"trafficAreaTable","" ,1,0,"" ,],
[-1,-1,-1,"trafficBroadcastCoverageTable","" ,1,0,"" ,],
[-1,-1,-1,"updateAreaNameTable","" ,1,0,"" ,],
[-1,-1,-1,"updateAreaTable","" ,1,0,"" ,],
[-1,-1,-1,"updateRegionNameTable","" ,1,0,"" ,],
[-1,-1,-1,"updateRegionSetNameTable","" ,1,0,"" ,],
[-1,-1,-1,"updateRegionSetTable","" ,1,0,"" ,],
[-1,-1,-1,"updateRegionTable","" ,1,0,"" ,],
[-1,-1,-1,"updateRegionViewSetTable","" ,1,0,"" ,],
[-1,-1,-1,"urBuildingBlockVersionTable","" ,1,0,"" ,],
[-1,-1,-1,"urIconImageTable","" ,1,0,"" ,],
[-1,-1,-1,"urIconSetTable","" ,1,0,"" ,],
[-1,-1,-1,"urIconSpriteTable","" ,1,0,"" ,],
[-1,-1,-1,"urIconTextureMapTable","" ,1,0,"" ,],
[-1,-1,-1,"versionTable","" ,1,0,"" ,],
[-1,-1,-1,"volatileLocationIdTable","" ,1,0,"" ,],
[1,-1,0,"additionalIconRefTable","" ,1,0,"" ,],
[1,-1,0,"addressFormatNameTable","" ,1,0,"" ,],
[1,-1,0,"addressFormatTable","" ,1,0,"" ,],
[1,-1,0,"levelMetadataTable","" ,1,0,"" ,],
[1,-1,0,"parkingAvailProfTable","" ,1,0,"" ,],
[1,-1,0,"regionMetadataTable","" ,1,0,"" ,],
[1,-1,0,"regionParkingAvailProfTable","" ,1,0,"" ,],
[1,-1,0,"regionSpeedProfileTable","" ,1,0,"" ,],
[1,-1,0,"regionTimeZoneTable","" ,1,0,"" ,],
[1,-1,0,"roadNumberClassPrefixTable","" ,1,0,"" ,],
[1,-1,0,"speedProfileTable","" ,1,0,"" ,],
[1,-1,0,"timeZoneNameTable","" ,1,0,"" ,],
[1,-1,0,"timeZoneOlsonIdTable","" ,1,0,"" ,],
[1,-1,0,"timeZoneTable","" ,1,0,"" ,],
[1,-1,2,"frcLevelTable","" ,1,0,"" ,],
[1,-1,2,"roadGeometry3DTileTable","" ,1,0,"" ,],
[1,-1,2,"routingAuxTileTable","" ,1,0,"" ,],
[1,-1,2,"routingTileTable","" ,1,0,"" ,],
[1,-1,2,"signpostAttributeTable","" ,1,0,"" ,],
[1,-1,2,"signpostIconImageTable","" ,1,0,"" ,],
[1,-1,2,"signpostIconSetTable","" ,1,0,"" ,],
[1,-1,2,"signpostIconSpriteTable","" ,1,0,"" ,],
[1,-1,2,"signpostIconTextureMapTable","" ,1,0,"" ,],
[1,-1,2,"signpostIconToLayoutTable","" ,1,0,"" ,],
[1,-1,2,"signpostLayoutTable","" ,1,0,"" ,],
[1,-1,2,"signpostTextLayoutTable","" ,1,0,"" ,],
[1,-1,2,"tollCostTable","" ,1,0,"" ,],
[1,-1,18,"laneTileTable","" ,1,0,"" ,],
[1,-1,18,"laneGeoTileTable","" ,1,0,"" ,],
[1,-1,18,"laneBoundaryTileTable","" ,1,0,"" ,],
[1,-1,18,"publicTransportLaneTileTable","" ,1,0,"" ,],
[1,-1,21,"landmarkSignTileTable","" ,1,0,"" ,],
[1,-1,21,"landmarkPoleTileTable","" ,1,0,"" ,],
[1,-1,21,"landmarkMarkingTileTable","" ,1,0,"" ,],
[1,-1,21,"landmarkTrafficLightTileTable","" ,1,0,"" ,],
[1,-1,21,"landmarkWallTileTable","" ,1,0,"" ,],
[1,-1,21,"landmarkBarrierTileTable","" ,1,0,"" ,],
[1,-1,22,"obstacleTileTable","" ,1,0,"" ,],
[1,-1,22,"verticalEdgeTileTable","" ,1,0,"" ,]
]

"""buildingBlockId	buildingBlockName	buildingBlockType	buildingBlockDetailedType	globalBuildingBlockMetadata"""
buildingBlockTableList = [
    [0, "Shared", 0, None, None],
    [2, "Routing", 2, None, None],
    [18, "Lane", 18, None, None],
    [21, "Landmark", 21, None, None],
    [22, "Obstacle", 22, None, None]
]

"""updateRegionId	updateAreaId	buildingBlockId	versionId	isDirty	isPartiallyFilled	checksumsAvailable	encryptionKeyId	buildingBlockMetadata	uri	dataModelVersionId"""
urBuildingBlockTableList = [
    [1,-1,0,1,0,0,0,None,None,"MMI/SHARED.NDS",1,],
    [1,-1,2,1,0,0,0,None,None,"MMI/ROUTING.NDS",1,],
    [1,-1,18,1,0,0,0,None,None,"MMI/LANE.NDS",1,],
    [1,-1,21,1,0,0,0,None,None,"MMI/LANDMARK.NDS",1,],
    [1,-1,22,1,0,0,0,None,None,"MMI/OBSTACLE.NDS",1,],
]

"""dataModelVersionId	dataModelVersion	datascriptVersionName	hasAdaptation	uri"""
dataModelVersionList = [[1, 20504000, '2.5.4', 0, None]]


year = datetime.date.today().year
month = date.today().month
"""updateRegionId	versionId	isDirty	mapDataReleaseDate	releaseYear	releaseMonth	iconSetId"""
updateRegionTableList = [[1, 1, False, year, year, month, None]]

"""languageCode	nameString"""
updateProductNameTableList = [[1 , "MMI_Database"]]

"""languageCode	isoCountryCode	isoLanguageCode	isoScriptCode	isTransliterationOf	isDiacriticTransliterationOf	languageNames	characterChartCodeColl"""
languageTableList = [[1, "IND", "ENG", "Latin", 0, 0]]

"""updateRegionId	updateAreaId	buildingBlockId	levelNumber	sequenceNumber	southWestTileId	numRows	numColumns	tileContentIndex"""
tileContentIndexTableList = [
    [1,-1,2,13,1],
    [1,-1,18,13,1]
    ]

"""disputantId	updateRegionId"""
updateRegionViewSetTableList = [[0,1]]
"""versionId	versionName	compilerVersion	compilerConfiguration	creationDateTime"""
now = datetime.date.today()
versionTableList = [[1, "2.5.4", "MMI_NDS_Classic_V1.0", "Linux UBU-20", str(now)]]