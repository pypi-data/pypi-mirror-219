from datetime import date
from mmi_constants.productConstants import languageTableList

levelMetaDataList = [
    [-1,13,18,0,0,1,50000,1,0,None],
    [-1,13,21,0,0,1,50000,1,0,None],
    [-1,13,22,0,0,1,50000,1,0,None],
    [-1,13,2,0,3,1,50000,1,0,None]
]



today = str(date.today())
timeZoneNameId = 1
langCode = languageTableList[0][0]  
timeZoneDataList = [
[1,today,4,timeZoneNameId,None,True,8,None,None,120,0,-1,3,180,0,-1,10]
]


timeZoneNameDataList = [
    [timeZoneNameId,langCode,'IST Indian Standard Time UTC+5:30']
]

regionTimeZoneDataList = [
[1, 1]
]
"""regionId,updateRegionId,regionNamedObjectReference,hasRightHandDriving,hasMetricSystem,hasCommonUTurnRestriction,isoCountryCode,isoSubCountryCode,characterChartCodeColl,usedPriorityRoadClasses,defaultAttrGroupList,languageCodes"""
regionMetaDataList = [
    [1,1,None,1,1,1,"IND","ind"]
]
