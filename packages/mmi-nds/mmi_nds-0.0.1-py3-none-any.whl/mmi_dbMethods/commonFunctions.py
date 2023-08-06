from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *

from nds.common.fixedattributes.ScaleSublevelInfo import *
from nds.common.geometry.CoordXYDiff import *
from nds.common.geometry.CoordXYOffset import *
from nds.common.geometry.NumVertices import *
from nds.common.geometry.ExtNumVertices import *
from nds.common.geometry.CoordXYDiffWithStart import *
from nds.common.MAX_NUM_FEATURES_PER_TILE import *
from nds.common.flexattr.attrmaps.api import AttributeMapList, AttributeMap, AttributeTypeRef, AttrMapType
from nds.common.flexattr.attrmaps.AttributeLayer import *
from nds.common.flexattr.attrmaps.FeatureReference import *
from nds.common.flexattr.valuecodes.AttributeValue import *
from nds.common.flexattr.valuecodes.AttributeTypeCode import *
from nds.common.flexattr.attrmaps.ReferenceType import *
from nds.common.flexattr.attrmaps.AttrValueList import *
from nds.common.flexattr.attrmaps.AttrVals4OneFeature import *
from nds.common.flexattr.attrmaps.AttrVals4OneFeatureImplicit import *
from nds.common.flexattr.attrmaps.AttrVals4ManyFeatures import *
from nds.common.flexattr.attrmaps.AttrMapType import *
from nds.common.flexattr.attrmaps.AttributeMapList import *
from nds.common.flexattr.attrmaps.AttributeMap import *
from nds.common.flexattr.attrmaps.AttributeTypeRef import *
from nds.common.fixedattributes.AttributeSource import *

from nds.common.BuildingBlockType import *
from nds.common.fixedattributes.api import *
from nds.common.fixedattributes.Direction import *
from nds.common.fixedattributes.api import *
from nds.common.geometry.api import *
from nds.common.IntOrExtDirectedLinkReference import *
from nds.common.LinkReferenceChoice import *
from nds.common.DirectedLinkReference import *
from nds.common.ExternalDirectedLinkReference import *
from nds.common.fixedattributes.SharedRoadAttributes import *
from nds.common.ExternalTileIdList import *
from nds.common.PackedTileId import *
from nds.common.ExternalTileIdList import *

from nds.common.api import *


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def getAttributeLayer(hasExternalTileIdList : bool, attributeMapList:list, externalTileIdList:object = False):
    
    """ Description : The function returns Guidance Attribute Layer Object for RoutingAux Tile Table guidanceAttributeLayer
    :type hasExternalTileIdList:bool
    :param hasExternalTileIdList:bool

    :type attributeMapList:list
    :param attributeMapList:list of attributeMap from AttributeMapList Function

    :externalTileIdList: getExternalTileIdList() object
    :raises:

    :rtype: Object <AttributeLayer>
    """
    attributeLayerInstance = AttributeLayer()
    if hasExternalTileIdList == True:
        def __init__(self, externalTileIdList):
            self.externalTileIdList = externalTileIdList
            attributeLayerInstance.setHasExternalTileIdList(True)
            attributeLayerInstance.setExternalTileIdList(self.externalTileIdList)
    else:
        attributeLayerInstance.setHasExternalTileIdList(False)
        attributeLayerInstance.setAttributeMapList(attributeMapList)
    
    return attributeLayerInstance

def getExternalTileIdList(numOfTileID:int, tileIDList:list): #intArray
    externalTileIdListInstance = ExternalTileIdList()
    externalTileIdListInstance.setNumTileIds(numOfTileID)
    externalTileIdListInstance.setTileId(tileIDList)
    return externalTileIdListInstance




def getAttributeTypeCode(code):
    attributeTypeCodeInstance = AttributeTypeCode(code)
    return attributeTypeCodeInstance



def getAttrTypeRef(numOfAttributeCode, attributeTypeCodeInstance, referenceType, offset=0):
    """Returns a AttrTypeRef instance with the given parameters."""
    attrTypeRefInstance = AttributeTypeRef()
    attrTypeRefInstance.setNumAttrCodes(numOfAttributeCode)
    attrTypeRefInstance.setAttributeTypeCodes(attributeTypeCodeInstance)
    attrTypeRefInstance.setReferenceType(referenceType)
    attrTypeRefInstance.setAttrTypeOffset(offset)
    return attrTypeRefInstance



def getAttributeMapList(numOfMaps, attrTypeRefInstance, attrMapInstance):
    attributeMapListInstance = AttributeMapList()
    attributeMapListInstance.setNumMaps(numOfMaps)
    attributeMapListInstance.setAttrTypeRef(attrTypeRefInstance)
    attributeMapListInstance.setAttrMap(attrMapInstance)
    return attributeMapListInstance