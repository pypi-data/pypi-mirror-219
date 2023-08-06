import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mmi_constants.rootConstants import *
import apsw
import hashlib
# str = ndsTopRootName+loadableServiceIdentifier
# result = hashlib.sha256(str.encode())
# if result.hexdigest() == '3ee6eab79eac44bb2ccf2b6edaccfd06bb4201c21a2cc17a79fd33efd4b7ce2e':


from datascript import *
from nds.all.api import *

from nds.rootdb.api import *
from nds.productdb.api import *
from nds.shareddb.api import *
from nds.routing.main.api import *


# dbPath = '/NDS/Project/Office_UpSdated/nds-classic-python/API/api/python/db'
# dbPath = '/NDS/Project/Office_Updated/nds-classic-python/API/api/python/database'
# dbPaths = '/NDS/Project/Office_Updated/nds-classic-python/API/api/python/database/MMI'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/tile_wise_small_sample_13062023/nds1/'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/two_tile_single_line/nds1/'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/NEW/two_tile_single_line/nds1/'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/Resolved/two_tile_sample_for_nds_writing/nds1/'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/Resolved/New/nds1/'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/Resolved/New/nds2/'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/new Resolved/nds1/'
dbPath = '/home/ce00148022/Documents/TWO_TILE/Resolved/New/ndsfromdbmethod/nds1/'
# dbPath = '/home/ce00148022/Documents/TWO_TILE/NEW/two_tile_sample_for_nds_writing/nds1/'
# dbPath = '/home/ce00148022/Documents/Test_One_Line'
# dbPath = '/home/ce00148022/Documents/One_Tile/nds'
# dbPath = '/home/ce00148022/Documents/TwoTileSample/two_tile_sample_for_nds_writing/nds1/'
# dbPath = '/home/ce00148022/Documents/TestSampleTwoLines/two_connected_road_withShp/nds1'
# dbPath = '/home/ce00148022/Documents/TestSample/single_line_with_shape_points/nds1'
dbPaths = dbPath+'/MMI'

databaseList = [
                RootDatabase, 
                ProductDatabase, 
                SharedDatabase, 
                BmdDatabase, 
                RoutingDatabase, 
                NameDatabase, 
                LaneDatabase, 
                SliDatabase, 
                PoiDatabase, 
                DtmDatabase, 
                OrthoimagesDatabase, 
                ThreeDObjectsDatabase, 
                TiDatabase, 
                JvDatabase, 
                NgDatabase, 
                FtsDatabase, 
                SpeechDatabase, 
                VolatileDataDatabase, 
                MapConfidenceDatabase, 
                AsrDatabase, 
                LandmarkDatabase, 
                ObstacleDatabase 
]

dbNames= [
        'Root', 
        'Product', 
        'Shared', 
        'Bmd', 
        'Routing', 
        'Name', 
        'Lane', 
        'Sli', 
        'Poi', 
        'Dtm', 
        'Orthoimages', 
        'ThreeDObjects', 
        'Ti', 
        'Jv', 
        'Ng', 
        'Fts', 
        'Speech', 
        'VolatileData', 
        'MapConfidence', 
        'Asr', 
        'Landmark', 
        'Obstacle'
]

rootDbTableNames = [
    NdsDatabaseSupplierTable,
    ProductDbTable,
    OverallMetadataTable,
]

strRootDbTableNames = [
    'NdsDatabaseSupplierTable',
    'ProductDbTable',
    'DataModelVersionTable',
    'OverallMetadataTable',
    'ProductTypeMaskValues',
    'ProductRelationMaskValues',
    'ProductNameTable'
]


productDbTableNames = [
                        BuildingBlockTable,
                        UpdateRegionTable,
                        UpdateRegionNameTable,
                        UpdateAreaTable,
                        UpdateAreaNameTable,
                        TileContentIndexTable,
                        TileContentIndex,
                        VersionTable,
                        UrBuildingBlockVersionTable,
                        BBlockCompVersionTable,
                        BuildingBlockRelationTable,
                        GlobalGatewayTable,
                        GlobalTmcGatewayTable,
                        GlobalTollGatewayTable,
                        UpdateRegionSetTable,
                        UpdateRegionViewSetTable,
                        UpdateRegionSetNameTable,
                        ColorTable,
                        FontTable,
                        LanguageTable,
                        DisputantDefinitionTable,
                        LanguageNames,
                        LanguageName,
                        GlobalBuildingBlockMetadata,
                        PoiGlobalMetadata,
                        BmdGlobalMetadata,
                        DataModelVersionTable,
                        ProductTypeMaskValues,
                        ProductRelationMaskValues,
                        ProductNameTable
                        
                        
]

strProductDbTableNames = [
                        'BuildingBlockTable',
                        'UpdateRegionTable',
                        'UpdateRegionNameTable',
                        'UpdateAreaTable',
                        'UpdateAreaNameTable',
                        'TileContentIndexTable',
                        'TileContentIndex',
                        'VersionTable',
                        'UrBuildingBlockVersionTable',
                        'BBlockCompVersionTable',
                        'BuildingBlockRelationTable',
                        'GlobalGatewayTable',
                        'GlobalTmcGatewayTable',
                        'GlobalTollGatewayTable',
                        'UpdateRegionSetTable',
                        'UpdateRegionViewSetTable',
                        'UpdateRegionSetNameTable',
                        'ColorTable',
                        'FontTable',
                        'LanguageTable',
                        'DisputantDefinitionTable',
                        'LanguageNames',
                        'LanguageName',
                        'GlobalBuildingBlockMetadata',
                        'PoiGlobalMetadata',
                        'BmdGlobalMetadata'
]

sharedDbTableNames = [
                        RegionMetadataTable,
                        RegionTimeZoneTable,
                        TimeZoneTable,
                        TimeZoneNameTable,
                        UsedPriorityRoadClasses,
                        AddressFormatTable,
                        AddressFormatNameTable,
                        RoadNumberClassPrefixTable,
                        AdditionalIconRefTable,
                        CharacterChartCodeColl,
                        LevelMetadataTable,
                        ScaleDenominatorList,
                        BuildingBlockMetadata,
                        SpeechMetadata,
                        PrerecordedVoiceMetadata,
                        PhoneticTranscriptionMetadata,
                        BmdMetadata,
                        RoutingMetadata,
                        AttributeTypeAvailability,
                        NameMetadata,
                        OrthoImageMetadata,
                        SliMetadata,
                        FtsMetadata,
                        MixedCaseDescriptionSliList,
                        MixedCaseDescriptionSli,
                        MaximumStringLength,
                        CharacterChangeRulesForLanguage,
                        CharacterChangeRules,
                        CharacterChangeRule,
                        TrafficInformationMetadata,
                        PoiMetadata,
                        RegionSpeedProfileTable,
                        SpeedProfileTable,
                        RegionParkingAvailabilityProfileTable,
                        ParkingAvailabilityProfileTable,
                        Object3DMetadata,
                        JvMetadata,
                        DtmMetadata,
                        DtmLevelMetadata,
                        UsedVehicleTypeInformation,
                        TimeZoneOlsonIdTable,
                        SpeedClassDistributionList,
                        SpeedClassDistribution,
                        LanguageCodes,
                        CoordinateProjection,
                        CharacterChangeRulesList,
]

routingDbTableNames = [
                        RoutingTileTable, 
                    RoutingAuxTileTable, 
                    RoutingTile, 
                    RoutingContentMask, 
                    RoutingTileHeader, 
                    RoutingGeoTile, 
                    RoutingGeoTileHeader, 
                    RoutingGeoTileContentMask, 
                    RoutingIdRangeList, 
                    RouteNumberRange, 
                    TollCostTable, 
                    FrcLevelTable
]

strRoutingDbTableNames = [  'RoutingTileTable', 
                            'RoutingAuxTileTable', 
                            'RoutingTile', 
                            'RoutingContentMask', 
                            'RoutingTileHeader', 
                            'RoutingGeoTile', 
                            'RoutingGeoTileHeader', 
                            'RoutingGeoTileContentMask', 
                            'RoutingIdRangeList', 
                            'RouteNumberRange', 
                            'TollCostTable', 
                            'FrcLevelTable'
] 

# Connection Methods

def dbConnection(database):
    dbName = database.DATABASE_NAME
    dbName = dbName.replace("Database", "").upper()
    if dbName == "ROOT":
        dbParam = os.path.join(dbPath, dbName+".NDS")
    elif dbName == "SHARED" or dbName == "ROUTING"  or dbName == "LANE" or dbName == "LANDMARK" or dbName == "OBSTACLE":
        dbParam = os.path.join(dbPaths, dbName+".NDS")
    else:
        dbParam = os.path.join(dbPath, dbName+".NDS")
    conn = apsw.Connection(dbParam, apsw.SQLITE_OPEN_URI | apsw.SQLITE_OPEN_READWRITE)
    return conn

def createDatabase(database):        
    dbName = database.DATABASE_NAME
    dbName = dbName.replace("Database", "").upper()
    if dbName == "ROOT":
        dbParam = os.path.join(dbPath, dbName+".NDS")
    elif dbName == "SHARED" or dbName == "ROUTING"  or dbName == "LANE" or dbName == "LANDMARK" or dbName == "OBSTACLE":
        dbParam = os.path.join(dbPaths, dbName+".NDS")
    else:
        dbParam = os.path.join(dbPath, dbName+".NDS")
    conn = apsw.Connection(dbParam, apsw.SQLITE_OPEN_URI | apsw.SQLITE_OPEN_READWRITE | apsw.SQLITE_OPEN_CREATE)
    dbObj = database(conn)
    dbObj.createSchema()
    dbObj.close()
