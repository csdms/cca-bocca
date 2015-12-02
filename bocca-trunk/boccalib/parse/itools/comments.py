import re

class Comments:
    '''This class is used for storing all comments in a source file, by line number.'''
    
    def __init__(self):
        self.lines = {}
    
    def addComment(self, commentstr, lineno, startlineno):
        if lineno not in self.lines.keys():
            self.lines[lineno] = []
        self.lines[lineno].append((self.strip_comment(commentstr), startlineno))
        return
    
    def getComments(self):
        ''' 
        Return a dictionary of all comments keyed by line number.
        '''
        return self.lines
    
    def clear(self):
        self.lines.clear()
        
    def __repr__(self):
        s = ''
        skeys = self.lines.keys()
        skeys.sort()
        for line in skeys:
            for c in self.lines[line]:
                s += '%4s: %s' % (str(line),c[0]) 
                if not c[0].endswith('\n'): s+='\n'
        return s
    
        
    def strip_comment(self,c):
        # Remove everything before the beginning and after the end of the comment
        s = c
        m1 = re.search(r'/\*',c)
        m2 = re.search(r'//',c)
        start = 0
        if m1 and m2:
            if m1.start() < m2.start():
                start = m1.start()
            else:
                start = m2.start()
        elif m1:
            start = m1.start()
        elif m2: 
            start = m2.start()
        
        s = c[start:]

        # Strip things after the comment (TODO: this cannot handle multiple comments on the same line)
        m = re.search(r'\*/',s)
        if m: s = s[:m.end()]
        return s
    
    pass