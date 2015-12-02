# Code taken from optik (optparse) example
# "Required options" with optparse, version 2:
# extend Option and add a 'required' attribute;
# extend OptionParser to ensure that required options
# are present after parsing.

import optparse, re
from ConfigParser import ConfigParser, DEFAULTSECT

class Option (optparse.Option):
    ATTRS = optparse.Option.ATTRS + ['required']

    def _check_required (self):
        if self.required and not self.takes_value():
            raise OptionError(
                "required flag set for option that doesn't take a value",
                 self)

    # Make sure _check_required() is called from the constructor!
    CHECK_METHODS = optparse.Option.CHECK_METHODS + [_check_required]

    def process (self, opt, value, values, parser):
        optparse.Option.process(self, opt, value, values, parser)
        parser.option_seen[self] = 1

class BoccaHelpFormatter(optparse.IndentedHelpFormatter):
    def format_option_strings (self, option):
        """Return a comma-separated list of option strings & metavariables."""
        if option.takes_value():
            if option.dest:
                metavar = option.metavar or option.dest.upper()
            else:
                metavar = option.metavar
            if metavar:
                short_opts = [sopt + metavar for sopt in option._short_opts]
                long_opts = [lopt + "=" + metavar for lopt in option._long_opts]
            else:
                short_opts = option._short_opts
                long_opts = option._long_opts
        else:
            short_opts = option._short_opts
            long_opts = option._long_opts

        if self.short_first:
            opts = short_opts + long_opts
        else:
            opts = long_opts + short_opts

        return ", ".join(opts)
    pass

class OptionParser (optparse.OptionParser):



    def _init_parsing_state (self):
        self.formatter = BoccaHelpFormatter()
        optparse.OptionParser._init_parsing_state(self)
        self.option_seen = {}


    def check_values (self, values, args):
        for option in self.option_list:
            if (isinstance(option, Option) and
                option.required and
                not self.option_seen.has_key(option)):
                self.error("%s not supplied" % option)
        return (values, args)
    
    def add_option(self, *args, **keywords):
        if (len(args) == 1 and str(args[0].__class__).endswith('Option')):
            o = args[0]
        else:
            o = Option(*args, **keywords)
        return optparse.OptionParser.add_option(self, o)

    def parse_args(self, args=None, values=None):
        newargs = []
        for arg in args:
            if len(arg) > 2 and (arg[0] == '-' and arg[2] == '='):
                newarg = arg[:2] + arg[3:] 
            else:
                newarg = arg
            newargs.append(newarg) 
        
        return optparse.OptionParser.parse_args(self, newargs, values)
    
    def get_option_strings(self):
        return self._long_opt.keys() + self._short_opt.keys()
            

class BoccaConfigParser(ConfigParser):
    
    def __init__(self, defaults=None):
        self._comments = {}
        ConfigParser.__init__(self,defaults)
        pass

    def optionxform(self, optionstr):
        '''Override method in RawConfigParser to not convert option names to lowercase.'''
        return optionstr
        
    def _read(self, fp, fpname):
        """Parse a sectioned setup file.

        The sections in setup file contains a title line at the top,
        indicated by a name in square brackets (`[]'), plus key/value
        options lines, indicated by `name: value' format lines.
        Continuations are represented by an embedded newline then
        leading whitespace.  Blank lines, lines beginning with a '#',
        and just about everything else are ignored.
        """
        cursect = None                            # None, or a dictionary
        cursectComments = None                    # None or a dictionary
        optname = None
        lineno = 0
        comment = ''
        e = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                comment += line
                continue
            if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
                # no leading whitespace
                comment += line
                continue
            # continuation line?
            if line[0].isspace() and cursect is not None and optname:
                value = line.strip()
                if value:
                    cursect[optname] = "%s\n%s" % (cursect[optname], value)
                comment = ''
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                        cursectComments = self._comments[sectname]
                    elif sectname == DEFAULTSECT:
                        cursect = self._defaults
                        cursectComments = {}
                    else:
                        cursect = {'__name__': sectname}
                        cursectComments = {'__name__': sectname,'__comment__': comment}
                        self._sections[sectname] = cursect
                        self._comments[sectname] = cursectComments
                        comment = ''
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                elif cursect is None:
                    raise MissingSectionHeaderError(fpname, lineno, `line`)
                # an option line?
                else:
                    mo = self.OPTCRE.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if vi in ('=', ':') and ';' in optval:
                            # ';' is a comment delimiter only if it follows
                            # a spacing character
                            pos = optval.find(';')
                            if pos != -1 and optval[pos-1].isspace():
                                optval = optval[:pos]
                        optval = optval.strip()
                        # allow empty values
                        if optval == '""':
                            optval = ''
                        optname = self.optionxform(optname.rstrip())
                        cursect[optname] = optval
                        if comment: cursectComments[optname] = comment
                        comment = ''
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = ParsingError(fpname)
                        e.append(lineno, `line`)
                comment = ''
        # if any parsing errors occurred, raise an exception
        if e:
            raise e

    def write(self, fp):
        """Write an .ini-format representation of the configuration state, 
sorting by keys in named sections. Sorting is added to keep users of version controlled
defaults files happier during merge."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        snames = self.sections()
        snames.sort()
        for section in snames:
            fp.write("[%s]\n" % section)
            skeys = self.options(section)
            skeys.sort()
            for key in skeys:
                if key != "__name__":
                    if section in self._comments.keys() and key in self._comments[section].keys():
                        fp.write(self._comments[section][key])
                    value = self.get(section, key)
                    fp.write("%s = %s\n" %
                             (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")


if __name__ == '__main__':
    parser = OptionParser(option_list=[
       Option("-v", action="count", dest="verbose"),
       Option("-f", "--file", required=1)])
    parser.add_option("-k", "--WAWAWA", required=1)
    try:
       (options, args) = parser.parse_args()
       print "verbose:", options.verbose
       print "file:", options.file
    except:
       pass


    from platform import uname
    from pwd import getpwuid
    from os import getuid
    host=uname()[1]
    user=getpwuid(getuid())[0]
    path="/sumware"
    key=user+"@"+host+"@sym"
    key2=user+"@"+host+"@p.q"
    cp= BoccaConfigParser()
    cp.read('q.defaults')
    cp.add_section('RepositoryPaths')
    cp.set('RepositoryPaths',key, path)
    cp.set('RepositoryPaths',key2, path)
    x=open('example.cfg', 'wb')
    cp.write(x)
    x.close()
