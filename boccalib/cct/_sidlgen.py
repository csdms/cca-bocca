# these are the bocca reserved sidl method names.
boccaReservedMethods=[
'boccaReleaseServices',
'boccaSetServices',
'boccaThrowException',
'boccaForceUsePortInclude',
'boccaClearException',
'boccaCheckException',
'checkException'
]


# checkexception is no use in cxx or java or probably python.
componentsidl=dict()
componentsidl['cxx']="""
"""

componentsidl['java']="""
"""

componentsidl['python']="""
"""

componentsidl['c']="""
/*
 * Function to display a message if an exception occurs.
 * @param excpt the exception to be checked.
 * @param msg the message to be printed or added to the exception if fatal is true.
 * @param fatal if an exception occured and fatal is false, msg is printed.
 *              If fatal is true, msg is printed and exit called.
 */
void checkException(in sidl.BaseInterface excpt, in string msg, in bool fatal);
"""

componentsidl['f77']="""
        /*
           Function to display a message if an exception occurs.
           @param excpt the exception to be checked.
           @param msg the message to be printed or added to the exception if fatal is true.
           @param fatal if an exception occured and fatal is false, msg is printed.
                        If fatal is true, msg is printed and exit called.
        */
void checkException(inout sidl.BaseInterface excpt, in string msg, in bool fatal);
"""

componentsidl['f77_31']=componentsidl['f77']

componentsidl['f90']="""
/*
 * Function to display a message if an exception occurs.
 * @param excpt the exception to be checked.
 * @param msg the message to be printed or added to the exception if fatal is true.
 * @param fatal if an exception occured and fatal is false, msg is printed.
 *              If fatal is true, msg is printed and exit called.
 */
void checkException(inout sidl.BaseInterface excpt, in string msg, in bool fatal);



/* Function callable in f90 only to clear the exception.
 * Use the macro form, not this directly. 
 */
void boccaClearException();

/* Function callable in f90 only to create the exception.
 * Use the macro form, not this directly.
 */
void boccaThrowException(in string message);

"""

componentsidl['f03']="""
/*
 * Function to display a message if an exception occurs.
 * @param excpt the exception to be checked.
 * @param msg the message to be printed or added to the exception if fatal is true.
 * @param fatal if an exception occured and fatal is false, msg is printed.
 *              If fatal is true, msg is printed and exit called.
 */
void checkException(inout sidl.BaseInterface excpt, in string msg, in bool fatal);



/* Function callable in f03 only to clear the exception.
 * Use the macro form, not this directly. 
 */
void boccaClearException();

/* Function callable in f03 only to create the exception.
 * Use the macro form, not this directly.
 */
void boccaThrowException(in string message);

"""

# common stuff here, if any.
componentsidl['all']="""
/*
 * Function to provide typical setServices behavior. User can bypass it by editing
 * their setServices to not call this.
 * @param services the services the component receives during the setServices call.
 */
void boccaSetServices(in gov.cca.Services services) throws gov.cca.CCAException;

/*
 * Function to provide typical releaseServices behavior. User can bypass it by editing
 * their releaseServices to not call this.
 * @param services the services the component receives during the releaseServices call.
 */
void boccaReleaseServices(in gov.cca.Services services) throws gov.cca.CCAException;
"""

def getReservedMethods():
    return boccaReservedMethods

def getSidl(lang, indentstr, sidltype, kind='component', usesvalues=[], requires=[], depthstring=""):
    """return the bocca methods block for a component in a given language, each line prefixed with indentstr.
    result is a list, not string."""
    global componentsidl

    # Insert a fake method for forcing the include of dependencies: uses ports and requires symbols
    usesargs = ''
    count = 0
    if kind == 'component':
        for uport in usesvalues:
            usesargs += 'in ' + uport + ' ' + 'dummy'+str(count)+', '
            count+=1
        if (count > 0):
            usesargs = usesargs.rstrip(', ')
            
    if usesargs and requires: reqargs = ', '
    else: reqargs = ''
    if requires:
        for req in requires:
            reqargs += 'in ' + req + ' ' + 'dummy' + str(count) + ', '
            count += 1
        if count: 
            reqargs = reqargs.rstrip(', ')

    result=[]
    
    # open delim
    result.append(indentstr + '//-----------------------------------------------------------------------------')
    result.append(indentstr + '// DO-NOT-DELETE bocca.protected.begin(bocca:' + sidltype + ':boccaPrivateMethods)' )
    result.append(indentstr + '// DO-NOT-EDIT' )
    # get generic bits
    if kind == 'component':
        for i in componentsidl['all'].splitlines():
            result.append(indentstr + i)
        # get language specific bits
        for i in componentsidl[lang].splitlines():
            result.append(indentstr + i)
    # force uses port includes, even if there are none, because there may have
    # been some and then we get now a babel splicer error.
    result.append(indentstr + '/** This function should never be called, but helps babel generate better code. */')
    result.append(indentstr + 'void boccaForceUsePortInclude'+depthstring+'(' + usesargs + reqargs + ');')
    # close delim
    result.append(indentstr + '// DO-NOT-DELETE bocca.protected.end(bocca:' + sidltype + ':boccaPrivateMethods)' )
    result.append(indentstr + '//-----------------------------------------------------------------------------')

    return result
