from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.commonFunctions import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mmi_functions.conversionlib import *
from mmi_dbConnections.postgresConnection import *
from mmi_constants.rootConstants import *

lat = 28.546103
lon = 77.183957
mortonCode = encode_morton_code(lat,lon )
tileID = getTileId(mortonCode, 13)

# CoordWidth Calculation as per NDS Documentation
levelNum = 13
coordShift = 0
coordWidth = 31 - levelNum - coordShift

# packedTileId = tileID
packedTileId = tileID # Overide tileID
versionId = versionId
lastConfirmedVersionId = "NULL"
crc32c = 'NULL'

# Attribute for Content Mask
fixedRoadAttributeSetList = True
simpleIntersectionList = True
linkList = True
routeUpLinkList = False
routeDownLinkList = False
link2TileList = False
linkIdRangeList = False
simpleIntersectionIdRangeList = False
attributeMaps = False
externalTileIdList = False

connlist = [fixedRoadAttributeSetList, simpleIntersectionList, linkList, routeUpLinkList, routeDownLinkList, 
            link2TileList, linkIdRangeList, simpleIntersectionIdRangeList, attributeMaps, externalTileIdList]

contentMaskAttrList = [fixedRoadAttributeSetList, simpleIntersectionList,
                       linkList, routeUpLinkList, routeDownLinkList, link2TileList, linkIdRangeList, 
                       simpleIntersectionIdRangeList, attributeMaps, externalTileIdList]

# Routing Tile Header Offset List
fixedRoadAttributeSetListOffset = 18
simpleIntersectionOffset = 31
linksOffset = 35
routeUpLinksOffset = 326
routeDownLinksOffset = 0
link2TileListOffset = 0
linkIdRangeListOffset = 0
simplIntIdRangeListOffset = 0
attributeMapsOffset = 0
externalTileIdListOffset = 0

routingTileHeaderAttrList = [fixedRoadAttributeSetListOffset, simpleIntersectionOffset, linksOffset, 
                             routeUpLinksOffset, routeDownLinksOffset, link2TileListOffset, linkIdRangeListOffset, 
                             simplIntIdRangeListOffset, attributeMapsOffset, externalTileIdListOffset]

# Shared Road Attributes
priorityRoadClass = 0
linkType = LinkType.NO_SPECIAL
travelDirection = Direction.IN_BOTH_DIRECTIONS
ferry = False
tunnel = False
bridge = False
toll = Direction.IN_NO_DIRECTION
controlledAccess = Direction.IN_NO_DIRECTION
serviceArea = False

sharedAttrList = [priorityRoadClass, linkType, travelDirection, ferry, tunnel, bridge, toll, controlledAccess, serviceArea]

#  Routing Road Attributes
functionalRoadClass = 3
urban = False 
complexIntersection = False 
pluralJunction = False 
motorway = False 

routingRoadAttrList = [functionalRoadClass, urban, complexIntersection, pluralJunction, motorway]

# FixedRoadAttributeSetList  Attributes
numAttributeSetsInstance = 1

# SimpleIntersectionList Attributes
coordXYOffset = 15
dx = -13441
dy = 1084
positiveLinkDirection = True
linkId = 0
linkRefChoice = False
externalLinkRef = False
isExternalLinkRef = False
coordWidth = coordWidth
numLinks = 1
# numIntersections = 1

simpleIntersectionAttrList = [coordXYOffset, dx, dy, positiveLinkDirection, linkId, linkRefChoice, externalLinkRef, isExternalLinkRef,  coordWidth, numLinks]


"""id	versionId	guidanceAttributeLayerVersionId	nameAttributeLayerVersionId	adasAttributeLayerVersionId	volatileLocationLayerVersionId	truckAttributeLayerVersionId	lastConfirmedVersionId	guidanceAttributeLayerLastConfirmedVersionId	nameAttributeLayerLastConfirmedVersionId	adasAttributeLayerLastConfirmedVersionId	volatileLocationLayerLastConfirmedVersionId	truckAttributeLayerLastConfirmedVersionId	crc32c	guidanceAttributeLayerCrc32c	nameAttributeLayerCrc32c	adasAttributeLayerCrc32c	volatileLocationLayerCrc32c	truckAttributeLayerCrc32c	ndsData	guidanceAttributeLayer	nameAttributeLayer	adasAttributeLayer	volatileLocationLayer	truckAttributeLayer"""
routingAuxTileTableMeta = [[1,1,1,1,1,"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL", "NULL","NULL","NULL","NULL","NULL","NULL"]]



# Link List Attributes
# length = 4000
# attrSource = AttributeSource.INDEXED
# avgSpeed = 50
# startAngle = 3
# endAngle = 35
# routingAttrInfo = AttributeSource.INDEXED
# attrSetList = 0
# fixedAttr = None

# linkAttrList = [length, attrSource, avgSpeed, startAngle, endAngle, routingAttrInfo, attrSetList, fixedAttr]

# # final Links List Attributes
# numLink = 1
