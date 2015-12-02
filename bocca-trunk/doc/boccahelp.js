var helptext = {};
var shorthelptext = {};

//------------------------------------------------------------
// bocca help create class

shorthelptext["create class"] = "bocca create class [options] pkg.MyClassName";

helptext["create class"] = "bocca help create class\u000D\u000A\
\u000D\u000A\
Usage: create class SIDL_SYMBOL [options]\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -lLANGUAGE, --language=LANGUAGE\u000D\u000A\
                        language for class [project default is cxx]\u000D\u000A\
  -dDIALECT, --dialect=DIALECT\u000D\u000A\
                        language dialect for class [project default is\u000D\u000A\
                        standard]\u000D\u000A\
  -iIMPLEMENTED_SYMBOL, --implements=IMPLEMENTED_SYMBOL\u000D\u000A\
                        a SIDL interface that the class being created\u000D\u000A\
                        implements (optional, can be repeated). Multiple\u000D\u000A\
                        --extends options can be specified. If\u000D\u000A\
                        IMPLEMENTED_SYMBOL is an existing external interface,\u000D\u000A\
                        the file containing its definition must be specified\u000D\u000A\
                        immediately following the the IMPLEMENTED_SYMBOL,\u000D\u000A\
                        e.g., --implements\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, use the \"change class +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command.\u000D\u000A\
  -eEXTENDED_SYMBOL, --extends=EXTENDED_SYMBOL\u000D\u000A\
                        a SIDL class that the class being created or modified\u000D\u000A\
                        extends (optional). Only one --extends option can be\u000D\u000A\
                        specified. If EXTENDED_SYMBOL is an existing external\u000D\u000A\
                        class, the file containing its definition must be\u000D\u000A\
                        specified immediately following the the\u000D\u000A\
                        EXTENDED_SYMBOL, e.g., --extends\u000D\u000A\
                        pkg.SomeClass@/path/to/somefile.sidl (Babel-generated\u000D\u000A\
                        XML files are allowed, as well).To change the location\u000D\u000A\
                        of the SIDL file associated with a class, usethe\u000D\u000A\
                        \"change class +  SIDL_SYMBOL --sourcefile/-s FILENAME\"\u000D\u000A\
                        command.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the class depends (other than through\u000D\u000A\
                        extension or implementation, for example, a symbol\u000D\u000A\
                        used as the type of one of the arguments in a method\u000D\u000A\
                        in the class.If the symbol is not in this project, a\u000D\u000A\
                        SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the class.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified class or\u000D\u000A\
                        several classes, e.g., --import-sidl=pkg.MySolverClass\u000D\u000A\
                        ,pkg.MyMatrixClass@/path/to/file.sidl. If no class is\u000D\u000A\
                        specified (only the SIDL filename is given), all\u000D\u000A\
                        methods from interfaces and classes in the SIDL file\u000D\u000A\
                        are imported into the specified project class.\u000D\u000A\
  --import-impl=IMPLIMPORTS\u000D\u000A\
                        A Babel-generated Impl file from which to import\u000D\u000A\
                        method implementations from the specified class or\u000D\u000A\
                        several classes (with multiple --import-impl options),\u000D\u000A\
                        e.g., --import-\u000D\u000A\
                        impl=\"pkg.MyClass@/path/to/pkg_MyClass/\".\u000D\u000A\
  --exclude-impl-symbols=IMPLEXCLUDES\u000D\u000A\
                        Exclude particular method implementations from\u000D\u000A\
                        importation. If this option is not given, a default\u000D\u000A\
                        set to exclude is read from\u000D\u000A\
                        BOCCA/$PROJECT.defaults:exclude_from_import. e.g.,\u000D\u000A\
                        --exclude-impl-symbols=\"setServices releaseServices\".\u000D\u000A\
                        This option may be repeated. To suppress the default\u000D\u000A\
                        and exclude no symbols, use  --exclude-impl-\u000D\u000A\
                        symbols=None\u000D\u000A\
  --import-impl-exact   All imported method implementations are exactly\u000D\u000A\
                        preserved, ignoring anything newly generated by bocca.\u000D\u000A\
                        Excluded symbols remain excluded. If this option is\u000D\u000A\
                        not given, bocca-generated implementations are\u000D\u000A\
                        appended and the user may need to do manual clean up\u000D\u000A\
                        of the resulting impl code.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        SIDL version of the class in the form X.Y. If no\u000D\u000A\
                        version specification  is given, version '0.0' is\u000D\u000A\
                        used.\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the interfaces and/or classes\u000D\u000A\
                        implemented and/or extended by the new class (or of\u000D\u000A\
                        symbols referenced by those interfaces). Multiple\u000D\u000A\
                        repositories can be used (separated by commas).\u000D\u000A\
                        Alternatively, multiple instances of the -x option can\u000D\u000A\
                        be used to specify multiple repositories paths.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help change class

shorthelptext["change class"] = "bocca change class [options] pkg.MyClassName";

helptext["change class"] = "bocca help change class\u000D\u000A\
\u000D\u000A\
Usage: change class SIDL_SYMBOL [options]\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -iIMPLEMENTED_SYMBOL, --implements=IMPLEMENTED_SYMBOL\u000D\u000A\
                        a SIDL interface that the class being created\u000D\u000A\
                        implements (optional, can be repeated). Multiple\u000D\u000A\
                        --extends options can be specified. If\u000D\u000A\
                        IMPLEMENTED_SYMBOL is an existing external interface,\u000D\u000A\
                        the file containing its definition must be specified\u000D\u000A\
                        immediately following the the IMPLEMENTED_SYMBOL,\u000D\u000A\
                        e.g., --implements\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, use the \"change class +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command.\u000D\u000A\
  -eEXTENDED_SYMBOL, --extends=EXTENDED_SYMBOL\u000D\u000A\
                        a SIDL class that the class being created or modified\u000D\u000A\
                        extends (optional). Only one --extends option can be\u000D\u000A\
                        specified. If EXTENDED_SYMBOL is an existing external\u000D\u000A\
                        class, the file containing its definition must be\u000D\u000A\
                        specified immediately following the the\u000D\u000A\
                        EXTENDED_SYMBOL, e.g., --extends\u000D\u000A\
                        pkg.SomeClass@/path/to/somefile.sidl (Babel-generated\u000D\u000A\
                        XML files are allowed, as well).To change the location\u000D\u000A\
                        of the SIDL file associated with a class, usethe\u000D\u000A\
                        \"change class +  SIDL_SYMBOL --sourcefile/-s FILENAME\"\u000D\u000A\
                        command.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the class depends (other than through\u000D\u000A\
                        extension or implementation, for example, a symbol\u000D\u000A\
                        used as the type of one of the arguments in a method\u000D\u000A\
                        in the class.If the symbol is not in this project, a\u000D\u000A\
                        SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the class.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified class or\u000D\u000A\
                        several classes, e.g., --import-sidl=pkg.MySolverClass\u000D\u000A\
                        ,pkg.MyMatrixClass@/path/to/file.sidl. If no class is\u000D\u000A\
                        specified (only the SIDL filename is given), all\u000D\u000A\
                        methods from interfaces and classes in the SIDL file\u000D\u000A\
                        are imported into the specified project class.\u000D\u000A\
  --import-impl=IMPLIMPORTS\u000D\u000A\
                        A Babel-generated Impl file from which to import\u000D\u000A\
                        method implementations from the specified class or\u000D\u000A\
                        several classes (with multiple --import-impl options),\u000D\u000A\
                        e.g., --import-\u000D\u000A\
                        impl=\"pkg.MyClass@/path/to/pkg_MyClass/\".\u000D\u000A\
  --exclude-impl-symbols=IMPLEXCLUDES\u000D\u000A\
                        Exclude particular method implementations from\u000D\u000A\
                        importation. If this option is not given, a default\u000D\u000A\
                        set to exclude is read from\u000D\u000A\
                        BOCCA/$PROJECT.defaults:exclude_from_import. e.g.,\u000D\u000A\
                        --exclude-impl-symbols=\"setServices releaseServices\".\u000D\u000A\
                        This option may be repeated. To suppress the default\u000D\u000A\
                        and exclude no symbols, use  --exclude-impl-\u000D\u000A\
                        symbols=None\u000D\u000A\
  --import-impl-exact   All imported method implementations are exactly\u000D\u000A\
                        preserved, ignoring anything newly generated by bocca.\u000D\u000A\
                        Excluded symbols remain excluded. If this option is\u000D\u000A\
                        not given, bocca-generated implementations are\u000D\u000A\
                        appended and the user may need to do manual clean up\u000D\u000A\
                        of the resulting impl code.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        SIDL version of the class in the form X.Y. If no\u000D\u000A\
                        version specification  is given, version '0.0' is\u000D\u000A\
                        used.\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the interfaces and/or classes\u000D\u000A\
                        implemented and/or extended by the new class (or of\u000D\u000A\
                        symbols referenced by those interfaces). Multiple\u000D\u000A\
                        repositories can be used (separated by commas).\u000D\u000A\
                        Alternatively, multiple instances of the -x option can\u000D\u000A\
                        be used to specify multiple repositories paths.\u000D\u000A\
  --remove-implements=REMOVEIMPLEMENTS\u000D\u000A\
                        remove implementation statements for the given SIDL\u000D\u000A\
                        symbol.  Multiple implementations can be removed by\u000D\u000A\
                        repeated --remove-implements options.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help config class

shorthelptext["config class"] = "not supported";

helptext["config class"] = "Class config is not implemented yet.";

//------------------------------------------------------------
// bocca help copy class

shorthelptext["copy class"] = "bocca copy class [options] pkg.MyClassName";

helptext["copy class"] = "bocca help copy class\u000D\u000A\
\u000D\u000A\
Usage: copy component [options] FROM_SIDL_SYMBOL TO_SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -lLANGUAGE, --language=LANGUAGE\u000D\u000A\
                        language for class [project default is cxx]\u000D\u000A\
  -dDIALECT, --dialect=DIALECT\u000D\u000A\
                        language dialect for class [project default is\u000D\u000A\
                        standard]\u000D\u000A\
  --no-impl             Don't copy original implementation from source.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help display class

shorthelptext["display class"] = "bocca display class [options] pkg.MyClassName";

helptext["display class"] = "bocca help display class\u000D\u000A\
\u000D\u000A\
Usage: display class SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -d, --dirs            Show a list of directories containing user-editable\u000D\u000A\
                        files; this can be used as input for revision control\u000D\u000A\
                        operations.\u000D\u000A\
  -f, --files           Show a list of user-editable files, which can be used\u000D\u000A\
                        as input for revision control operations.\u000D\u000A\
  -lLANGUAGES, --languages=LANGUAGES\u000D\u000A\
                        display all class elements whose implementations are\u000D\u000A\
                        in the specified language. To specify multiple\u000D\u000A\
                        languages, multiple -l options can be given, or a\u000D\u000A\
                        comma-separated list of languages.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help edit class

shorthelptext["edit class"] = "bocca edit class [options] pkg.MyClassName";

helptext["edit class"] = "bocca help edit class\u000D\u000A\
\u000D\u000A\
Usage: edit class SIDL_SYMBOL options\u000D\u000A\
        whereis class SIDL_SYMBOL options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -H, --header          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -m, --module          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -i, --implementation  Edit/whereis the implementation file\u000D\u000A\
  -s, --sidl            Edit/whereis the sidl file (the default)\u000D\u000A\
  -t, --touch           Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules      Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars       Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help remove class

shorthelptext["remove class"] = "bocca remove class [options] pkg.MyClassName";

helptext["remove class"] = "bocca help remove class\u000D\u000A\
\u000D\u000A\
Usage: remove class SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help rename class

shorthelptext["rename class"] = "bocca rename class [options] pkg.MyClassName";

helptext["rename class"] = "bocca help rename class\u000D\u000A\
\u000D\u000A\
Usage: rename class OLD_SIDL_SYMBOL NEW_SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help update class

shorthelptext["update class"] = "not supported";

helptext["update class"] = "Class update is not implemented yet.";

//------------------------------------------------------------
// bocca help whereis class

shorthelptext["whereis class"] = "bocca whereis class [options] pkg.MyClassName";

helptext["whereis class"] = "bocca help whereis class\u000D\u000A\
\u000D\u000A\
Usage: bocca [options]\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -H, --header          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -m, --module          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -i, --implementation  Edit/whereis the implementation file\u000D\u000A\
  -s, --sidl            Edit/whereis the sidl file (the default)\u000D\u000A\
  -t, --touch           Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules      Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars       Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help create component

shorthelptext["create component"] = "bocca create component [options] pkg.MyComponentName";

helptext["create component"] = "bocca help create component\u000D\u000A\
\u000D\u000A\
Usage: create component [options] SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -pPROVIDESPORT, --provides=PROVIDESPORT\u000D\u000A\
                        ports PROVIDED by the component. A port is specified\u000D\u000A\
                        as PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully\u000D\u000A\
                        qualified SIDL type of the provided port, and\u000D\u000A\
                        PORT_NAME is the name given to the provided port\u000D\u000A\
                        instance in the component code. Multiple ports can be\u000D\u000A\
                        specified using multiple --provides\u000D\u000A\
                        options.Optionally, an external SIDL file name can be\u000D\u000A\
                        specified if the port is not part of this project,\u000D\u000A\
                        e.g., PORT_TYPE@PORT_NAME@/path/to/portfile.sidl.\u000D\u000A\
  -uUSESPORT, --uses=USESPORT\u000D\u000A\
                        ports USED by the component. A port is specified as\u000D\u000A\
                        PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully\u000D\u000A\
                        qualified SIDL type of the used port, and PORT_NAME is\u000D\u000A\
                        the name given to the used port instance in the\u000D\u000A\
                        component code. Multiple ports can be specified using\u000D\u000A\
                        multiple --uses options. Optionally, an external SIDL\u000D\u000A\
                        file name can be specified if the port is not part of\u000D\u000A\
                        this project, e.g.,\u000D\u000A\
                        PORT_TYPE@PORT_NAME@/path/to/portfile.sidl.\u000D\u000A\
  -gGO, --go=GO         port type gov.cca.ports.GoPort is provided by the\u000D\u000A\
                        component. PORT_NAME must be specified; PORT_TYPE is\u000D\u000A\
                        omitted. Multiple requests for a GoPort will be\u000D\u000A\
                        ignored\u000D\u000A\
  -lLANGUAGE, --language=LANGUAGE\u000D\u000A\
                        language for component [project default is cxx]\u000D\u000A\
  -dDIALECT, --dialect=DIALECT\u000D\u000A\
                        language dialect for component [project default is\u000D\u000A\
                        standard]\u000D\u000A\
  -iIMPLEMENTED_SYMBOL, --implements=IMPLEMENTED_SYMBOL\u000D\u000A\
                        a SIDL interface that the component being created\u000D\u000A\
                        implements (optional, can be repeated). Multiple\u000D\u000A\
                        --extends options can be specified. If\u000D\u000A\
                        IMPLEMENTED_SYMBOL is an existing external interface,\u000D\u000A\
                        the file containing its definition must be specified\u000D\u000A\
                        immediately following the the IMPLEMENTED_SYMBOL,\u000D\u000A\
                        e.g., --implements\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, use the \"change component +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command.\u000D\u000A\
  -eEXTENDED_SYMBOL, --extends=EXTENDED_SYMBOL\u000D\u000A\
                        a SIDL class that the component being created or\u000D\u000A\
                        modified extends (optional). Only one --extends option\u000D\u000A\
                        can be specified. If EXTENDED_SYMBOL is an existing\u000D\u000A\
                        external class, the file containing its definition\u000D\u000A\
                        must be specified immediately following the the\u000D\u000A\
                        EXTENDED_SYMBOL, e.g., --extends\u000D\u000A\
                        pkg.SomeClass@/path/to/somefile.sidl (Babel-generated\u000D\u000A\
                        XML files are allowed, as well).To change the location\u000D\u000A\
                        of the SIDL file associated with a class, usethe\u000D\u000A\
                        \"change component +  SIDL_SYMBOL --sourcefile/-s\u000D\u000A\
                        FILENAME\" command.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the component depends (other than\u000D\u000A\
                        through extension or implementation, for example, a\u000D\u000A\
                        symbol used as the type of one of the arguments in a\u000D\u000A\
                        method in the component.If the symbol is not in this\u000D\u000A\
                        project, a SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the component.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified class or\u000D\u000A\
                        several classes, e.g., --import-sidl=pkg.MySolverClass\u000D\u000A\
                        ,pkg.MyMatrixClass@/path/to/file.sidl. If no class is\u000D\u000A\
                        specified (only the SIDL filename is given), all\u000D\u000A\
                        methods from interfaces and classes in the SIDL file\u000D\u000A\
                        are imported into the specified project component.\u000D\u000A\
  --import-impl=IMPLIMPORTS\u000D\u000A\
                        A Babel-generated Impl file from which to import\u000D\u000A\
                        method implementations from the specified class or\u000D\u000A\
                        several classes (with multiple --import-impl options),\u000D\u000A\
                        e.g., --import-\u000D\u000A\
                        impl=\"pkg.MyClass@/path/to/pkg_MyClass/\".\u000D\u000A\
  --exclude-impl-symbols=IMPLEXCLUDES\u000D\u000A\
                        Exclude particular method implementations from\u000D\u000A\
                        importation. If this option is not given, a default\u000D\u000A\
                        set to exclude is read from\u000D\u000A\
                        BOCCA/$PROJECT.defaults:exclude_from_import. e.g.,\u000D\u000A\
                        --exclude-impl-symbols=\"setServices releaseServices\".\u000D\u000A\
                        This option may be repeated. To suppress the default\u000D\u000A\
                        and exclude no symbols, use  --exclude-impl-\u000D\u000A\
                        symbols=None\u000D\u000A\
  --import-impl-exact   All imported method implementations are exactly\u000D\u000A\
                        preserved, ignoring anything newly generated by bocca.\u000D\u000A\
                        Excluded symbols remain excluded. If this option is\u000D\u000A\
                        not given, bocca-generated implementations are\u000D\u000A\
                        appended and the user may need to do manual clean up\u000D\u000A\
                        of the resulting impl code.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        SIDL version of the component in the form X.Y. If no\u000D\u000A\
                        version specification  is given, version '0.0' is\u000D\u000A\
                        used.\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the ports (and/or interfaces)\u000D\u000A\
                        referenced  by the new component (or of symbols\u000D\u000A\
                        referenced by those ports). Multiple repositories can\u000D\u000A\
                        be used (separated by commas). Alternatively, multiple\u000D\u000A\
                        instances of the -x option can be used to specify\u000D\u000A\
                        multiple repositories paths.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help change component

shorthelptext["change component"] = "bocca change component [options] pkg.MyComponentName";

helptext["change component"] = "bocca help change component\u000D\u000A\
\u000D\u000A\
Usage: change component SIDL_SYMBOL options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -pPROVIDESPORT, --provides=PROVIDESPORT\u000D\u000A\
                        ports PROVIDED by the component. A port is specified\u000D\u000A\
                        as PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully\u000D\u000A\
                        qualified SIDL type of the provided port, and\u000D\u000A\
                        PORT_NAME is the name given to the provided port\u000D\u000A\
                        instance in the component code. Multiple ports can be\u000D\u000A\
                        specified using multiple --provides\u000D\u000A\
                        options.Optionally, an external SIDL file name can be\u000D\u000A\
                        specified if the port is not part of this project,\u000D\u000A\
                        e.g., PORT_TYPE@PORT_NAME@/path/to/portfile.sidl.\u000D\u000A\
  -uUSESPORT, --uses=USESPORT\u000D\u000A\
                        ports USED by the component. A port is specified as\u000D\u000A\
                        PORT_TYPE@PORT_NAME, where PORT_TYPE is the fully\u000D\u000A\
                        qualified SIDL type of the used port, and PORT_NAME is\u000D\u000A\
                        the name given to the used port instance in the\u000D\u000A\
                        component code. Multiple ports can be specified using\u000D\u000A\
                        multiple --uses options. Optionally, an external SIDL\u000D\u000A\
                        file name can be specified if the port is not part of\u000D\u000A\
                        this project, e.g.,\u000D\u000A\
                        PORT_TYPE@PORT_NAME@/path/to/portfile.sidl.\u000D\u000A\
  -gGO, --go=GO         port type gov.cca.ports.GoPort is provided by the\u000D\u000A\
                        component. PORT_NAME must be specified; PORT_TYPE is\u000D\u000A\
                        omitted. Multiple requests for a GoPort will be\u000D\u000A\
                        ignored\u000D\u000A\
  -iIMPLEMENTED_SYMBOL, --implements=IMPLEMENTED_SYMBOL\u000D\u000A\
                        a SIDL interface that the component being created\u000D\u000A\
                        implements (optional, can be repeated). Multiple\u000D\u000A\
                        --extends options can be specified. If\u000D\u000A\
                        IMPLEMENTED_SYMBOL is an existing external interface,\u000D\u000A\
                        the file containing its definition must be specified\u000D\u000A\
                        immediately following the the IMPLEMENTED_SYMBOL,\u000D\u000A\
                        e.g., --implements\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, use the \"change component +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command.\u000D\u000A\
  -eEXTENDED_SYMBOL, --extends=EXTENDED_SYMBOL\u000D\u000A\
                        a SIDL class that the component being created or\u000D\u000A\
                        modified extends (optional). Only one --extends option\u000D\u000A\
                        can be specified. If EXTENDED_SYMBOL is an existing\u000D\u000A\
                        external class, the file containing its definition\u000D\u000A\
                        must be specified immediately following the the\u000D\u000A\
                        EXTENDED_SYMBOL, e.g., --extends\u000D\u000A\
                        pkg.SomeClass@/path/to/somefile.sidl (Babel-generated\u000D\u000A\
                        XML files are allowed, as well).To change the location\u000D\u000A\
                        of the SIDL file associated with a class, usethe\u000D\u000A\
                        \"change component +  SIDL_SYMBOL --sourcefile/-s\u000D\u000A\
                        FILENAME\" command.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the component depends (other than\u000D\u000A\
                        through extension or implementation, for example, a\u000D\u000A\
                        symbol used as the type of one of the arguments in a\u000D\u000A\
                        method in the component.If the symbol is not in this\u000D\u000A\
                        project, a SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the component.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified class or\u000D\u000A\
                        several classes, e.g., --import-sidl=pkg.MySolverClass\u000D\u000A\
                        ,pkg.MyMatrixClass@/path/to/file.sidl. If no class is\u000D\u000A\
                        specified (only the SIDL filename is given), all\u000D\u000A\
                        methods from interfaces and classes in the SIDL file\u000D\u000A\
                        are imported into the specified project component.\u000D\u000A\
  --import-impl=IMPLIMPORTS\u000D\u000A\
                        A Babel-generated Impl file from which to import\u000D\u000A\
                        method implementations from the specified class or\u000D\u000A\
                        several classes (with multiple --import-impl options),\u000D\u000A\
                        e.g., --import-\u000D\u000A\
                        impl=\"pkg.MyClass@/path/to/pkg_MyClass/\".\u000D\u000A\
  --exclude-impl-symbols=IMPLEXCLUDES\u000D\u000A\
                        Exclude particular method implementations from\u000D\u000A\
                        importation. If this option is not given, a default\u000D\u000A\
                        set to exclude is read from\u000D\u000A\
                        BOCCA/$PROJECT.defaults:exclude_from_import. e.g.,\u000D\u000A\
                        --exclude-impl-symbols=\"setServices releaseServices\".\u000D\u000A\
                        This option may be repeated. To suppress the default\u000D\u000A\
                        and exclude no symbols, use  --exclude-impl-\u000D\u000A\
                        symbols=None\u000D\u000A\
  --import-impl-exact   All imported method implementations are exactly\u000D\u000A\
                        preserved, ignoring anything newly generated by bocca.\u000D\u000A\
                        Excluded symbols remain excluded. If this option is\u000D\u000A\
                        not given, bocca-generated implementations are\u000D\u000A\
                        appended and the user may need to do manual clean up\u000D\u000A\
                        of the resulting impl code.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        SIDL version of the component in the form X.Y. If no\u000D\u000A\
                        version specification  is given, version '0.0' is\u000D\u000A\
                        used.\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the ports (and/or interfaces)\u000D\u000A\
                        referenced  by the new component (or of symbols\u000D\u000A\
                        referenced by those ports). Multiple repositories can\u000D\u000A\
                        be used (separated by commas). Alternatively, multiple\u000D\u000A\
                        instances of the -x option can be used to specify\u000D\u000A\
                        multiple repositories paths.\u000D\u000A\
  --remove-implements=REMOVEIMPLEMENTS\u000D\u000A\
                        remove implementation statements for the given SIDL\u000D\u000A\
                        symbol.  Multiple implementations can be removed by\u000D\u000A\
                        repeated --remove-implements options.\u000D\u000A\
  -dDELETEPORTNAME, --delete=DELETEPORTNAME\u000D\u000A\
                        remove ports used or provided by the component given\u000D\u000A\
                        the port name (not SIDL symbol).Multiple ports can be\u000D\u000A\
                        specified using multiple --delete options.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help config component

shorthelptext["config component"] = "not supported";

helptext["config component"] = "Component config is not implemented yet.";

//------------------------------------------------------------
// bocca help copy component

shorthelptext["copy component"] = "bocca copy component [options] pkg.MyComponentName";

helptext["copy component"] = "bocca help copy component\u000D\u000A\
\u000D\u000A\
Usage: copy component [options] FROM_SIDL_SYMBOL TO_SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -lLANGUAGE, --language=LANGUAGE\u000D\u000A\
                        language for component [project default is cxx]\u000D\u000A\
  -dDIALECT, --dialect=DIALECT\u000D\u000A\
                        language dialect for component [project default is\u000D\u000A\
                        standard]\u000D\u000A\
  --no-impl             Don't copy original implementation from source.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help display component

shorthelptext["display component"] = "bocca display component [options] pkg.MyComponentName";

helptext["display component"] = "bocca help display component\u000D\u000A\
\u000D\u000A\
Usage: display component SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -d, --dirs            Show a list of directories containing user-editable\u000D\u000A\
                        files; this can be used as input for revision control\u000D\u000A\
                        operations.\u000D\u000A\
  -f, --files           Show a list of user-editable files, which can be used\u000D\u000A\
                        as input for revision control operations.\u000D\u000A\
  -lLANGUAGES, --languages=LANGUAGES\u000D\u000A\
                        display all component elements whose implementations\u000D\u000A\
                        are in the specified language. To specify multiple\u000D\u000A\
                        languages, multiple -l options can be given, or a\u000D\u000A\
                        comma-separated list of languages.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help edit component

shorthelptext["edit component"] = "bocca edit component [options] pkg.MyComponentName";

helptext["edit component"] = "bocca help edit component\u000D\u000A\
\u000D\u000A\
Usage: edit component SIDL_SYMBOL [optional method name] options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -H, --header          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -m, --module          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -i, --implementation  Edit/whereis the implementation file\u000D\u000A\
  -s, --sidl            Edit/whereis the sidl file (the default)\u000D\u000A\
  -t, --touch           Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules      Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars       Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help remove component

shorthelptext["remove component"] = "bocca remove component [options] pkg.MyComponentName";

helptext["remove component"] = "bocca help remove component\u000D\u000A\
\u000D\u000A\
Usage: remove component SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help rename component

shorthelptext["rename component"] = "bocca rename component [options] pkg.MyComponentName";

helptext["rename component"] = "bocca help rename component\u000D\u000A\
\u000D\u000A\
Usage: rename component OLD_SIDL_SYMBOL NEW_SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help update component

shorthelptext["update component"] = "not supported";

helptext["update component"] = "Component update is not implemented yet.";

//------------------------------------------------------------
// bocca help whereis component

shorthelptext["whereis component"] = "bocca whereis component [options] pkg.MyComponentName";

helptext["whereis component"] = "bocca help whereis component\u000D\u000A\
\u000D\u000A\
Usage: whereis component SIDL_SYMBOL [optional method name] options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -H, --header          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -m, --module          Edit/whereis the header (or module in F90) file\u000D\u000A\
  -i, --implementation  Edit/whereis the implementation file\u000D\u000A\
  -s, --sidl            Edit/whereis the sidl file (the default)\u000D\u000A\
  -t, --touch           Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules      Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars       Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help create enum

shorthelptext["create enum"] = "bocca create enum [options] pkg.MyEnumName";

helptext["create enum"] = "bocca help create enum\u000D\u000A\
\u000D\u000A\
Usage:  create enum SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
        Creates an enum with the name SIDL_SYMBOL. If SIDL_SYMBOL is not fully\u000D\u000A\
        qualified, e.g., MyEnum instead of somepackage.MyEnum, the enum will be added\u000D\u000A\
        to the default package for the project, usually the same as the project name.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all methods from interfaces in the SIDL\u000D\u000A\
                        file are imported into the specified project enum.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help change enum

shorthelptext["change enum"] = "bocca change enum [options] pkg.MyEnumName";

helptext["change enum"] = "bocca help change enum\u000D\u000A\
\u000D\u000A\
Usage: change port [options] SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -eSIDLSYMBOL_AND_LOCATION, --extends=SIDLSYMBOL_AND_LOCATION\u000D\u000A\
                        a SIDL interface that the enum being created extends\u000D\u000A\
                        (optional). Multiple --extends options can be\u000D\u000A\
                        specified. If SIDL_SYMBOL is an existing external\u000D\u000A\
                        interface, the file containing its definition must be\u000D\u000A\
                        specified immediately following the the SIDL_SYMBOL,\u000D\u000A\
                        e.g., --extends\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, usethe \"change enum +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the interfaces and/or classes\u000D\u000A\
                        referenced by this enum. Multiple instances of the\u000D\u000A\
                        --xml option can be used to specify multiple\u000D\u000A\
                        repository paths.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the enum depends (other than through\u000D\u000A\
                        extension or implementation, for example, a symbol\u000D\u000A\
                        used as the type of one of the arguments in a method\u000D\u000A\
                        in the enum.If the symbol is not in this project, a\u000D\u000A\
                        SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the enum.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all methods from interfaces in the SIDL\u000D\u000A\
                        file are imported into the specified project enum.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help config enum

shorthelptext["config enum"] = "not supported";

helptext["config enum"] = "Enum config is not implemented yet.";

//------------------------------------------------------------
// bocca help copy enum

shorthelptext["copy enum"] = "bocca copy enum [options] pkg.MyEnumName";

helptext["copy enum"] = "bocca help copy enum\u000D\u000A\
\u000D\u000A\
Usage: bocca [options]\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help display enum

shorthelptext["display enum"] = "bocca display enum [options] pkg.MyEnumName";

helptext["display enum"] = "bocca help display enum\u000D\u000A\
\u000D\u000A\
Usage: display port SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help   show this help message and exit\u000D\u000A\
  -d, --dirs   Show a list of directories containing user-editable files; this\u000D\u000A\
               can be used as input for revision control operations.\u000D\u000A\
  -f, --files  Show a list of user-editable files, which can be used as input\u000D\u000A\
               for revision control operations.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help edit enum

shorthelptext["edit enum"] = "bocca edit enum [options] pkg.MyEnumName";

helptext["edit enum"] = "bocca help edit enum\u000D\u000A\
\u000D\u000A\
Usage: edit port SIDL_SYMBOL options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help        show this help message and exit\u000D\u000A\
  -s, --sidl        Edit the sidl file (the default)\u000D\u000A\
  -t, --touch       Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules  Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars   Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help remove enum

shorthelptext["remove enum"] = "bocca remove enum [options] pkg.MyEnumName";

helptext["remove enum"] = "bocca help remove enum\u000D\u000A\
\u000D\u000A\
Usage: remove port [options] SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
        Remove the specified port from the project.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help rename enum

shorthelptext["rename enum"] = "bocca rename enum [options] pkg.MyEnumName";

helptext["rename enum"] = "bocca help rename enum\u000D\u000A\
\u000D\u000A\
Usage: rename port [options] SIDL_SYMBOL NEWSIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
        Rename the port specified with the SIDL symbol SIDL_SYMBOL to NEWSIDL_SYMBOL.\u000D\u000A\
        The SIDL file containing the port definition is also renamed.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help update enum

shorthelptext["update enum"] = "not supported";

helptext["update enum"] = "Enum update is not implemented yet.";

//------------------------------------------------------------
// bocca help whereis enum

shorthelptext["whereis enum"] = "bocca whereis enum [options] pkg.MyEnumName";

helptext["whereis enum"] = "bocca help whereis enum\u000D\u000A\
\u000D\u000A\
Usage: whereis port SIDL_SYMBOL options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help        show this help message and exit\u000D\u000A\
  -s, --sidl        Edit the sidl file (the default)\u000D\u000A\
  -t, --touch       Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules  Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars   Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help create interface

shorthelptext["create interface"] = "bocca create interface [options] pkg.MyInterfaceName";

helptext["create interface"] = "bocca help create interface\u000D\u000A\
\u000D\u000A\
Usage:  create interface INTERFACE [--extends/-e SIDL_SYMBOL{FILE}]\u000D\u000A\
\u000D\u000A\
        Creates an interface with the name INTERFACE, optionally extending SIDL_SYMBOL.\u000D\u000A\
        INTERFACE and SIDL_SYMBOL are both SIDL types. If INTERFACE is not fully\u000D\u000A\
        qualified, e.g., MyPort instead of somepackage.MyPort, the port will be added\u000D\u000A\
        to the default package for the project, usually the same as the project name.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -eSIDLSYMBOL_AND_LOCATION, --extends=SIDLSYMBOL_AND_LOCATION\u000D\u000A\
                        a SIDL interface that the interface being created\u000D\u000A\
                        extends (optional). Multiple --extends options can be\u000D\u000A\
                        specified. If SIDL_SYMBOL is an existing external\u000D\u000A\
                        interface, the file containing its definition must be\u000D\u000A\
                        specified immediately following the the SIDL_SYMBOL,\u000D\u000A\
                        e.g., --extends\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, usethe \"change interface +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the interfaces and/or classes\u000D\u000A\
                        referenced by this interface. Multiple instances of\u000D\u000A\
                        the --xml option can be used to specify multiple\u000D\u000A\
                        repository paths.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the interface depends (other than\u000D\u000A\
                        through extension or implementation, for example, a\u000D\u000A\
                        symbol used as the type of one of the arguments in a\u000D\u000A\
                        method in the interface.If the symbol is not in this\u000D\u000A\
                        project, a SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the interface.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all methods from interfaces in the SIDL\u000D\u000A\
                        file are imported into the specified project\u000D\u000A\
                        interface.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help change interface

shorthelptext["change interface"] = "bocca change interface [options] pkg.MyInterfaceName";

helptext["change interface"] = "bocca help change interface\u000D\u000A\
\u000D\u000A\
Usage: change interface [options] SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -eSIDLSYMBOL_AND_LOCATION, --extends=SIDLSYMBOL_AND_LOCATION\u000D\u000A\
                        a SIDL interface that the interface being created\u000D\u000A\
                        extends (optional). Multiple --extends options can be\u000D\u000A\
                        specified. If SIDL_SYMBOL is an existing external\u000D\u000A\
                        interface, the file containing its definition must be\u000D\u000A\
                        specified immediately following the the SIDL_SYMBOL,\u000D\u000A\
                        e.g., --extends\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, usethe \"change interface +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the interfaces and/or classes\u000D\u000A\
                        referenced by this interface. Multiple instances of\u000D\u000A\
                        the --xml option can be used to specify multiple\u000D\u000A\
                        repository paths.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the interface depends (other than\u000D\u000A\
                        through extension or implementation, for example, a\u000D\u000A\
                        symbol used as the type of one of the arguments in a\u000D\u000A\
                        method in the interface.If the symbol is not in this\u000D\u000A\
                        project, a SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the interface.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all methods from interfaces in the SIDL\u000D\u000A\
                        file are imported into the specified project\u000D\u000A\
                        interface.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help config interface

shorthelptext["config interface"] = "not supported";

helptext["config interface"] = "Interface config is not implemented yet.";

//------------------------------------------------------------
// bocca help copy interface

shorthelptext["copy interface"] = "bocca copy interface [options] pkg.MyInterfaceName";

helptext["copy interface"] = "bocca help copy interface\u000D\u000A\
\u000D\u000A\
Usage: copy interface FROM_SIDL_SYMBOL TO_SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help display interface

shorthelptext["display interface"] = "bocca display interface [options] pkg.MyInterfaceName";

helptext["display interface"] = "bocca help display interface\u000D\u000A\
\u000D\u000A\
Usage: display interface SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help   show this help message and exit\u000D\u000A\
  -d, --dirs   Show a list of directories containing user-editable files; this\u000D\u000A\
               can be used as input for revision control operations.\u000D\u000A\
  -f, --files  Show a list of user-editable files, which can be used as input\u000D\u000A\
               for revision control operations.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help edit interface

shorthelptext["edit interface"] = "bocca edit interface [options] pkg.MyInterfaceName";

helptext["edit interface"] = "bocca help edit interface\u000D\u000A\
\u000D\u000A\
Usage: edit interface SIDL_SYMBOL options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help        show this help message and exit\u000D\u000A\
  -s, --sidl        Edit the sidl file (the default)\u000D\u000A\
  -t, --touch       Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules  Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars   Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help remove interface

shorthelptext["remove interface"] = "bocca remove interface [options] pkg.MyInterfaceName";

helptext["remove interface"] = "bocca help remove interface\u000D\u000A\
\u000D\u000A\
Usage: remove interface [options] SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
        Remove the specified interface from the project.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help rename interface

shorthelptext["rename interface"] = "bocca rename interface [options] pkg.MyInterfaceName";

helptext["rename interface"] = "bocca help rename interface\u000D\u000A\
\u000D\u000A\
Usage: rename interface [options] SIDL_SYMBOL NEWSIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
        Rename the interface specified with the SIDL symbol SIDL_SYMBOL to NEWSIDL_SYMBOL.\u000D\u000A\
        The SIDL file containing the interface definition is also renamed.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help update interface

shorthelptext["update interface"] = "not supported";

helptext["update interface"] = "Interface update is not implemented yet.";

//------------------------------------------------------------
// bocca help whereis interface

shorthelptext["whereis interface"] = "bocca whereis interface [options] pkg.MyInterfaceName";

helptext["whereis interface"] = "bocca help whereis interface\u000D\u000A\
\u000D\u000A\
Usage: bocca [options]\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help        show this help message and exit\u000D\u000A\
  -s, --sidl        Edit the sidl file (the default)\u000D\u000A\
  -t, --touch       Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules  Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars   Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help create package

shorthelptext["create package"] = "bocca create package [options] pkg.MyPackageName";

helptext["create package"] = "bocca help create package\u000D\u000A\
\u000D\u000A\
Usage:  create package SIDL_SYMBOL [options]\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all packages from the SIDL file are\u000D\u000A\
                        imported into the specified project package.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        Specify the version of the package; the default is 0.0\u000D\u000A\
";

//------------------------------------------------------------
// bocca help change package

shorthelptext["change package"] = "bocca change package [options] pkg.MyPackageName";

helptext["change package"] = "bocca help change package\u000D\u000A\
\u000D\u000A\
Usage: change package SIDL_SYMBOL [options]\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all packages from the SIDL file are\u000D\u000A\
                        imported into the specified project package.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        Specify the version of the package; the default is 0.0\u000D\u000A\
";

//------------------------------------------------------------
// bocca help config package

shorthelptext["config package"] = "not supported";

helptext["config package"] = "Package config is not implemented yet.";

//------------------------------------------------------------
// bocca help copy package

shorthelptext["copy package"] = "not supported";

helptext["copy package"] = "Package copy is not implemented yet.";

//------------------------------------------------------------
// bocca help display package

shorthelptext["display package"] = "bocca display package [options] pkg.MyPackageName";

helptext["display package"] = "bocca help display package\u000D\u000A\
\u000D\u000A\
Usage:  display package SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help edit package

shorthelptext["edit package"] = "not supported";

helptext["edit package"] = "Package edit is not implemented yet.";

//------------------------------------------------------------
// bocca help remove package

shorthelptext["remove package"] = "not supported";

helptext["remove package"] = "Package remove is not implemented yet.";

//------------------------------------------------------------
// bocca help rename package

shorthelptext["rename package"] = "not supported";

helptext["rename package"] = "Package rename is not implemented yet.";

//------------------------------------------------------------
// bocca help update package

shorthelptext["update package"] = "not supported";

helptext["update package"] = "Package update is not implemented yet.";

//------------------------------------------------------------
// bocca help whereis package

shorthelptext["whereis package"] = "not supported";

helptext["whereis package"] = "Package whereis is not implemented yet.";

//------------------------------------------------------------
// bocca help create port

shorthelptext["create port"] = "bocca create port [options] pkg.MyPortName";

helptext["create port"] = "bocca help create port\u000D\u000A\
\u000D\u000A\
Usage:  create port SIDL_SYMBOL {--extends/-e SIDL_SYMBOL}\u000D\u000A\
\u000D\u000A\
        Creates an interface with the name INTERFACE, optionally extending SIDL_SYMBOL.\u000D\u000A\
        PORTINTERFACE and SIDL_SYMBOL are both SIDL types. If PORTINTERFACE is not fully\u000D\u000A\
        qualified, e.g., MyPort instead of somepackage.MyPort, the port will be added\u000D\u000A\
        to the default package for the project, usually the same as the project name.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -eSIDLSYMBOL_AND_LOCATION, --extends=SIDLSYMBOL_AND_LOCATION\u000D\u000A\
                        a SIDL interface that the port being created extends\u000D\u000A\
                        (optional). Multiple --extends options can be\u000D\u000A\
                        specified. If SIDL_SYMBOL is an existing external\u000D\u000A\
                        interface, the file containing its definition must be\u000D\u000A\
                        specified immediately following the the SIDL_SYMBOL,\u000D\u000A\
                        e.g., --extends\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, usethe \"change port +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the interfaces and/or classes\u000D\u000A\
                        referenced by this port. Multiple instances of the\u000D\u000A\
                        --xml option can be used to specify multiple\u000D\u000A\
                        repository paths.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the port depends (other than through\u000D\u000A\
                        extension or implementation, for example, a symbol\u000D\u000A\
                        used as the type of one of the arguments in a method\u000D\u000A\
                        in the port.If the symbol is not in this project, a\u000D\u000A\
                        SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the port.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all methods from interfaces in the SIDL\u000D\u000A\
                        file are imported into the specified project port.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help change port

shorthelptext["change port"] = "bocca change port [options] pkg.MyPortName";

helptext["change port"] = "bocca help change port\u000D\u000A\
\u000D\u000A\
Usage: change port [options] SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  -eSIDLSYMBOL_AND_LOCATION, --extends=SIDLSYMBOL_AND_LOCATION\u000D\u000A\
                        a SIDL interface that the port being created extends\u000D\u000A\
                        (optional). Multiple --extends options can be\u000D\u000A\
                        specified. If SIDL_SYMBOL is an existing external\u000D\u000A\
                        interface, the file containing its definition must be\u000D\u000A\
                        specified immediately following the the SIDL_SYMBOL,\u000D\u000A\
                        e.g., --extends\u000D\u000A\
                        pkg.SomeInterface@/path/to/somefile.sidl (Babel-\u000D\u000A\
                        generated XML files are allowed, as well).To change\u000D\u000A\
                        the location of the SIDL file associated with an\u000D\u000A\
                        interface, usethe \"change port +  SIDL_SYMBOL\u000D\u000A\
                        --sourcefile/-s FILENAME\" command\u000D\u000A\
  -xXMLREPOS, --xml=XMLREPOS\u000D\u000A\
                        path to external XML repositories containing\u000D\u000A\
                        specification of the interfaces and/or classes\u000D\u000A\
                        referenced by this port. Multiple instances of the\u000D\u000A\
                        --xml option can be used to specify multiple\u000D\u000A\
                        repository paths.\u000D\u000A\
  --requires=REQUIRED_SYMBOL\u000D\u000A\
                        A SIDL symbol or a comma-separated list of SIDL\u000D\u000A\
                        symbols on which the port depends (other than through\u000D\u000A\
                        extension or implementation, for example, a symbol\u000D\u000A\
                        used as the type of one of the arguments in a method\u000D\u000A\
                        in the port.If the symbol is not in this project, a\u000D\u000A\
                        SIDL file name should be given, e.g.,\u000D\u000A\
                        --requires=sidltype@/path/to/file.sidl.\u000D\u000A\
  --remove-requires=SYMBOL_TO_REMOVE\u000D\u000A\
                        Remove the dependency on the specified SIDL symbol or\u000D\u000A\
                        SIDL file (or a comma-separated list of symbols). This\u000D\u000A\
                        affects only dependencies other than extension or\u000D\u000A\
                        implementation, for example, a symbol used as the type\u000D\u000A\
                        of one of the arguments in a method in the port.\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface@/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all methods from interfaces in the SIDL\u000D\u000A\
                        file are imported into the specified project port.\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help config port

shorthelptext["config port"] = "not supported";

helptext["config port"] = "Port config is not implemented yet.";

//------------------------------------------------------------
// bocca help copy port

shorthelptext["copy port"] = "bocca copy port [options] pkg.MyPortName";

helptext["copy port"] = "bocca help copy port\u000D\u000A\
\u000D\u000A\
Usage: copy port [options] FROM_SIDL_SYMBOL TO_SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help display port

shorthelptext["display port"] = "bocca display port [options] pkg.MyPortName";

helptext["display port"] = "bocca help display port\u000D\u000A\
\u000D\u000A\
Usage: display port SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help   show this help message and exit\u000D\u000A\
  -d, --dirs   Show a list of directories containing user-editable files; this\u000D\u000A\
               can be used as input for revision control operations.\u000D\u000A\
  -f, --files  Show a list of user-editable files, which can be used as input\u000D\u000A\
               for revision control operations.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help edit port

shorthelptext["edit port"] = "bocca edit port [options] pkg.MyPortName";

helptext["edit port"] = "bocca help edit port\u000D\u000A\
\u000D\u000A\
Usage: edit port SIDL_SYMBOL options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help        show this help message and exit\u000D\u000A\
  -s, --sidl        Edit the sidl file (the default)\u000D\u000A\
  -t, --touch       Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules  Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars   Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help remove port

shorthelptext["remove port"] = "bocca remove port [options] pkg.MyPortName";

helptext["remove port"] = "bocca help remove port\u000D\u000A\
\u000D\u000A\
Usage: remove port [options] SIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
        Remove the specified port from the project.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help rename port

shorthelptext["rename port"] = "bocca rename port [options] pkg.MyPortName";

helptext["rename port"] = "bocca help rename port\u000D\u000A\
\u000D\u000A\
Usage: rename port [options] SIDL_SYMBOL NEWSIDL_SYMBOL\u000D\u000A\
\u000D\u000A\
        Rename the port specified with the SIDL symbol SIDL_SYMBOL to NEWSIDL_SYMBOL.\u000D\u000A\
        The SIDL file containing the port definition is also renamed.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help  show this help message and exit\u000D\u000A\
";

//------------------------------------------------------------
// bocca help update port

shorthelptext["update port"] = "not supported";

helptext["update port"] = "Port update is not implemented yet.";

//------------------------------------------------------------
// bocca help whereis port

shorthelptext["whereis port"] = "bocca whereis port [options] pkg.MyPortName";

helptext["whereis port"] = "bocca help whereis port\u000D\u000A\
\u000D\u000A\
Usage: whereis port SIDL_SYMBOL options\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help        show this help message and exit\u000D\u000A\
  -s, --sidl        Edit the sidl file (the default)\u000D\u000A\
  -t, --touch       Touch the sidl file as if bocca edit changed it.\u000D\u000A\
  -r, --make-rules  Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars   Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help create project

shorthelptext["create project"] = "bocca create project [options] pkg.MyProjectName";

helptext["create project"] = "bocca help create project\u000D\u000A\
\u000D\u000A\
Usage: create project [options] projectName\u000D\u000A\
\u000D\u000A\
        Creates a project with the specified name.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface:/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all packages from the SIDL file are\u000D\u000A\
                        imported into the project.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        set the version number for this project [default is\u000D\u000A\
                        0.0.0]\u000D\u000A\
  -oOUTDIR, --output-dir=OUTDIR\u000D\u000A\
                        directory in which to create the new project [default\u000D\u000A\
                        is .]\u000D\u000A\
  -pPACKAGE, --package=PACKAGE\u000D\u000A\
                        package name [default is to use the project name as\u000D\u000A\
                        the package]\u000D\u000A\
  -lLANGUAGE, --language=LANGUAGE\u000D\u000A\
                        default language for project impls unless overridden\u000D\u000A\
                        [default is cxx]\u000D\u000A\
  -mMAKETEMPLATE, --make-template=MAKETEMPLATE\u000D\u000A\
                        project build system template to use [default is\u000D\u000A\
                        gmake]\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help change project

shorthelptext["change project"] = "bocca change project [options] pkg.MyProjectName";

helptext["change project"] = "bocca help change project\u000D\u000A\
\u000D\u000A\
Usage: change project [options] projectName\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  --import-sidl=SIDLIMPORTS\u000D\u000A\
                        A SIDL file from which to import a specified interface\u000D\u000A\
                        or several interfaces, e.g., --import-sidl=\"pkg.MySolv\u000D\u000A\
                        erInterface,pkg.MyMatrixInterface:/path/to/file.sidl\".\u000D\u000A\
                        If no interface is specified (only the SIDL filename\u000D\u000A\
                        is given), all packages from the SIDL file are\u000D\u000A\
                        imported into the project.\u000D\u000A\
  -vVERSION, --version=VERSION\u000D\u000A\
                        set the version number for this project [default is\u000D\u000A\
                        0.0.0]\u000D\u000A\
  --dpath=SET_QUERY_PATH\u000D\u000A\
                        Reset the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directories given.\u000D\u000A\
                        Done before append, prepend. Do not mix append and\u000D\u000A\
                        prepend in the same command.\u000D\u000A\
  --dpath-clear         Remove the search path for _depl.xml files. Done\u000D\u000A\
                        before any other dpath actions.\u000D\u000A\
  --dpath-append=APPEND_QUERY_PATH\u000D\u000A\
                        Extend the search path for external symbols in\u000D\u000A\
                        _depl.xml files with the file or directory given.\u000D\u000A\
  --dpath-prepend=PREPEND_QUERY_PATH\u000D\u000A\
                        Insert at front of the current search path for\u000D\u000A\
                        external symbols in _depl.xml.\u000D\u000A\
  --dpath-user=USER_QUERY_PATH\u000D\u000A\
                        Redefine the username to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-host=HOST_QUERY_PATH\u000D\u000A\
                        Redefine the hostname to which other dpath options\u000D\u000A\
                        apply.\u000D\u000A\
  --dpath-show=SHOW_QUERY_PATH\u000D\u000A\
                        --dpath-show[=FILTER] Show the search path for\u000D\u000A\
                        _depl.xml files, filtered by optional [USER]@[HOST] or\u000D\u000A\
                        ALL.\u000D\u000A\
  --dpath-user-alias=NEW_USER_ALIAS\u000D\u000A\
                        Define build-equivalent username for current username.\u000D\u000A\
  --dpath-host-alias=NEW_HOST_ALIAS\u000D\u000A\
                        Define build-equivalent hostname for current hostname.\u000D\u000A\
  --dpath-show-aliases  Show equivalent repository names for current user and\u000D\u000A\
                        host.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help config project

shorthelptext["config project"] = "bocca config project [options] pkg.MyProjectName";

helptext["config project"] = "bocca help config project\u000D\u000A\
\u000D\u000A\
Usage: config project [options]\u000D\u000A\
\u000D\u000A\
        Displays or modifies the contents of the project defaults file:\u000D\u000A\
            <project dir>/BOCCA/<project name>.defaults\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help            show this help message and exit\u000D\u000A\
  --dump                display the bocca project settings\u000D\u000A\
  --system              display the bocca system-wide default settings\u000D\u000A\
  -u, --update          merge the system defaults into the project settings\u000D\u000A\
                        and regenerate project-specific build files. Needed\u000D\u000A\
                        after a bocca project is relocated or after changes to\u000D\u000A\
                        the CCA environment\u000D\u000A\
  -qVAR, --query-var=VAR\u000D\u000A\
                        print the value of VAR in the project. VAR may be\u000D\u000A\
                        section:var or just var to match all sections\u000D\u000A\
  -rKILLVAR, --remove-var=KILLVAR\u000D\u000A\
                        delete the var from the project. VAR must be\u000D\u000A\
                        section:var or a global default var.\u000D\u000A\
  -sSETVAR, --set-var=SETVAR\u000D\u000A\
                        set the value of VAR in the project. VAR may be\u000D\u000A\
                        section:var or just var for a global default\u000D\u000A\
  -vSETVAL, --value=SETVAL\u000D\u000A\
                        the value for the set-var in the project.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help copy project

shorthelptext["copy project"] = "not supported";

helptext["copy project"] = "Project copy is not implemented yet.";

//------------------------------------------------------------
// bocca help display project

shorthelptext["display project"] = "bocca display project [options] pkg.MyProjectName";

helptext["display project"] = "bocca help display project\u000D\u000A\
\u000D\u000A\
Usage: display project [projectName]\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help   show this help message and exit\u000D\u000A\
  -f, --files  Show a list of user-editable files, which can be used as input\u000D\u000A\
               for revision control operations.\u000D\u000A\
  -d, --dirs   Show a list of directories containing user-editable files; this\u000D\u000A\
               can be used as input for revision control operations.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help edit project

shorthelptext["edit project"] = "bocca edit project [options] pkg.MyProjectName";

helptext["edit project"] = "bocca help edit project\u000D\u000A\
\u000D\u000A\
Usage: edit project [--make-rules|--make-vars]\u000D\u000A\
\u000D\u000A\
        The edit command provides support for editing the bocca project's top-level\u000D\u000A\
        makefiles.\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help        show this help message and exit\u000D\u000A\
  -r, --make-rules  Edit the make.rules.user file\u000D\u000A\
  -V, --make-vars   Edit the make.vars.user file\u000D\u000A\
";

//------------------------------------------------------------
// bocca help remove project

shorthelptext["remove project"] = "not supported";

helptext["remove project"] = "Project remove is not implemented yet.";

//------------------------------------------------------------
// bocca help rename project

shorthelptext["rename project"] = "bocca rename project [options] pkg.MyProjectName";

helptext["rename project"] = "bocca help rename project\u000D\u000A\
\u000D\u000A\
Usage: rename project [options] newProjectName\u000D\u000A\
\u000D\u000A\
        Renames the project in the current directory. If multiple\u000D\u000A\
        projects are present in the same directory, use\u000D\u000A\
           'bocca -p <projName> rename project <newProjectName>'\u000D\u000A\
        to disambiguate.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help   show this help message and exit\u000D\u000A\
  -f, --force  Force the change without prompting for confirmation.\u000D\u000A\
";

//------------------------------------------------------------
// bocca help update project

shorthelptext["update project"] = "bocca update project [options] pkg.MyProjectName";

helptext["update project"] = "bocca help update project\u000D\u000A\
\u000D\u000A\
Usage: update project [options]\u000D\u000A\
\u000D\u000A\
        The update command supports options for updating or recovering the\u000D\u000A\
        default build system files, generating sample cvs or svn commands\u000D\u000A\
        (but not running cvs or svn), and other functionality for managing\u000D\u000A\
        bocca upgrades and interactions with revision control systems.\u000D\u000A\
\u000D\u000A\
\u000D\u000A\
Options:\u000D\u000A\
  -h, --help      show this help message and exit\u000D\u000A\
  -b, --build     Update all build system files with the ones from the bocca\u000D\u000A\
                  template; old files are backed up. [NOT AVAILABLE YET]\u000D\u000A\
  --revert-build  Revert all build files to the last version used before using\u000D\u000A\
                  update --build. [NOT AVAILABLE YET]\u000D\u000A\
  --cvs-add       Generate cvs add command string for project directories.\u000D\u000A\
                  This does not actually invoke cvs. [NOT AVAILABLE YET]\u000D\u000A\
  -s, --store     Regenerate the internal project representation (e.g., after\u000D\u000A\
                  upgrading bocca).\u000D\u000A\
";

//------------------------------------------------------------
// bocca help whereis project

shorthelptext["whereis project"] = "not supported";

helptext["whereis project"] = "Project whereis is not implemented yet.";

