# commenttab.py. This file automatically created by PLY (version 2.3). Don't edit!
_lextokens    = {'COMMENT': None, 'CODE': None, 'MULTILINE_COMMENT_END': None, 'MULTILINE_COMMENT_BEGIN': None}
_lexreflags   = 0
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_newline>(\\r\\n)+|\\n+)|(?P<t_COMMENT>[ \\t]*/\\*[^\\n]+\\*/|.*//(.*)\\n|"(\\\\.|[^"\\\\])*"\\n)|(?P<t_MULTILINE_COMMENT_BEGIN>[ \\t]*/\\*.*\\n)|(?P<t_MULTILINE_COMMENT_END>.*\\*/)|(?P<t_CODE>[^(\\/\\/)\\n]+.*\\n)', [None, ('t_newline', 'newline'), None, ('t_COMMENT', 'COMMENT'), None, None, ('t_MULTILINE_COMMENT_BEGIN', 'MULTILINE_COMMENT_BEGIN'), ('t_MULTILINE_COMMENT_END', 'MULTILINE_COMMENT_END'), ('t_CODE', 'CODE')])]}
_lexstateignore = {'INITIAL': '\r\x0c'}
_lexstateerrorf = {'INITIAL': 't_error'}
