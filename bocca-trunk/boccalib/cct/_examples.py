"""A file full of succinct examples, as a nested dictionary for handing
out to an interactive user as requested.
This is different from the help, which is primarly usage information.
"""
import cct
ex=dict()

## known verbs
for i in cct.action_menu:
    ex[i]=dict()
    for j in cct.menu:
        ex[i][j] = "MISSING examples for " + i + " " +j
del ex['help']

# returns 1 if no examples found or keywords bogus.
def exdispatchArgv(argv):
    if len(argv) == 2:
        return exdispatch("all", "all")
    if len(argv) == 3:
        if argv[2] in cct.action_menu:
            return exdispatch(argv[2], "all")
        if argv[2] in cct.menu:
            return exdispatch("all",argv[2])
        print argv[2], " is not in actions or subjects"
	return 1
    if argv[2] in cct.action_menu and argv[3] in cct.menu:
        return exdispatch(argv[2], argv[3])
    print "The combination ", argv[2], argv[3]," is not in the examples"
    return 1

############# print examples based on verb, subject. #############
# special cases are
# bocca example all all
# and by example:
# bocca example create all
# bocca example all component
#
def exdispatch(verb, subject):
    print "dispatch " , verb, subject
    if verb == "all" and subject == "all":
        for v in ex:
            print "## ", v, "examples:"
            for e in ex[v]:
                print "# ", v,  e, ":"
                print ex[v][e]
        return 0
    if subject == "all":
        if ex.has_key(verb):
            print "## ", verb, "examples:"
            for e in ex[verb]:
                print "# ", verb, e, ":"
                print ex[verb][e]
        else:
            print "no examples for unknown verb: ", verb
            return 1
        return 0
    if verb == "all":
        print "## ", subject, "examples:"
        count = 0
        for v in ex:
            if ex[v].has_key(subject):
                print "# ", v, subject, ":"
                print ex[v][subject]
                count=1
        if count == 0:
            print "no examples for unknown subject: ", subject
            return 1
        return 0
    
    print "# ", verb, subject, ":"
    if ex.has_key(verb) and ex[verb].has_key(subject):
        print ex[verb][subject]
    else:
        print "Unknown command", verb,  " " , subject, " or Missing Examples"
        return 1
    return 0

# data:

### examples grouped by subject, not verb
## PORT
# create
ex['create']['port'] = """Examples of create port:
	bocca create port mypkg.MyPort
To derive one port from another interface or port:
	bocca create port mypkg.MyPort --extends=mypkg.SomeInterface
	bocca create port mypkg.MyPort -e=mypkg.SomeInterface
To specify which language bindings get generated for the 
port, instead of the project default set:
	bocca create port mypkg.MyPort --languages="c,f77"
	bocca create port mypkg.MyPort -l="c,f77"
Shortcut examples:
If your project only one package, you may omit mypkg
	bocca create port MyPort
	bocca create port MyPort -e SomeInterface
"""

# rename
ex['rename']['port'] = """Examples of port rename:
	bocca rename port MyPort MyPort2
"""

## COMPONENT
ex['create']['component'] = """Examples of create component:
Making a no-ports component:
	bocca create component mypkg.MyComp
Making a port-providing component with default port instance naming
	bocca create component mypkg.MyComp -p=mypkg.MyPort
	bocca create component mypkg.MyComp --provides=mypkg.MyPort
Making a port-using component with default port instance naming
	bocca create component mypkg.MyDriver -u=mypkg.MyPort
	bocca create component mypkg.MyDriver -uses=mypkg.MyPort
Making a component with explicit port instance naming
	bocca create component mypkg.MyComp -p=mypkg.MyPort,oneProvider
	bocca create component mypkg.MyComp -u=mypkg.MyPort,oneUser
Making a middle-man component
	bocca create component mypkg.Manager -u=mypkg.MyPort -p=mypkg.OtherPort
Making a proxy component
	bocca create component mypkg.ProxyMyPortLogger \
		-u=mypkg.MyPort,realMyPort \
		-p=mypkg.MyPort,interceptorMyPort
Shortcuts:
If the port type is unique, it may be abbreviated, omitting the package name:
	bocca create component mypkg.MyComp -p=MyPort
If there is only one package in the project, the package name may be omitted:
	bocca create component MyComp
"""

