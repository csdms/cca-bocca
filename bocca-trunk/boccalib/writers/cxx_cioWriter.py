from writers.sourceWriter import SourceWriter
from writers.cxxWriter import CxxWriter

def getWriterParameters():
    return (Cxx_cioWriter.language, Cxx_cioWriter.babelVersions, Cxx_cioWriter.dialect)
 
class Cxx_cioWriter(CxxWriter):
    """ This class identical to CxxWriter, except it sets the flag so C printfs get used."""
    language = 'cxx'
    dialect = 'cio'
    usecio=True

    def __init__(self, kind = 'component'):
        CxxWriter.__init__(self, kind)
        usecio=True

