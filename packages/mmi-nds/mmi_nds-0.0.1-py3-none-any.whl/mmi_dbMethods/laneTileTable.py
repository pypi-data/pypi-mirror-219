from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *
from mmi_dbMethods.commonFunctions import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mmi_constants.laneConstants import *

from nds.lane.main.LaneTileHeader import LaneTileHeader
from nds.lane.main.LaneTileContentMask import LaneTileContentMask
from nds.lane.main.LaneMetadata import LaneMetadata

def getContentMask(contentMask:object, hasExternalTileIdList:bool, hasAttributeMaps:bool):
    laneTileContentMaskInstance = LaneTileContentMask()
    laneTileContentMaskInstance.setHasExternalTileIdList(hasExternalTileIdList)
    laneTileContentMaskInstance.setHasAttributeMaps(hasAttributeMaps)
    return laneTileContentMaskInstance

def getHeader(laneTileContentMaskInstance:object):
    laneTileHeaderInstance = LaneTileHeader()
    laneTileHeaderInstance.setContentMask(laneTileContentMaskInstance)
    if laneTileContentMaskInstance.getHasExternalTileIdList() == True:
        laneTileHeaderInstance.setExternalTileIdListOffset(0)
    if laneTileContentMaskInstance.getHasAttributeMaps() == True:
        laneTileHeaderInstance.setAttributeMapsOffset(0)
    return laneTileHeaderInstance

def getLaneMetaData(baseTileHeight:int, precesion):
    laneMetaDataInstance = LaneMetadata()
    laneMetaDataInstance.setBaseTileHeight(baseTileHeight)
    laneMetaDataInstance.setPrecisionOfTParameter(precesion)
    return laneMetaDataInstance

def getLaneTile(laneTileHeaderInstance:LaneTileHeader, laneMetaDataInstance:LaneMetadata, AttributeMapList:AttributeMapList, externalTileIdList:ExternalTileIdList):
    pass