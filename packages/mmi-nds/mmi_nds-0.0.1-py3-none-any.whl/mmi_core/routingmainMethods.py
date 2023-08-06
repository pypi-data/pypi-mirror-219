from mmi_dbMethods.dbconfig import *
from mmi_dbMethods.modMethods import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mmi_dbMethods.routingAuxTileTable import *
from mmi_dbMethods.routingTileTable import *

from mmi_dbConnections.postgresConnection import *
from mmi_functions.conversionlib import *

import random
from rich.progress import track as t2
from rich.progress import track as t1


def InsertIntoRoutingTile():
    tileIDSs = executeQueryWithReturn('select mastertileid  from nds.intersection_ as a group by mastertileid order by mastertileid')
    tileIDs = []
    for id in tileIDSs:
        tileIDs.append(list(id)[0])
    for tileID in tileIDs:
        checkList = executeQueryWithReturn("with a as (SELECT startintersectionid as sid FROM nds.link_ union (select endintersectionid as sid from nds.link_)) select sid from  a group by sid order by sid")
        checkList = sorted([int(i[0]) for i in checkList])
        finalLinkList = []
        finalSimpleIntersection = []
        fixedAttributeSets = []

    # Global Values Go Here \
        levelNum = 13
        coordShift = 3
        coordXYOffset = 15
        coordWidth = 31 - levelNum - coordShift

        attribs = executeQueryWithReturn(f"select * from nds.uniqueattrib_ order by idxnumber")
        linkrows = executeQueryWithReturn(f'select lat, lng, numlinks, connectedlinks, isec_id, externaltileid FROM nds.intersection_ where seflag=1 and mastertileid = {tileID} order by isec_id') #<SimpleIntersection>
        linkTuple = executeQueryWithReturn(f"SELECT linkid FROM nds.link_ where linkstarttileid = {tileID} and mastertileid = {tileID} group by linkid order by linkid ")
        attribInstance = len(attribs)

    # <<<<<<<<< Attribute for Content Mask Start >>>>>>>>>>>>>>>>>> Returns -> Header Object
        if linkrows != None or linkrows != []:
            hasSimpleIntersection = True
        else:
            hasSimpleIntersection = False

        if attribs != None or attribs != []:
            hasFixedRoadAttributeSetList = True
        else:
            hasFixedRoadAttributeSetList = False
        
        if linkTuple != [] or linkTuple != None:
            hasLinkList = True
            haslink2TileList = True
        else:
            hasLinkList = False
            haslink2TileList = False
            
        tempexternalTileIdList = executeQueryWithReturn(f'select isexternal from nds.link_ where isexternal = 1 and mastertileid = {tileID} limit 1')
        if not tempexternalTileIdList == []:
            hasExternalTileIdList = True
        else:
            hasExternalTileIdList = False

        routeUpLinkList = False
        routeDownLinkList = False
        linkIdRangeList = False
        simpleIntersectionIdRangeList = False
        attributeMaps = False
        connlist = [hasFixedRoadAttributeSetList, hasSimpleIntersection, hasLinkList, routeUpLinkList, routeDownLinkList, haslink2TileList, linkIdRangeList, simpleIntersectionIdRangeList, attributeMaps, hasExternalTileIdList]
        contentMask = getContentMask(connlist)
        header = getRoutingTileHeader(contentMask)

        # <<<<<< Routing Shared Road Attributes Start >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if hasFixedRoadAttributeSetList == True:
            for attribute in attribs:
                bridge = attribute[0]  
                tunnel = attribute[1]
                motorway = attribute[2]
                functionalRoadClass = attribute[3]
                travelDirection = Direction(attribute[4])
                toll = Direction(attribute[5])
                ferry = attribute[6]
                pluralJunction = attribute[7]
                priorityRoadClass = attribute[8]
                linkType = LinkType(attribute[9])
                controlledAccess = attribute[10]
                serviceArea = attribute[11]
                urban = attribute[12]
                complexIntersection = False
                # Also we can use LinkType.NO_SPECIAL or LinkType(0)
                shareds = [priorityRoadClass, linkType, travelDirection, ferry, tunnel, bridge, toll, controlledAccess, serviceArea]
            # <<<<<< Routing Shared Road Attributes End >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                roadlist = [functionalRoadClass, urban, complexIntersection, pluralJunction, motorway]
                shared = getSharedRoadAttributes(shareds)
                road = getRoutingRoadAttributes(roadlist)
                fixedAttributeSets.append(getFixedRoadAttributeSet(shared, road))
            fixedset = getFixedRoadAttributeSetList(attribInstance, fixedAttributeSets)

    # <<<<<< Routing SimpleIntersection Starts >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if hasSimpleIntersection == True:
            for linkrow in t1(range(len(linkrows)),description=f'Running On Tile ID: {tileID}'):
                linkrow = linkrows[linkrow]
                row = list(linkrow)
                lat = str(row[0])
                lon = str(row[1])
                DxDy = getDxDy(lon, lat, coordShift, levelNum)
                Dx, Dy = DxDy[0], DxDy[1]
                numLinks = row[2]
                connectedLinkList = []
                links: str = row[3]
                links: list = links.split("|")
                connectedTile = row[5]
                connectedTile = connectedTile.split('|')
                for link in range(len(links)):
                    linkid = links[link]
                    connectedLinkTile = int(connectedTile[link])
                    ulinkid = executeQueryWithReturn(f"SELECT uid FROM nds.link_ where linkid = {linkid} and (startintersectionid ={row[4]} or endintersectionid = {row[4]})  ")
                    ulinkid: int = list(ulinkid[0])[0]
                    positiveLinkDirectionChoice = executeQueryWithReturn(f"SELECT startintersectionid, endintersectionid from nds.link_ where uid = {ulinkid}")
                    if positiveLinkDirectionChoice[0][0] == row[4]:
                        positiveLinkDirection = True
                    else:
                        positiveLinkDirection = False

                    if connectedLinkTile == tileID:
                        isExternalLinkRef = False
                        internalRef = getDirectedLinkReference(positiveLinkDirection, int(linkid))
                        linkref1 = getLinkRefereneChoice(isExternalLinkRef, internalRef)
                        connected = getConnectedLinks(isExternalLinkRef, linkref1)
                        connectedLinkList.append(connected)
                    else:
                        tempList = [a for a in tileIDs if a != tileID]
                        tempList = sorted(tempList)
                        idx = tempList.index(connectedLinkTile)
                        
                        isExternalLinkRef = True
                        externalRef = getDirectedLinkReference(positiveLinkDirection, int(linkid))
                        externalLinkReference = getExternalDirectedLinkReference(idx, externalRef)
                        linkref1 = getLinkRefereneChoice(isExternalLinkRef, externalLinkReference)
                        connected = getConnectedLinks(isExternalLinkRef, linkref1)
                        connectedLinkList.append(connected)
                position = getPosition(Dx, Dy, coordXYOffset)
                finalSimpleIntersection.append(getSimpleIntersection(coordWidth, numLinks, position, connectedLinkList))
    
    # <<<<<< Routing LinkList Starts >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if hasLinkList == True:
            for link in linkTuple:
                attrSource = AttributeSource.INDEXED
                fixedAttrIndex = int(executeQueryWithReturn(f"select idxnumber from nds.attribmaster_ where linkid = {link[0]} and mastertileid = {tileID}")[0][0])
                linkAttrInfo = [attrSource, fixedAttrIndex]
                attrInfo = getAttrInfo(linkAttrInfo)
                linkFeature = executeQueryWithReturn(f"SELECT * FROM nds.link_ where linkid =  \'{str(list(link)[0])}\' and mastertileid = {tileID} ")
                linkFeature = [*linkFeature[0]]
                length = int(linkFeature[1]*100) #Temp Changes as to Introduce Coordinate Precision
                avgSpeed = random.randint(60, 65)
                startAngle = linkFeature[4]
                endAngle = linkFeature[5]
                routingAttrSource = AttributeSource.INDEXED
                linkAttr = [length, routingAttrSource,avgSpeed, startAngle, endAngle]
                finalLinkList.append(getAttrList(linkAttr, attrInfo))
    
    # <<<<<< Routing ExternalTileIDList Starts >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if hasExternalTileIdList == True:
            a = executeQueryWithReturn(f'with tab as (select linkstarttileid as tileid from nds.link_ union select linkendtileid  as tileid from nds.link_) select * from tab where tileid !={tileID} group by tileid order by tileid')
            externalTileIdListInstance = sorted([i[0] for i in list(a)])
            numOfExternalTile = len(externalTileIdListInstance)
            finalExternalTileIdList = getExternalTileIdList(numOfExternalTile , externalTileIdListInstance)

    # <<<<<< Routing Link2TileList Starts >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if haslink2TileList == True:
            externalLinks = executeQueryWithReturn(f'select linkid from nds.link_ where mastertileid = {tileID} and isexternal = 1 order by linkid')
            externalLinks = sorted([i[0] for i in list(externalLinks)])
            numOfExternalLink = len(externalLinks)
            tileRef = []
            for extLink in externalLinks:
                numOfTile = executeQueryWithReturn(f"""SELECT tileid FROM nds.linkgeometry_ where linkid = {extLink} and 
                                                   tileid = {tileID} union select linkstarttileid as tileid from nds.link_ where linkid = {extLink} 
                                                   and mastertileid = {tileID} union select linkendtileid as tileid from nds.link_ where linkid = {extLink}
                                                       and mastertileid = {tileID} group by tileid ORDER BY tileid""")
                extTile = sorted([i[0] for i in list(numOfTile)])
                extTile.remove(tileID)
                numOfTile = len(extTile)
                tempMapList = []
                for ind in range(numOfTile):
                    tempMapList.append(ind)
                    externalTileCollectionIndex = getExternalTileIndexCollection(numOfTile,  tempMapList)
                    tileRef.append(getLink2TileReferenceList(externalTileCollectionIndex, extLink))
            link2tileListObject = getLink2TileList(numOfExternalLink, tileRef)

    # <<<<<< Routing - Setup Of all the components >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        numofInt = len(finalSimpleIntersection)
        finalIntersectionList = getSimpleIntersectionList(numofInt, coordWidth, finalSimpleIntersection)
        numOfLinks = len(finalLinkList)
        finalLinkedList = getLinkList(numOfLinks, finalLinkList)
        routingObj = RoutingTile(coordWidth)
        routingObj.setHeader(header)
        if hasFixedRoadAttributeSetList == True:
            routingObj.setFixedRoadAttributeSetList(fixedset)
        
        if hasSimpleIntersection == True:
            routingObj.setSimpleIntersection(finalIntersectionList)
        else:
            raise Exception("Simple Intersection Object Not Initialized")
        
        if linkList == True:
            routingObj.setLinks(finalLinkedList)
        else:
            raise Exception("Link List Object Not Initialized")
        
        if hasExternalTileIdList == True:
            if hasExternalTileIdList != None:
                routingObj.setExternalTileIdList(finalExternalTileIdList)
            else:
                raise Exception("External Tile Id Object can be empty")
        
        if haslink2TileList ==True:
            if link2tileListObject != None:
                routingObj.setLink2TileList(link2tileListObject)
            else:
                raise Exception("Link2Tile Object can be empty")
    
    # <<<<<< Routing - Final Writing Procedure Starts >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        database = databaseList[4]
        TABLE_NAME = routingDbTableNames[0]
        rows = [(tileID, versionId, lastConfirmedVersionId, crc32c, routingObj)]
        insertIntoRoutingTile(rows, database, TABLE_NAME)

def dynamicInsertRoutingAuxTile():
    database = databaseList[4]
    TABLE_NAME = routingDbTableNames[1]
    coordShift = 3
    TileIds = executeCustomQuery(databaseList[4],routingDbTableNames[0], "SELECT \"{}\" FROM".format("id"))
    for id in TileIds:
        Id = int(id[0])
        roadGeoLineInstance = []
        routeLinkMapLineReferenceList = []
        # nds Blob Data Starts
        shapeTypeOfLinks = executeQueryWithReturn(f"SELECT * FROM nds.link_ where mastertileid =\'{Id}\' order by linkid")
        if shapeTypeOfLinks != []:
            hasRoadShape = True
        else:
            hasRoadShape = False

        contenetMask = getGeoTileContentMask(False, hasRoadShape)
        header = getGeoTileHeader(contenetMask)
        routingIdRangeList = getRoutingIdRangeList(0, None)
        numOfLinks = len(executeQueryWithReturn(f"SELECT * FROM nds.link_ where mastertileid = \'{Id}\'  order by linkid"))
        
        if hasRoadShape == True:
            finalShapePointList = [] # set this to getShapePointInfoList
            for i in t2(range(len(shapeTypeOfLinks)), description="Inserting RoutingAuxTile >"):
                if shapeTypeOfLinks[i][7] == 0:
                    shapeType = ShapePointType.BASE_LINK_NO_GEOMETRY
                    scaleSubLevel = getScaleSubLevelInfo(0) # It should come from DB
                    finalShapePointList.append(getShapePointInfo(shapeType, scaleSubLevel ))
                elif shapeTypeOfLinks[i][7] == 1:
                    shapeType = ShapePointType.BASE_LINK_WITH_GEOMETRY
                    scaleSubLevel = getScaleSubLevelInfo(0) # It should come from DB
                    numOfShapePoints = shapeTypeOfLinks[i][8] 
                    if numOfShapePoints > 0:
                        shapePoints = executeQueryWithReturn("select lat, lng, seq, linkid from nds.linkgeometry_ where linkid = {} and mastertileid={} order by seq".format(shapeTypeOfLinks[i][0], Id))
                        coordXYOffset = []
                        rowData = executeQueryWithReturn("SELECT * FROM nds.startend_ where linkid = {} and tileid={}".format(shapeTypeOfLinks[i][0], Id))
                        check =1
                        refCoord = WGS2NDS(rowData[0][4], rowData[0][3])
                        for seq in shapePoints:
                            seq = list(seq)
                            lat = seq[0]
                            lng = seq[1]
                            seqq = seq[2]
                            """roadShapes/shapePointInfo/shapePointInfo[i]/shapePoints/coord/offsets/offsets[j]/dx"""
                            numOfVertices = getNumVertices(numOfShapePoints, shapePoints[0][3])
                            if check == 1 and seqq  == 1:
                                # The Method getCoordOffset will be depricated to only (lng, lat, numOfvertices, refCoord, coordShif)
                                coordXYOffset.append(getCoordOffset(lng, lat, numOfVertices, refCoord, coordShift))
                                check = 2
                            else:
                                tempCoord = executeQueryWithReturn("select lat, lng, seq, linkid from nds.linkgeometry_ where linkid = {} and seq = {} and mastertileid = {} order by seq".format(shapeTypeOfLinks[i][0], seqq, Id))
                                tempCoord = list(tempCoord)
                                lat = tempCoord[0][0]
                                lng = tempCoord[0][1]
                                temprCoord = executeQueryWithReturn("select lat, lng, seq, linkid from nds.linkgeometry_ where linkid = {} and seq = {} and mastertileid = {} order by seq".format(shapeTypeOfLinks[i][0], seqq-1, Id))
                                temprCoord = list(temprCoord)
                                rlat = temprCoord[0][0]
                                rlng = temprCoord[0][1]
                                refCoord = WGS2NDS(rlng, rlat)
                                # The Method getCoordOffset will be depricated to only (lng, lat, numOfvertices, refCoord, coordShif)
                                coordXYOffset.append(getCoordOffset(lng, lat, numOfVertices, refCoord, coordShift))
                        coorObj = getCoordDiffXY(coordXYOffset, numOfVertices, shapePoints[0][3])
                        # print('Running On LinkID: ', shapePoints[0][3], 'ShapePoint Counts: ',numOfShapePoints, 'LenCoordOffset: ', len(coordXYOffset) )
                        shapePointss = getShapePointList(numOfVertices,coorObj)
                    finalShapePointList.append(getShapePointInfo(shapeType, scaleSubLevel, shapePointss))
                elif shapeTypeOfLinks[i][7] == 2:
                    shapeType = ShapePointType.ROUTE_LINK
                    scaleSubLevel = getScaleSubLevelInfo(0) # It should come from DB
                    finalShapePointList.append(getShapePointInfo(shapeType, scaleSubLevel ))
                else:
                    raise Exception("Invalid shape type")
            finalShape = getShapePointInfoList(numOfLinks, finalShapePointList)

# Road GeoLine
        roadGeoLineInstance = []
        linkIDS = executeQueryWithReturn(f"select * from nds.roadgeoline_ where  tileid = \'{Id}\' order by linkid")
        numRoadGeoLines = len(linkIDS)
        for link in linkIDS:
            vlong, vlat = link[4], link[3]
            endLong, endLat = link[6], link[5]
            featureLength = int(link[2]*100) #Temp Changes as to Introduce Coordinate Precision
            # print(f"select idxnumber from nds.attribmaster_ where linkid = {link[0]} and mastertileid = {Id}")
            # fixedAttrIndex = int(executeQueryWithReturn(f"select idxnumber from nds.attribmaster_ where linkid = {link[0]} and mastertileid = {Id}")[0][0])
            fixedAttrIndex = 0
            attrSource = AttributeSource.INDEXED
            linkAttrInfo = [attrSource, fixedAttrIndex]
            attrInfo = getAttrInfo(linkAttrInfo)
            
            roadGeoLineSeq = executeQueryWithReturn(f'SELECT * FROM nds.roadgeoseq_ where linkid = {link[0]} and tileid = {Id} and mastertileid = {link[7]} order by seq')
            NumOfVertices = (len(roadGeoLineSeq) + 2) # for V0 Point
            numOfVertices = getNumVertices(NumOfVertices, link[0] )
            ordinalNumber = 0
            check = 0
            roadGeoLineShapePointList = []
            vxPoint = getCoordXYOffset(getDxDy(vlong, vlat, coordShift, levelNum))
            # print(link[0],'->', Id, roadGeoLineSeq, vxPoint,NumOfVertices )
            if roadGeoLineSeq != []:
                # roadGeoLineSeq.pop()
                for shape in range(len(roadGeoLineSeq)+1):
                    if check == 0:
                        shape = roadGeoLineSeq[shape]
                        oLong, oLat = shape[4], shape[3]
                        roadGeoLineShapePointList.append(getCoordXYOffset(getRefDxDy(shape[4], shape[3], WGS2NDS(vlong, vlat) , coordShift)))
                        check +=1
                    elif check > 0 and check < len(roadGeoLineSeq):
                        shape = roadGeoLineSeq[shape]
                        roadGeoLineShapePointList.append(getCoordXYOffset(getRefDxDy(shape[4], shape[3], WGS2NDS(oLong, oLat) , coordShift)))
                        oLong, oLat = shape[4], shape[3]
                        check +=1
                    else:
                        roadGeoLineShapePointList.append(getCoordXYOffset(getRefDxDy(endLong, endLat, WGS2NDS(oLong, oLat) , coordShift)))
                shapes = getCoordXYDiffWithStart(coordWidth, NumOfVertices, vxPoint, roadGeoLineShapePointList)
            else:
                roadGeoLineShapePointList.append(getCoordXYOffset(getRefDxDy(endLong, endLat, WGS2NDS(vlong, vlat) , coordShift)))
                shapes = getCoordXYDiffWithStart(coordWidth, NumOfVertices, vxPoint, roadGeoLineShapePointList)

            if link[1] != link[7]:
                isExternal  =  True
                externalTileIdList = executeQueryWithReturn(f'select tileid from nds.linkgeometry_ group by tileid order by tileid')
                externalTileIdList = sorted([i[0] for i in list(externalTileIdList)])
                externalTileIdList.remove(Id)
                idx = externalTileIdList.index(link[7])
                linkChoice = getExternalLinkId(idx, link[0])
            else:
                isExternal = False
                linkChoice = link[0]

            linkIdChoiceInstance = getLinkIdChoiceObject(isExternal, linkChoice)
            routeLinkFeatureId = getIntOrExtLinkid(isExternal, linkIdChoiceInstance)
            scaleSublevel = getScaleSubLevelInfo(0)
            roadGeoLine = getRoadGeoLine(coordWidth, featureLength, attrInfo, numOfVertices, attrSource, ordinalNumber, shapes, routeLinkFeatureId, scaleSublevel )
            roadGeoLineInstance.append(roadGeoLine)
        geoLine = getRoutingGeoline(coordWidth, numRoadGeoLines, roadGeoLineInstance)
        
        
        finalRoutingAuxBlob = RoutingGeoTile(coordWidth)
        finalRoutingAuxBlob.setHeader(header)
        if numLinks <= MAX_NUM_FEATURES_PER_TILE:
            finalRoutingAuxBlob.setNumLinks(numOfLinks)
        else:
            raise Exception("numLinks is greater than MAX_NUM_FEATURES_PER_TILE")
        finalRoutingAuxBlob.setRoadGeometryLineIdRangeList(routingIdRangeList)
        if finalRoutingAuxBlob.hasRoadShapes() == True:
            finalRoutingAuxBlob.setRoadShapes(finalShape)
        if finalRoutingAuxBlob.hasRouteLinkMapLineReferenceList() == True:
            finalRoutingAuxBlob.setRouteLinkMapLineReferenceList(routeLinkMapLineReferenceList)
        finalRoutingAuxBlob.setRoadGeoLine(geoLine)


        # NDS Blob Data End
        for block in routingAuxTileTableMeta:
            versionId = 1
            guidanceAttributeLayerVersionId = block[0]
            nameAttributeLayerVersionId = block[1]
            adasAttributeLayerVersionId = block[2]
            volatileLocationLayerVersionId = block[3] 
            truckAttributeLayerVersionId = block[4]
            lastConfirmedVersionId = "NULL"
            guidanceAttributeLayerLastConfirmedVersionId = block[5]
            nameAttributeLayerLastConfirmedVersionId = block[6]
            adasAttributeLayerLastConfirmedVersionId = block[7]
            volatileLocationLayerLastConfirmedVersionId = block[8]
            truckAttributeLayerLastConfirmedVersionId = block[9]
            crc32c = "NULL"
            guidanceAttributeLayerCrc32c = block[10]
            nameAttributeLayerCrc32c = block[11]
            adasAttributeLayerCrc32c = block[12]
            volatileLocationLayerCrc32c = block[13]
            truckAttributeLayerCrc32c = block[14]
            ndsData = finalRoutingAuxBlob
            guidanceAttributeLayer = None
            nameAttributeLayer = None
            adasAttributeLayer = None
            volatileLocationLayer = None
            truckAttributeLayer = None
            rows = [(Id, versionId, guidanceAttributeLayerVersionId, nameAttributeLayerVersionId, adasAttributeLayerVersionId, volatileLocationLayerVersionId, truckAttributeLayerVersionId, lastConfirmedVersionId, guidanceAttributeLayerLastConfirmedVersionId, nameAttributeLayerLastConfirmedVersionId, adasAttributeLayerLastConfirmedVersionId, volatileLocationLayerLastConfirmedVersionId, truckAttributeLayerLastConfirmedVersionId, crc32c, guidanceAttributeLayerCrc32c, nameAttributeLayerCrc32c, adasAttributeLayerCrc32c, volatileLocationLayerCrc32c, truckAttributeLayerCrc32c, ndsData, guidanceAttributeLayer, nameAttributeLayer, adasAttributeLayer, volatileLocationLayer, truckAttributeLayer)]
            # deleteRoutingTileTable(database, TABLE_NAME)
            writeDbwithBlob(rows, database, TABLE_NAME )


if __name__ == "__main__":
    # pass
    # dynamicInsertRoutingTileTable()
    # InsertIntoRoutingTile()
    dynamicInsertRoutingAuxTile()
    