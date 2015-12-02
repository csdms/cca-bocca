#
# This is a file of option parser support routines for more advanced behavior than string append
# in handling arguments to component.
# The aim is to keep reading the code in component.py reasonably clean and limited to reading
# the component class itself.

from cct._err import err, warn

def go_option_callback(option, opt, value, parser):
    """ handler for --go[=portname]. There is an auxiliary value GoPortStatus which is 0
if the user did not apply --go during the current invocation. This needs to get stored
in the permanent data structure eventually. This allows us to differentiate a user specified
go port (-p) and a generated goport prototype --go. The expected values of GoPortStatus are:
0: --go never appeared. If goport is found, came from -p.
1: --go appeared and a default go impl should be generated.
2: [future] --go-done. We used --go before, but future updates if uses list changes
   should be suppressed.
3: [future] --go-delegate=portname[:delegateclass] delegated goport instead of inherited.
"""
    if opt == "--go" or opt == "-g":
        porttype="gov.cca.ports.GoPort"
        if value == None or len(value) < 1 :
            portname="GO"
        else:
            portname=value
        if parser.values.providesPort == None:
            parser.values.providesPort=[]
        if portname[0] == '-':
            err("--go needs an argument. Got another switch.", 2)
        parser.values.providesPort.append(porttype+"@"+portname)
        parser.values.GoPortStatus=1
