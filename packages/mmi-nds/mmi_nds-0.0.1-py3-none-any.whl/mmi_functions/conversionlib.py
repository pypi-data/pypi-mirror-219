# Convert WGS84 to NDS
from math import *
import numpy as NP
from mmi_functions.toCSV import *
from decimal import *
from afw.wgs84 import Position as WgsPos
from afw import TileId
import afw
from afw.wgs84 import AABB, Position

# <<<<<<<<<< Start of World Coordinate Type Conversion Functions >>>>>>>>>>>>>>>>>>
def NDS2WGS(x, y):
    """ Description : Convert NDS (long, lat) Coordinates to WGS84 and return the long, lat
    :type x:int
    :param x:int

    :type y:int
    :param y:int

    :raises:

    :rtype: Wgs84 ->  Long, Lat
    """
    long = afw.wgs84.Position.from_nds((afw.nds.Position(x, y))).x
    lat  = afw.wgs84.Position.from_nds((afw.nds.Position(x, y))).y
    return long, lat

def toNds(long:float, lat:float):
    long, lat = float(long), float(lat)
    """Convert WGS84 to NDS Coordinates and return the NDS Coordinates"""
    # ndsLat  = int((float(lat) / 360.0) * (2.0**32.0))
    # ndsLong = int((float(long) / 180.0) * (2.0**31.0))
    ndsLong = afw.wgs84.Position(long, lat).to_nds().x
    ndsLat  = afw.wgs84.Position(long, lat).to_nds().y
    return ndsLong, ndsLat

def WGS2NDS(long:float, lat:float):
    """Convert WGS84 to NDS Coordinates"""
    coord = {}
    # x, y =  toNds(round(float(long),6), round(float(lat), 6))    
    # x, y = afw.wgs84.Position.to_nds(afw.wgs84.Position(float(long), float(lat)))
    # p= Position(float(long), float(lat))
    # x,y = afw.wgs84.Position.to_nds(p)
    x, y =  toNds(long, lat)    
    coord['x'] = x
    coord['y'] = y
    return coord
# <<<<<<<<<< End of World Coordinate Type Conversion Functions >>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<< Start of Morton Code Functions >>>>>>>>>>>>>>>

def filter(value, bitLength):
    comp = bin(value & (2**bitLength - 1))
    return int(comp[2:], 2)

def latitude_isvalid(lat):
    if lat < -90.0 or lat > 90.0:
        return False

    return True

def longitude_isvalid(lng):
    if lng < -180.0 or lng > 180.0:
        return False

    return True

def widen(v, mask):
    ''' widen (create a zero to the left of each bit) a 32bit value to 64 bits
      https://graphics.stanford.edu/~seander/bithacks.html#InterleaveBMN
    '''
    v &= mask
    v |= v << 16
    v &= 0x0000ffff0000ffff
    v |= v << 8
    v &= 0x00ff00ff00ff00ff
    v |= v << 4
    v &= 0x0f0f0f0f0f0f0f0f
    v |= v << 2
    v &= 0x3333333333333333
    v |= v << 1
    v &= 0x5555555555555555

    return v

def unwiden(v):
    ''' unwiden (remove the zero from the left of each bit) a 64bit value to 32 bits
      http://fgiesen.wordpress.com/2009/12/13/decoding-morton-codes/
    '''
    v = int(v)
    v &= 0x5555555555555555
    v ^= v >> 1
    v &= 0x3333333333333333
    v ^= v >> 2
    v &= 0x0f0f0f0f0f0f0f0f
    v ^= v >> 4
    v &= 0x00ff00ff00ff00ff
    v ^= v >> 8
    v &= 0x0000ffff0000ffff
    v ^= v >> 16
    v &= 0x00000000ffffffff

    return v

def encode_morton_code(lat, lng):
    """ This Function is used to encode a longitude and latitude into a Morton Code"""
    lat = float(lat)
    lng = float(lng)
    if not latitude_isvalid(lat) or not longitude_isvalid(lng):
        raise Exception("Invalid longitude/latitude %f %f" % (lng, lat))
    sign_bit_latw = 0x0000000040000000
    sign_bit_lngw = 0x0000000080000000
    sign_latw = -1 if lat < 0 else 1
    sign_lngw = -1 if lng < 0 else 1
    latw = floor(abs(lat)*(2**30/90))
    lngw = floor(abs(lng)*(2**30/90))
    latw = (~latw+1) | sign_bit_latw if sign_latw < 0 else latw
    lngw = (~lngw+1) | sign_bit_lngw if sign_lngw < 0 else lngw
    latw = widen(latw, ((sign_bit_latw << 1) - 1))
    lngw = widen(lngw, ((sign_bit_lngw << 1) - 1))
    mCode: int = lngw | (latw << 1)
    return mCode


def mortonDecode(morton_code: int):
    
    """ Description :This Function is used to decode a Morton Code into a NDS Coordinates (X, Y)
    :type morton_code:int
    :param morton_code:int

    :raises: Exception if the Morton_Code in not valid.

    :rtype: NDS Coordinates : int
    """
    if not morton_isvalid(morton_code):
        raise Exception("Invalid morton code %d" % (morton_code))
    # tempList = []
    # tempList.append(getCompactBit(code))
    # tempList.append(getFunckyBit(getCompactBit(code >> 1)))
    return afw.nds.MortonCode(morton_code).to_nds().x, afw.nds.MortonCode(morton_code).to_nds().y

def morton_isvalid(morton):
    if not isinstance(morton, int) or morton < 0 or morton > 2**63-1:
        return False

    return True

# def getCompactBit(v: int):
#     v &= 0x5555555555555555;
#     v = (v ^ (v >> 1)) & 0x3333333333333333;
#     v = (v ^ (v >> 2)) & 0x0F0F0F0F0F0F0F0F;
#     v = (v ^ (v >> 4)) & 0x00FF00FF00FF00FF;
#     v = (v ^ (v >> 8)) & 0x0000FFFF0000FFFF;
#     v = (v ^ (v >> 16)) & 0x00000000FFFFFFFF;
#     return v

# def getFunckyBit(val:int):		
#     if (val & 0x40000000) != 0 :
#         (val | 0x80000000) 
#     else:
#         val
#     return val
# <<<<<<<<<<<<<< End of Morton Code >>>>>>>>>>>>>>>
def getTileBorderInWgs(tileID):
    """This Function Returns the tile border & Level in WGS84 Format"""
    left, bottom, right, top = 0,0,-1,-1
    level = unpackLevel(tileID)
    unpTile = unpackTile(tileID)
    code = unpTile << (62 - 2 * level)
    left, bottom = mortonDecode(code)
    leftt, bottomm = NDS2WGS(left, bottom) 
    width = getTileWidth(level)
    right = left + width
    top = bottom + width
    right, top = NDS2WGS(right, top)
    """Left, Bottom, Right, Top"""
    tileBorder = [leftt, bottomm, right, top]
    return tileBorder, level

# <<<<<<<<<<<<<< Start of Tile Functions >>>>>>>>>>>>>>>
def getTileNumber(morton_code, lvl):
    """ This function is used to get the tile number from a Morton Code and a level number"""
    count_bits = 2 * lvl + 1;
    morton_bit_count = 63
    move_count = morton_bit_count - count_bits
    return morton_code >> move_count

def getTileId(morton_code:int, lvl:int):
    """ This function returns the tile id from a Morton Code and a level number"""
    tile_number = getTileNumber(morton_code, lvl)
    return tile_number | (0x01 << (16 + lvl));

def unpackLevel(tileId):
    level = 0
    while tileId != 0:
        tileId >>= 1
        level= level
        level += 1
    return level - 17

def getTileWidth(level):
    return 1 << (31 - (level))

def unpackTile(tileId):
    level = unpackLevel(tileId)
    return  ((0xFFFFFFFF >> (31 - 2 * level)) & tileId)

def Point2d(lng, lat):
    point = { 'x': lng, 'y': lat}
    return point

def toVector(point:dict):
    """Converts a point to a vector"""
    return [point['x'], point['y']]

def vectorSubtract(ndsCoord, tileCenter):
    """Subtracts two vectors"""
    # vectorPositon = {}
    subs = NP.subtract(toVector(ndsCoord), toVector(tileCenter))
    # vectorPositon['x'] = ndsCoord['x'] - tileCenter['x']
    # vectorPositon['y'] = ndsCoord['y'] - tileCenter['y']
    return subs

def getTileBorder(tileID):
    left, bottom, right, top = 0,0,-1,-1
    level = unpackLevel(tileID)
    unpTile = unpackTile(tileID)
    code = unpTile << (62 - 2 * level)
    left, bottom = mortonDecode(code)
    width = getTileWidth(level)
    right = left + width
    top = bottom + width
    """Left, Bottom, Right, Top"""
    tileBorder = [left, bottom, right, top]
    return tileBorder

def getTileCenter(tileId:int):
    """ Description : Returns two values, the x and y coordinates of the tile center
    :type tileId:int
    :param tileId:int

    :raises:

    :rtype: Dict -> NDS {X, Y}
    """
    centerCoord = {}
    centerCoord['x'] = afw.TileId(tileId).center().x
    centerCoord['y'] = afw.TileId(tileId).center().y
    return centerCoord

def snap(vectorPoint:list, tileCenter:dict, coordShift:int):
    """Snaps a point to a tile center"""
    pos = WGS2NDS(vectorPoint[0], vectorPoint[1])
    pos1 = vectorSubtract(pos, tileCenter)
    divided = NP.divide(pos1, 1 << coordShift)
    dividedX = floor(divided[0])
    dividedY = floor(divided[1])
    return [dividedX, dividedY]
    
def getDxDy(longitude:float,latitude:float, coordShift:int,levelNum:int):
    """ This function returns the dx and dy values"""
    vectorPoint = toVector(Point2d(longitude, latitude))
    mCode = encode_morton_code(latitude, longitude)
    tileId = getTileId(mCode, levelNum)
    tileCenter = getTileCenter(tileId)
    position = snap(vectorPoint,tileCenter, coordShift)
    return position

def getRefDxDy(longitude:float,latitude:float, refPoint:dict, coordShift:int):
    longitude = float(longitude)
    latitude = float(latitude)
    """ This function returns the dx and dy values"""
    vectorPoint = toVector(Point2d(longitude, latitude))
    position = snap(vectorPoint,refPoint, coordShift)
    return [position[0], position[1]]

def getConnectedTileID(tileid):
    """This function returns the connected tile id of a given tileID"""
    a = TileId(tileid)
    if tileid == 0:
        return 0
    connected = []
    connected.append(a.bottom_neighbour())
    connected.append(a.left_neighbour())
    connected.append(a.right_neighbour())
    connected.append(a.top_neighbour())
    tempConnected = []
    for tile in connected: 
        if TileId.valid(tile) == True: 
            tempConnected.append(TileId.value(tile))
        else:
            raise Exception("Tile is not valid")
    return tempConnected

def validateTileID(tileIDQuery):
    tileIDS = []
    for t in tileIDQuery: tileIDS.append(t[0])
    tempList = []
    for t in tileIDS: 
        if '|' not in t:   tempList.append(int(t)) 
    return tempList

def countNumOfTileForBoundingBox(startlat, startlong, endlat, endlong, level):
    from afw.wgs84 import AABB, Position
    st = Position(startlong, startlat)
    en = Position(endlong, endlat)
    # st = Position(68.1766451354, 7.96553477623)
    # en = Position(97.4025614766, 35.4940095078)
    a = AABB(st, en)
    temp = AABB.num_tile_ids(a, level)
    return temp


    
    
# <<<<<<<<<<<<<< End of Tile Functions >>>>>>>>>>>>>>>
