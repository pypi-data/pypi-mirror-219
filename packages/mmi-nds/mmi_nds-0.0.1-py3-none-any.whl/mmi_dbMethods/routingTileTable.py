from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *
from mmi_dbMethods.commonFunctions import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mmi_constants.rootConstants import *
from mmi_constants.routingConstants import *

from nds.routing.main.api import * 
from nds.routing.attribute.api import *
from nds.routing.intersection.api import *
from nds.routing.link.api import *
from nds.routing.ref.api import *
from nds.routing.link.Link import *
from nds.routing.attribute.RoutingAttributeInfo import *  

def getContentMask(contentMaskAttrList:list):
    """Returns a RoutingContentMask instance with the given parameters."""
    contentMaskInstance = RoutingContentMask()
    contentMaskInstance.setHasFixedRoadAttributeSetList(contentMaskAttrList[0])
    contentMaskInstance.setHasSimpleIntersectionList(contentMaskAttrList[1])
    contentMaskInstance.setHasLinkList(contentMaskAttrList[2])
    contentMaskInstance.setHasRouteUpLinkList(contentMaskAttrList[3])
    contentMaskInstance.setHasRouteDownLinkList(contentMaskAttrList[4])
    contentMaskInstance.setHasLinkToTileList(contentMaskAttrList[5])
    contentMaskInstance.setHasLinkIdRangeList(contentMaskAttrList[6])
    contentMaskInstance.setHasSimpleIntersectionIdRangeList(contentMaskAttrList[7])
    contentMaskInstance.setHasAttributeMaps(contentMaskAttrList[8])
    contentMaskInstance.setHasExternalTileIdList(contentMaskAttrList[9])
    return contentMaskInstance

def getRoutingTileHeader(contentMaskInstance:object):
    """Returns a RoutingTileHeader instance with the given parameters."""
    routingTileHeaderInstance = RoutingTileHeader()
    routingTileHeaderInstance.setContentMask(contentMaskInstance)
    routingTileHeaderInstance.setFixedRoadAttributeSetListOffset(0)
    routingTileHeaderInstance.setSimpleIntersectionOffset(0)
    routingTileHeaderInstance.setLinksOffset(0)
    routingTileHeaderInstance.setRouteUpLinksOffset(0)
    routingTileHeaderInstance.setRouteDownLinksOffset(0)
    routingTileHeaderInstance.setLink2TileListOffset(0)
    routingTileHeaderInstance.setLinkIdRangeListOffset(0)
    routingTileHeaderInstance.setSimplIntIdRangeListOffset(0)
    routingTileHeaderInstance.setAttributeMapsOffset(0)
    routingTileHeaderInstance.setExternalTileIdListOffset(0)
    return routingTileHeaderInstance

def getSharedRoadAttributes(sharedAttrList:list):    
    """Returns a SharedRoadAttributes instance with the given parameters."""
    sharedRoadAttributesInstance = SharedRoadAttributes()
    sharedRoadAttributesInstance.setPriorityRoadClass(sharedAttrList[0])
    sharedRoadAttributesInstance.setLinkType(sharedAttrList[1])
    sharedRoadAttributesInstance.setTravelDirection(sharedAttrList[2])
    sharedRoadAttributesInstance.setFerry(sharedAttrList[3])
    sharedRoadAttributesInstance.setTunnel(sharedAttrList[4])
    sharedRoadAttributesInstance.setBridge(sharedAttrList[5])
    sharedRoadAttributesInstance.setToll(sharedAttrList[6])
    sharedRoadAttributesInstance.setControlledAccess(sharedAttrList[7])
    sharedRoadAttributesInstance.setServiceArea(sharedAttrList[8])
    return sharedRoadAttributesInstance

def getRoutingRoadAttributes(routingRoadAttrList):
    """Returns a RoutingRoadAttributes instance with the given parameters."""
    routingRoadAttributesInstance = RoutingRoadAttributes()
    routingRoadAttributesInstance.setFunctionalRoadClass(routingRoadAttrList[0])
    routingRoadAttributesInstance.setUrban(routingRoadAttrList[1])
    routingRoadAttributesInstance.setComplexIntersection(routingRoadAttrList[2])
    routingRoadAttributesInstance.setPluralJunction(routingRoadAttrList[3])
    routingRoadAttributesInstance.setMotorway(routingRoadAttrList[4])
    return routingRoadAttributesInstance

def getFixedRoadAttributeSet(sharedRoadAttributesInstance, routingRoadAttributesInstance):
    """Returns a FixedRoadAttributeSet instance with the given parameters."""
    fixedRoadAttributeSetInstance = FixedRoadAttributeSet()
    fixedRoadAttributeSetInstance.setSharedAttr(sharedRoadAttributesInstance)
    fixedRoadAttributeSetInstance.setRoutingAttr(routingRoadAttributesInstance)
    return fixedRoadAttributeSetInstance

def getFixedRoadAttributeSetList(numAttributeSetsInstance, fixedRoadAttributeSetInstanceList):
    """Returns a FixedRoadAttributeSetList instance with the given parameters."""
    fixedRoadAttributeSetListInstance = FixedRoadAttributeSetList()
    fixedRoadAttributeSetListInstance.setNumAttributeSets(numAttributeSetsInstance)
    fixedRoadAttributeSetListInstance.setAttributeList(fixedRoadAttributeSetInstanceList)
    return fixedRoadAttributeSetListInstance

# @@ A_________________________________________________________________________________________________________________________
"""directedLinkReferenceInstance = internalLinkReferenceInstance"""
def getDirectedLinkReference(positiveLinkDirection, linkId):
    """Returns a DirectedLinkReference instance with the given parameters."""
    directedLinkReferenceInstance = DirectedLinkReference()
    directedLinkReferenceInstance.setPositiveLinkDirection(positiveLinkDirection)
    directedLinkReferenceInstance.setLinkId(linkId)
    internalLinkReferenceInstance = directedLinkReferenceInstance
    return internalLinkReferenceInstance

def getExternalDirectedLinkReference(extTileIdx, tileExternalLinkReference:object):
    """Returns a ExternalDirectedLinkReference instance with the given parameters."""
    externalDirectedLinkReferenceInstance = ExternalDirectedLinkReference()
    externalDirectedLinkReferenceInstance.setExtTileIdx(extTileIdx)
    externalDirectedLinkReferenceInstance.setTileExternalLinkReference(tileExternalLinkReference)
    externalLinkReferenceInstance = externalDirectedLinkReferenceInstance
    return externalLinkReferenceInstance


def getLinkRefereneChoice(isExternalLinkReference:bool, IntOrExtDirectedLinkReference:object):
    """Returns a LinkReferenceChoice instance with the given parameters."""
    linkReferenceChoiceInstance = LinkReferenceChoice(isExternalLinkReference)
    if isExternalLinkReference == False:
        linkReferenceChoiceInstance.setInternalLinkReference(IntOrExtDirectedLinkReference)
    if isExternalLinkReference == True:
        linkReferenceChoiceInstance.setExternalLinkReference(IntOrExtDirectedLinkReference)
    return linkReferenceChoiceInstance

"""getConnecteLinks = IntOrExtDirectedLinkReference"""
def getConnectedLinks(isExternalLinkReference:bool, linkReferenceChoiceInstance:object):
    """Only Provide Single Instace of LinkReferenceChoice or Connected Link Array Index Item"""
    intOrExternalDirectedLinkReference =  IntOrExtDirectedLinkReference()
    intOrExternalDirectedLinkReference.setIsExternalLinkReference(isExternalLinkReference)
    intOrExternalDirectedLinkReference.setLinkReferenceChoice(linkReferenceChoiceInstance)
    # intOrExternalDirectedLinkReference = [intOrExternalDirectedLinkReference]
    return intOrExternalDirectedLinkReference
# @@ A_________________________________________________________________________________________________________________________

# A_________________________________________________________________________________________________________________________
def getPosition(dx:int, dy:int, offset:int):
    """ Description: Returns an object which should be use to make a list of CoordXYOffset instances with the given parameters.
    :type dx:
    :param dx: Referential Position with respect to center (int16)

    :type dy:
    :param dy: Referential Position with respect to center (int16)

    :type offset:
    :param offset: CoordOffset Value (int16)

    :raises: N/A

    :rtype:CoordXYOffset() -> Object
    """
    coord = CoordXYOffset(offset)
    coord.setDx(dx)
    coord.setDy(dy)
    return coord
# B--------------------------------------------------------------------------------------------------------------------------------
def getSimpleIntersection(coordwidth, numofLinks, position, connectedLinksList):
    """ Description: Returns a SimpleIntersection instance with the given parameters.
    :type coordwidth:
    :param coordwidth:

    :type numofLinks:
    :param numofLinks:

    :type position: getPosition() -> Object
    :param position: 

    :type connectedLinksList:
    :param connectedLinksList:

    :raises: N/A

    :rtype: SimpleIntersection() -> Object
    """
    simpleIntersectionInstance = SimpleIntersection(coordwidth)
    simpleIntersectionInstance.setPosition(position)
    simpleIntersectionInstance.setNumLinks(numofLinks)
    simpleIntersectionInstance.setConnectedLinks(connectedLinksList)
    return simpleIntersectionInstance

# A_________________________________________________________________________________________________________________________
def getSimpleIntersectionList(numIntersectionsInstance, coordwidth, simpleIntersectionInstanceList):
    """Returns a SimpleIntersectionList instance with the given parameters."""
    simpleIntersectionListInstance = SimpleIntersectionList(coordwidth)
    simpleIntersectionListInstance.setNumIntersections(numIntersectionsInstance)
    simpleIntersectionListInstance.setSimpleIntersection(simpleIntersectionInstanceList)
    return simpleIntersectionListInstance
# B--------------------------------------------------------------------------------------------------------------------------------

def getAttrInfo(linkAttrInfo, fixedAttributes=False):
    attrInfoIntance = RoutingAttributeInfo(linkAttrInfo[0])
    if linkAttrInfo[0] == AttributeSource.INDEXED:
        attrInfoIntance.setFixedRoadAttributeSetListIndex(linkAttrInfo[1])
    if linkAttrInfo[0] == AttributeSource.EXPLICIT:
        attrInfoIntance.setFixedAttributes(fixedAttributes)  
    return attrInfoIntance

def getAttrList(linkAttrList, attrInfoIntance):
    linkInstance = Link()
    linkInstance.setLength(linkAttrList[0])
    linkInstance.setAttrSource(linkAttrList[1])
    linkInstance.setAttrInfo(attrInfoIntance)
    linkInstance.setAverageSpeed(linkAttrList[2])
    linkInstance.setStartAngle(linkAttrList[3])
    linkInstance.setEndAngle(linkAttrList[4])    
    linkInstance = linkInstance
    return linkInstance

def getLinkList(numLink, linkListInstanceList):
    linkListInstance = LinkList()
    linkListInstance.setNumLinks(numLink)
    linkListInstance.setLink(linkListInstanceList)
    return linkListInstance

# Attribute Map Ends

# <<<<<<<<<<<< Value4Feature >>>>>>>>>>>>>>>>
    
def getAttributeValue(attrTypeCode):
    attrValueInstance = AttributeValue(attrTypeCode)
    return attrValueInstance

def getAttrValueList(attrRefHeader_):
    attrValueList = AttrValueList(attrRefHeader_)
    attrRefHeader_.getAttributeTypeCodes()
    attrValueList.setValues()
    


def getAttrVals4OneFeature(attrValueListInstance:object):
    attrVals4OneFeatureInstance = AttrVals4OneFeature()
    featureReference = FeatureReference()
    attrVals4OneFeatureInstance.setFeature(featureReference)
    attrVals4OneFeatureInstance.setAttrValList(attrValueListInstance)
    return attrVals4OneFeatureInstance


def getAttributeMap(attrRefHeader_, AttributeMapType:enum, numOfEntries:int, AttrVals4Type:list = None):
    """ This Function is recursivly Callable and will return objects of a list to AttributeMapList"""
    attributeMapInstance = AttributeMap(attrRefHeader_)
    attributeMapInstance.setAttrMapType(AttributeMapType)
    attributeMapInstance.setNumEntries(numOfEntries)
    if attributeMapInstance.getAttrMapType() == AttrMapType.VALUES_TO_ONE_FEATURE:
        attributeMapInstance.setValues4OneFeature(AttrVals4Type)
    elif attributeMapInstance.getAttrMapType() == AttrMapType.VALUES_TO_MANY_FEATURES:
        attributeMapInstance.setValues4ManyFeatures(AttrVals4Type)
    elif attributeMapInstance.getAttrMapType() == AttrMapType.VALUES_TO_ALL_FEATURES:
        attributeMapInstance.setValues4AllFeatures(AttrVals4Type)
    else:
        raise Exception("AttributeMapType is not valid")
    return attributeMapInstance
#  <<<<<<<<<<<<<<< AttributeTypeRef >>>>>>>>>>>>>>>>>>>>>>>>>
def getAttributeTypeCodes(typeCode:enum):
    """This Function will have a recursive call for each AttributeTypeCode"""
    attributeTypeCodesInstance = AttributeTypeCode(typeCode)
    return attributeTypeCodesInstance
    
def getAttributeTypeRef(numAttrCodes,attrTypeCodelist:list, referenceType:enum):
    """Use getAttributeTypeCodes function and append to a list which will become attrTypeCodelist"""
    """This Function Should be Recursively Called for Each AttributeTypeRef this will give us a final list"""
    attributeTypeRefInstance = AttributeTypeRef()
    attributeTypeRefInstance.setNumAttrCodes(numAttrCodes)
    """AttributeTypeCode is a list of AttributeTypeCode"""
    attributeTypeRefInstance.setAttributeTypeCodes(attrTypeCodelist)
    attributeTypeRefInstance.setReferenceType(referenceType)
    attributeTypeRefInstance.setAttrTypeOffset(0)
    return attributeTypeRefInstance
#  <<<<<<<<<<<<<<< AttributeTypeRef >>>>>>>>>>>>>>>>>>>>>>>>>

def getAttributeMapList(attrNum, attributeTypeRefInstance:list, attrMapInstance:list):
    """ Description
    :type attrNum:
    :param attrNum: attrNum is equal to the number of links present in the layers

    :type attributeTypeRefInstance:list:
    :param attributeTypeRefInstance:list: Call getAttributeTypeRef function and append to a list which will become attributeTypeRefInstance

    :type attrMapInstance:list:
    :param attrMapInstance:list: Call getAttributeMap function and append to a list which will become attrMapInstance

    :raises:

    :rtype:
    """
    attributeMapListInstance = AttributeMapList()
    attributeMapListInstance.setNumMaps(attrNum)
    attributeMapListInstance.setAttrTypeRef(attributeTypeRefInstance)
    attributeMapListInstance.setAttrMap(attrMapInstance)
    return attributeMapListInstance

# Attribute Map Ends

# LinkedTile ID Starts
def getExternalTileIndexCollection(numOfExternalTileIdx:int, externalTileIdx:list): #Array
    """ Description: Returns the externalTileIndexCollection Instance
    :type numOfExternalTileIdx:int:
    :param numOfExternalTileIdx:int: Number of External Tile Id -> Count

    :type externalTileIdx:list:
    :param externalTileIdx:list: List of External Tile Id indexes.

    :raises:

    :rtype: ExtTileIdxColl() -> Object
    """
    externalTileIndexCollectionInstance = ExtTileIdxColl()
    externalTileIndexCollectionInstance.setNumExtTileIds(numOfExternalTileIdx)
    externalTileIndexCollectionInstance.setExtTileIdx(externalTileIdx)
    return externalTileIndexCollectionInstance

def getLink2TileReferenceList(externalTileIndexCollectionInstance:object, linkId:int):
    link2TileRefInstance = Link2TileRef()
    link2TileRefInstance.setLinkId(linkId)
    link2TileRefInstance.setExtTileColl(externalTileIndexCollectionInstance)
    return link2TileRefInstance
    
def getLink2TileList(numOfLinks:int,link2TileRefInstance:object): #objectArray
    link2TileListInstance = Link2TileList()
    if numOfLinks <= nds.common.MAX_NUM_FEATURES_PER_TILE.MAX_NUM_FEATURES_PER_TILE:
        link2TileListInstance.setNumLinks(numOfLinks)
        link2TileListInstance.setTileRef(link2TileRefInstance)
    else:
        raise Exception("numOfLinks exceeds MAX_NUM_FEATURE_PER_TILE limit")
    return link2TileListInstance
  
# LinkedTile ID Ends

def insertIntoRoutingTile(rows, database, TABLE_NAME):
    conn = dbConnection(database)
    writeDbwithBlob(rows, database, TABLE_NAME )
    
def deleteRoutingTileTable(database, TABLE_NAME):
    deleteDbTableRow( database, TABLE_NAME )