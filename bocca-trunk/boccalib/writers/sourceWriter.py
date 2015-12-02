# We do not force overriding to be done for splices that may reasonably
# be empty in some languages.

class SourceWriter(object):
    language = "unknown"
    dialect = "unknown"
    commentLineStart = "#error"
    commentLineEnd = ""
    servicesVariable = 'd_services' # from the sidl spec, 'services' is the only bad choice here.
    boccaServicesMethod = "boccaSetServices"
    boccaReleaseMethod = "boccaReleaseServices"
    # fragments surrounded by onceKey are never respliced in normal use. Appear only at create (or add provides port) time
    onceKey = "bocca-default-code. User may edit or delete"
    # fragments surrounded by protKey are strictly bocca's and may always be respliced.
    protKey = "Bocca generated code. bocca.protected"

    def __init__(self, kind='component'):
        self.kind = kind
        self.babelVersion=''

    # Store the Babel version 
    def setBabelVersion(self, babel_version):
        self.babelVersion = babel_version
        return

    # Get the Babel version
    def getBabelVersion(self):
        return self.babelVersion

    # used every time for cca components.
    def getHeaderCode(self, componentSymbol):
        return ''
    
    # used every time any class
    def getImplHeaderCode(self, componentSymbol):
        return ''
    
    # create time only any class
    def getConstructorCode(self, componentSymbol):
        return ''
    
    # create time only any class
    def getDestructorCode(self, componentSymbol):
        return ''

    # create time only component
    def getSetServicesCode(self, componentSymbol):
        return self.commentLineStart + 'ERROR: FIXME getSetServicesCode in language writer ' + self.language + ' for ' + componentSymbol + self.commentLineEnd

    # create time only. component
    def getReleaseMethod(self, componentSymbol):
        return ''

    # at create of goport time only (if --go used)
    def getGoCode(self, componentSymbol, uses=[]):
        return self.commentLineStart + 'ERROR: FIXME getGoCode in language writer ' + self.language + ' for ' + componentSymbol + self.commentLineEnd

    # used every time. component
    def getAuxiliarySetServicesMethod(self, componentSymbol, provides=[], uses=[]):
        return self.commentLineStart + 'ERROR: FIXME getAuxiliarySetServicesMethod in language writer ' + self.language + ' for ' + componentSymbol + self.commentLineEnd

    # used every time. component
    def getAuxiliaryReleaseServicesMethod(self, componentSymbol, provides=[], uses=[]):
        return self.commentLineStart + 'ERROR: FIXME getAuxiliaryReleaseServicesMethod in language writer ' + self.language  + ' for ' + componentSymbol + self.commentLineEnd
    
    # used every time. component w/uses ports.
    def getForceUsePortCode(self, componentSymbol, numitems=0, depthstring=""):
        if numitems == 0:
            return ""
        return self.commentLineStart + 'ERROR: FIXME getForceDepCode in language writer ' + self.language  + ' for ' + componentSymbol + self.commentLineEnd

    # used every time. component.
    def getCheckExceptionMethod(self, componentSymbol):
        return ''
    
    # used to regenerate go prolog block if uses list changes.
    def getGoPrologCode(self, componentSymbol, uses=[]):
        return self.commentLineStart + 'ERROR: FIXME getGoPrologCode in language writer ' + self.language  + ' for ' + componentSymbol + self.commentLineEnd
    
    # used to regenerate go epilog block if uses list changes.
    def getGoEpilogCode(self, componentSymbol, uses=[]):
        return self.commentLineStart + 'ERROR: FIXME getGoEpilogCode in language writer ' + self.language  + ' for ' + componentSymbol + self.commentLineEnd
