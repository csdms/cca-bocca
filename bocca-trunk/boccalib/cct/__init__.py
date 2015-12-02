# By default, Python deprecation warnings are disabled, define the CCA_TOOLS_DEBUG env. variable to enable
try:
    import warnings
    if not ('BOCCA_DEBUG' in os.environ.keys() and os.environ['BOCCA_DEBUG'] == '1'): 
        warnings.filterwarnings("ignore", category=DeprecationWarning)
except:
    pass


action_menu = [
        'help',
        'create', 
        'copy',
        'change',
        'config',
        'display',
        'edit', 
        'remove',
        'rename',
        'update',
        'version',
        'whereis'
        ]

menu_aliases = [
        'sidlclass'
               ]

menu = [
        'project',
        'package',
        'interface',
        'port',
        'class',
        'component',
        'enum',
        'application',
	    'example'
        ]

