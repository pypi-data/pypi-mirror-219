import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mmi_dbConnections.postgresConnection  import *

# tileWriter  = open('tileWithBorder.csv', 'w')
# tileWriter.write('tileId, level, left, bottom, right, top\n')


def writer(tileId, tileBorder, level):
    # tileWriter.write(str(tileId) +',' + str(level)+ ',' + str(tileBorder[0]) + ',' + str(tileBorder[1]) + ',' + str(tileBorder[2]) + ',' + str(tileBorder[3]) + '\n')
    executeQueryToAnotherDB("Insert into grid.tileCollection values(\'{}\', {}, {}, {}, {}, {})".format(tileId, level, tileBorder[0], tileBorder[1], tileBorder[2], tileBorder[3]), 'india')
    