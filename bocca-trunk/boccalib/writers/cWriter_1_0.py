from writers.cWriter import CWriter

def getWriterParameters():
    return (CWriter_1_0.language, CWriter_1_0.babelVersions, CWriter_1_0.dialect)
 
# Only those methods which must differ from 1.1 should be implemented here.
# basically, that will be _hincludes if we ever need to write a header include block,
# which we don't presently.
class CWriter_1_0(CWriter):
    language = 'c'
    dialect = 'standard'
    babelVersions = ['1.0.X']

    def __init__(self, kind = 'component'):
        CWriter.__init__(self, kind)
    
