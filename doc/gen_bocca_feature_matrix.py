#!/usr/bin/env python

import os, popen2, sys, datetime
from string import Template

bocca='bocca'

# Get version and current time
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'..','boccalib')))
from boccaversion import bocca_version
last_update = datetime.datetime.now().strftime("%d %B %Y")


# The full enchilada 
#actions="create change config copy diff display edit export remove rename update whereis".split(' ')
#subjects="application class component enum interface package port project".split(' ')

actions="create change config copy display edit remove rename update whereis".split(' ')
subjects="class component enum interface package port project".split(' ')

s1 = Template('shorthelptext[$key] = $val;\n')
s2 = Template('helptext[$key] = $val;\n')

jsfile = open('boccahelp.js','w')
print >>jsfile, 'var helptext = {};\nvar shorthelptext = {};\n'
table_tr = Template('     <tr class="trdata$count" align="center"><td class="td_bold"  align="left">$subj</td>\r\n')
table_td = Template('          <td class="xtd" onmouseover="floatLayer(\'${command}\')" onclick="showHelp(\'${command}\')" onmouseout="hideLayer(\'${command}\')">\r\n' \
                  + '              <div id="${command}" class="hints"></div>\r\n' \
                  + '          $supported</td>\r\n')

htmlTemplate = Template('''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Bocca features matrix</title>

<!-- stylesheet -->
<link href="stylesheet.css" rel="stylesheet" type="text/css" />

<script type="text/javascript" src="boccahelp.js"></script>
<script type="text/javascript" src="boccajscripts.js"></script>

</head>
<body>
<table border="0" width="100%" cellpadding="0" cellspacing="0">
<tbody>
    <tr align="center" bgcolor="#eeeeee" valign="top">
        <td nowrap="nowrap" class="td_top">
        <center>
        <p class="header_text">Last Update: $date | Latest Version: $version</p>
        </center>
        </td>
    </tr>

    

</tbody>
</table>

<h1>Bocca Commands Cheat Sheet</h1>

<table border="0" width="90%" cellpadding="2px" cellspacing="0" margin="0" align="center">
    <tbody id="commands">
''') 
html = htmlTemplate.substitute(date=last_update, version=bocca_version)

html +=  '<tr>\r\n          <td class="td_header"></td>\r\n'

for action in actions: 
    html += '          <td class="td_header_bold" align="center">' + action + '</td>\r\n'

html += '     </tr>\r\n\r\n'
counter = 0
for subject in subjects:
    html += table_tr.substitute(subj=subject,count=counter)
    for action in actions:
        notSupported = False
        cmd = bocca + ' help ' + action + ' ' + subject
        print cmd
        output,input = popen2.popen4(cmd)
        out = output.readlines()
        if not out or out[0].startswith('Bocca ERROR:'): notSupported = True
        helptext = cmd + '\u000D\u000A\\\r\n\u000D\u000A\\\r\n'
        for line in out:
           helptext += line.rstrip() + '\u000D\u000A\\' + '\r\n'

        if notSupported: helptext = subject.capitalize() + ' ' + action + ' is not implemented yet.'

        helptext = helptext.replace('"','\\"').replace("'","\'")

        if notSupported: 
            shorthelptext = 'not supported'
            x = ''
        else: 
            shorthelptext = 'bocca ' + action + ' ' + subject + ' [options] pkg.My' + subject.capitalize() + 'Name'
            x = 'x'

        print >>jsfile, '//' + '-'*60 + '\n','// ' + cmd + '\n'
        keystr = '"' + action + ' ' + subject + '"'
        print >>jsfile, s1.substitute(key=keystr, val='"'+shorthelptext+'"')
        print >>jsfile, s2.substitute(key=keystr, val='"'+helptext+'"')

        # The HTML
        html += table_td.substitute(command=action + ' ' + subject,supported=x)

    counter = (counter + 1) % 2
    html += '      </tr>\r\n'

jsfile.close()

html += '      <tr><td colspan="'+str(len(actions)+1)+'" class="td_footer"></td></tr>\r\n'
html += '''  </tbody>
</table>


<h2>Command Help</h2>
<h4>(click on an 'x' in the table to display)</h4>
<blockquote><pre id="helptext" style="font-size:12px"></pre></blockquote>

</body>
</html>'''

htmlfile = open('bocca_feature_matrix.html','w')
print >>htmlfile, html
htmlfile.close()

        

