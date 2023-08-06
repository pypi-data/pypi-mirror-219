from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *
from mmi_dbMethods.commonFunctions import *
from mmi_dbMethods.routingTileTable import coordWidth

from mmi_constants.rootConstants import *
from mmi_constants.routingConstants import *

from math import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from nds.routing.attribute.FixedRoadAttributeSet import *
from nds.routing.attribute.RoutingAttributeInfo import *

from nds.routing.main.api import RoutingGeoTile, RoutingGeoTileContentMask, RoutingGeoTileHeader, RoutingIdRangeList

from nds.routing.line.RoadGeoLineList import *
from nds.routing.line.RoadGeoLine import *
from nds.routing.link.ShapePointType import *
from nds.routing.link.ShapePointInfo import *
from nds.routing.link.ShapePointList import *
from nds.routing.link.ShapePointInfoList import *
from nds.routing.ref.IntOrExtLinkId import *
from nds.routing.ref.Link2TileRef import *
from nds.routing.ref.Link2TileList import *
from nds.routing.ref.Link2TileRef import *
from nds.routing.ref.ExtTileIdxColl import *
from nds.routing.ref.api import *


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Routing NDS BLOB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# __`getGeoTileHeader`__
def getGeoTileContentMask(hasRouteLinkMapLineReferenceList: bool, hasRoadShapes: bool):
    routingGeoTileContentMaskInstance = RoutingGeoTileContentMask()
    routingGeoTileContentMaskInstance.setHasRouteLinkMapLineReferenceList(
        hasRouteLinkMapLineReferenceList)
    routingGeoTileContentMaskInstance.setHasRoadShapes(hasRoadShapes)
    return routingGeoTileContentMaskInstance


def getGeoTileHeader(routingGeoTileContentMaskInstance):
    """Default : ContentMask, None, None, None, None"""
    routingGeoTileHeaderInstance = RoutingGeoTileHeader()
    routingGeoTileHeaderInstance.setContentMask(
        routingGeoTileContentMaskInstance)
    routingGeoTileHeaderInstance.setRoadGeoLineOffset(0)
    routingGeoTileHeaderInstance.setRoadGeometryLineIdRangeListOffset(0)
    if routingGeoTileContentMaskInstance.getHasRoadShapes() == True:
        routingGeoTileHeaderInstance.setRoadShapesOffset(0)
    else:
        routingGeoTileHeaderInstance.setRoadShapesOffset(0)

    if routingGeoTileContentMaskInstance.getHasRouteLinkMapLineReferenceList() == True:
        routingGeoTileHeaderInstance.setRouteLinkMapLineReferenceListOffset(0)
    return routingGeoTileHeaderInstance
# __`getGeoTileHeader`__

# __`getRoutingIdRangeList`__
def getRouteNumberRange(startFeatureId:int, endFeatureId:int):
    routeNumberRangeInstance = RouteNumberRange()
    if startFeatureId <= MAX_NUM_FEATURES_PER_TILE:
        routeNumberRangeInstance.setStartFeatureId(startFeatureId)
    else:
        raise Exception(
            "startFeatureId is greater than MAX_NUM_FEATURES_PER_TILE")

    if endFeatureId <= MAX_NUM_FEATURES_PER_TILE:
        routeNumberRangeInstance.setEndFeatureId(endFeatureId)
    else:
        raise Exception(
            "endFeatureId is greater than MAX_NUM_FEATURES_PER_TILE")
    return routeNumberRangeInstance


"""routeNumberRangeInstance may be a list of routeNumberRangeInstance"""


def getRoutingIdRangeList(numOfRoutingListElements:int, routeNumberRangeInstance:object):
    routingIdRangeListInstance = RoutingIdRangeList()
    routingIdRangeListInstance.setNumFeatureRanges(numOfRoutingListElements)
    if numOfRoutingListElements != None:
        routingIdRangeListInstance.setFeatureRange(routeNumberRangeInstance)
    return routingIdRangeListInstance
# __`getRoutingIdRangeList`__

# __`Get Shape Point Object`__
def getCoordOffset(lnga, lata, numVertices, refPoints: dict, coordShift: int):
    dxdy = getRefDxDy(lnga, lata, refPoints, coordShift)
    coordOffset = CoordXYOffset(15)
    coordOffset.setDx(dxdy[0])
    coordOffset.setDy(dxdy[1])
    return coordOffset

def getCoordXYOffset(dxdy):
    coord = CoordXYOffset(15)
    coord.setDx(dxdy[0])
    coord.setDy(dxdy[1])
    return coord


def calculateMaxBit(coordOffset: object):
    maxTempList = []
    for _ in coordOffset:
        maxTempList.append(_._numBits_)
    maxBit = max(maxTempList)
    return maxBit


def getCoordDiffXY(coordOffset: list, numVertices: object,  linkid):
    coordXYDiffInstance = CoordXYDiff(numVertices.funcValue(), linkid)
    coordXYDiffInstance.setNumBits(15)
    coordXYDiffInstance.setOffsets(coordOffset)
    return coordXYDiffInstance


def getScaleSubLevelInfo(numOfScaleSubLevel, hasScaleSublevel=False):
    scaleSubLevelInfoInstance = ScaleSublevelInfo()
    scaleSubLevelInfoInstance.setHasScaleSublevel(hasScaleSublevel)
    if not hasScaleSublevel == False:
        scaleSubLevelInfoInstance.setScaleSublevel(numOfScaleSubLevel)
    return scaleSubLevelInfoInstance


def getReferentialDxDy(currentPoint: list, tileCenter, referencePoint: list):
    """Current Point = Point whose new coordinate to find,
        tileCenter is the Center of tile (Previous Origin),
        referencePoint is the previous Coordinate or reference coordinate (new origin)
        >> Use getDxDy function before putting currentPoint and referencePoint
    """
    pos3X, pos3Y = 0, 0
    pos1X = currentPoint[0]
    pos1Y = currentPoint[1]
    pos2X = referencePoint[0]
    pos2Y = referencePoint[1]
    h = pos3X - pos3X
    k = pos3Y - pos3Y
    long, lat = NDS2WGS(tileCenter[1], tileCenter[0])
    h = NP.subtract(lat, pos2X)
    k = NP.subtract(long, pos2Y)
    pos3X = NP.subtract(pos1X, h)
    pos3Y = NP.subtract(pos1Y, k)
    pos3 = [pos3X, pos3Y]
    return pos3


def getNumVertices(numVertices: int, linkid):
        numVerticesInstance = NumVertices(linkid)
        extInstance = ExtNumVertices(linkid)
        if numVertices <= 15:
            numVerticesInstance.setNumVx4(numVertices)
        else:
            numVerticesInstance.setNumVx4(0)
            flag = 1

        if int(numVerticesInstance.getNumVx4()) == 0 and flag == 1 and numVertices > 15 and numVertices <= 254:
                extInstance.setNumVx8(numVertices)
                numVerticesInstance.setExtNumVx(extInstance)
        else:
            extInstance.setNumVx8(255)
            numVerticesInstance.setExtNumVx(extInstance)
            flag=2

        if int(extInstance.getNumVx8()) == 255 and flag == 2 and  numVertices >= 255 and numVertices < 65535:
            extInstance.setNumVx16(numVertices)
            numVerticesInstance.setExtNumVx(extInstance)
        return numVerticesInstance


def getShapePointList(numVerticesInstance:int, coordXYDiffInstance: list):
    
    """ Description
    :type numVerticesInstance:object:
    :param numVerticesInstance:object:

    :type coordXYDiffInstance:list:
    :param coordXYDiffInstance:list:

    :raises:

    :rtype:shapePointListInstance
    """
    shapePointListInstance = ShapePointList()
    shapePointListInstance.setNumVertices(numVerticesInstance)
    shapePointListInstance.setCoord(coordXYDiffInstance)
    return shapePointListInstance

def getCoordXYDiffWithStart(coordwidth:int, numVertices:int, vxPoint, roadShapePointList):
    coordXYDiffWithStart = CoordXYDiffWithStart(coordwidth,numVertices)
    coordXYDiffWithStart.setNumBits(15)
    coordXYDiffWithStart.setV0(vxPoint)
    coordXYDiffWithStart.setOffsets(roadShapePointList)
    return coordXYDiffWithStart

def getExternalLinkId(externalTileIdx, linkid):
    externalLinkIdInstance = ExternalLinkId()
    externalLinkIdInstance.setExtTileIdx(externalTileIdx)
    externalLinkIdInstance.setLinkId(linkid)
    return externalLinkIdInstance

def getLinkIdChoiceObject(isExternal, linkChoice):
    linkIdChoiceInstance = LinkIdChoice(isExternal)
    if isExternal == False:
        linkIdChoiceInstance.setInternalLinkId(linkChoice)
    if isExternal == True:
        linkIdChoiceInstance.setExternalLinkId(linkChoice)
    return linkIdChoiceInstance

def getIntOrExtLinkid(isExternalLinkId, linkIdChoiceInstance):
    intOrExtLinkIdInstance =  IntOrExtLinkId()
    intOrExtLinkIdInstance.setIsExternalLinkId(isExternalLinkId)
    intOrExtLinkIdInstance.setLinkReferenceChoice(linkIdChoiceInstance)
    return intOrExtLinkIdInstance


def getShapePointInfo(shapePointType:enum, scaleSublevel:object, shapePointListInstance:object=False):
    """ Description
    :type shapePointType:enum:
    :param shapePointType:enum:

    :type scaleSublevel:object:
    :param scaleSublevel:object:

    :type shapePointListInstance:object:
    :param shapePointListInstance:object:

    :raises:

    :rtype:shapePointInfoInstance
    """
    shapePointInfoInstance = ShapePointInfo()
    shapePointInfoInstance.setShapePointType(shapePointType)
    if shapePointType == ShapePointType.BASE_LINK_WITH_GEOMETRY:
        shapePointInfoInstance.setShapePoints(shapePointListInstance)
    if shapePointType != ShapePointType.ROUTE_LINK:
        shapePointInfoInstance.setScaleSublevel(scaleSublevel)
    return shapePointInfoInstance


def getShapePointInfoList(numofLinks: int, shapePointInfoInstance: list):
    
    """ Description: shapePointInfoInstance is List of Shape Point Info
    :type numofLinks:int:
    :param numofLinks:int:

    :type shapePointInfoInstance:list:
    :param shapePointInfoInstance:list:

    :raises:

    :rtype:shapePointInfoListInstance
    """
    shapePointInfoListInstance = ShapePointInfoList(numofLinks)
    shapePointInfoListInstance.setShapePointInfo(shapePointInfoInstance)
    return shapePointInfoListInstance
# __`Get Shape Point Object`__


"""May be It can only accept items from the list """


def fixedRoadAttributeSet():
    fixedRoadAttributeSet = RoutingTile(coordWidth)
    fixedRoadAttributeSet.getFixedRoadAttributeSetList()
    return fixedRoadAttributeSet


def getRoutingAttributeInfo(attrSource: enum, param=fixedRoadAttributeSet()):
    routingAttributeInfoInstance = RoutingAttributeInfo(attrSource)
    if attrSource == AttributeSource.INDEXED:
        routingAttributeInfoInstance.setFixedRoadAttributeSetListIndex(param)
    elif attrSource == AttributeSource.EXPLICIT:
        routingAttributeInfoInstance.setFixedAttributes(param)
    else:
        raise Exception("attrSource is not AttributeSource.INDEXED")
    return routingAttributeInfoInstance


def getRoadGeoLine(coordWidth:int, featureLength:int, attrInfo: object, numOfVertices: object, attrSource:enum, ordinalNumber:int, shapes:object, routeLinkFeatureId:object, scaleSublevel:bool):

    """ Description : Call getRoutingAttributeInfo before calling this function 
    :type coordWidth:int:
    :param coordWidth:int:

    :type featureLength:int:
    :param featureLength:int:

    :type attrInfo:object:
    :param attrInfo:object:

    :type numOfVertices:object:
    :param numOfVertices:object:

    :type attrSource:enum:
    :param attrSource:enum:

    :type ordinalNumber:
    :param ordinalNumber:

    :type shapes:
    :param shapes:

    :type routeLinkFeatureId:
    :param routeLinkFeatureId:

    :type scaleSublevel:bool:
    :param scaleSublevel:bool:

    :raises:

    :rtype:
    """
    roadGeoLineInstance = RoadGeoLine(coordWidth)
    roadGeoLineInstance.setLength(featureLength)
    roadGeoLineInstance.setAttrSource(attrSource)
    roadGeoLineInstance.setAttrInfo(attrInfo)
    roadGeoLineInstance.setNumVertices(numOfVertices)
    roadGeoLineInstance.setOrdinalNumber(ordinalNumber)
    roadGeoLineInstance.setShapes(shapes)
    roadGeoLineInstance.setRouteLinkFeatureId(routeLinkFeatureId)
    roadGeoLineInstance.setScaleSublevel(scaleSublevel)
    return roadGeoLineInstance


def getRoutingGeoline(coordWidth:int, numRoadGeoLines:int, roadGeoLineInstance: object):
    roadGeoLineListInstance = RoadGeoLineList(coordWidth)
    if numRoadGeoLines <= MAX_NUM_FEATURES_PER_TILE:
        roadGeoLineListInstance.setNumRoadGeoLines(numRoadGeoLines)
    else:
        raise Exception("numRoadGeoLines is greater than MAX_NUM_FEATURES_PER_TILE")
    roadGeoLineListInstance.setRoadGeoLine(roadGeoLineInstance)
    return roadGeoLineListInstance


def getRoutingGeoTile(coordWidth:int, geoTileHeader:object, numLinks:int, routingIdRangeListInstance:object, roadGeoLineListInstance:object, routeLinkMapLineReferenceList:object, roadShapeInstance:object): 

    """ Description: Object Are of List OF Objects
    :type coordWidth:int:
    :param coordWidth:int:

    :type geoTileHeader:object:
    :param geoTileHeader:object:

    :type numLinks:int:
    :param numLinks:int:

    :type routingIdRangeListInstance:object:
    :param routingIdRangeListInsnumLinks is greater than MAX_NUM_FEATURES_PER_TILEtance:object:

    :type roadGeoLineListInstance:object:
    :param roadGeoLineListInstance:object:

    :type routeLinkMapLineReferenceList:object:
    :param routeLinkMapLineReferenceList:object:

    :type roadShapeInstance:object:
    :param roadShapeInstance:object:

    :raises: numLinks is greater than MAX_NUM_FEATURES_PER_TILE

    :rtype:
    """
    routingGeoTile = RoutingGeoTile(coordWidth)
    routingGeoTile.setHeader(geoTileHeader)
    if numLinks <= MAX_NUM_FEATURES_PER_TILE:
        routingGeoTile.setNumLinks(numLinks)
    else:
        raise Exception("numLinks is greater than MAX_NUM_FEATURES_PER_TILE")
    routingGeoTile.setRoadGeometryLineIdRangeList(routingIdRangeListInstance)
    if routingGeoTile.hasRoadShapes() == True:
        routingGeoTile.setRoadShapes(roadShapeInstance)
    if routingGeoTile.hasRouteLinkMapLineReferenceList() == True:
        routingGeoTile.setRouteLinkMapLineReferenceList(
            routeLinkMapLineReferenceList)
    routingGeoTile.setRoadGeoLine(roadGeoLineListInstance)
    return routingGeoTile

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Routing NDS BLOB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Routing ADAS BLOB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# from dbMethods.commonFunctions import getAttributeLayer
# getAttributeLayer().extend(getAttributeLayer()) 


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Routing NDS BLOB >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def deleteRoutingTileTable(database, TABLE_NAME):
    deleteDbTableRow( database, TABLE_NAME )
    
    