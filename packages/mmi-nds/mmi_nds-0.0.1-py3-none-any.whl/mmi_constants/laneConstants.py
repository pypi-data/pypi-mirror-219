from mmi_dbMethods.dbconfig import *
from mmi_constants.rootConstants import versionId
from mmi_constants.routingConstants import lastConfirmedVersionId

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

laneList = [versionId, 1, lastConfirmedVersionId, 1, None, None]
