import sys

version = sys.version_info
if version[0] <= 2 and version[1] < 4:
    def reversed(l):
        newlist = list(l)
        newlist.reverse()
        return newlist