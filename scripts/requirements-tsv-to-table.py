#!/usr/bin/env python3
"""
Convert a TSV file exported from Google Docs containing application
requirements into HTML code which can be copy-pasted into our documentation.
"""

import logging
import sys

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

TEMPLATE_HEADER = '''\
<tr>
<th scope="col">Code</th>
<th scope="col">Requirement</th>
<th scope="col">
    Justification for exclusion
    <br>OR<br>
    Evidence
    <br>OR<br>
    Comment
</th>
</tr>
'''

TEMPLATE_HEADING = '''\
<tr>
<th scope="col">{code}</td>
<th scope="col">
    {requirement}
</th>
<th scope="col">&nbsp;</td>
</tr>
'''

TEMPLATE_SEPARATOR = '''\
<tr>
<td colspan="3">&nbsp;</td>
</tr>
'''

TEMPLATE = '''\
<tr>
<td>{code}</td>
<td>
    {requirement}
    <details>
        <summary>Why is this important?</summary>
        {why}
    </details>
</td>
<td>&nbsp;</td>
</tr>
'''

print(f'''<!--
This document was generated from an internal document using the
`{sys.argv[0]}` script.
-->''')
print('<table>')
for line in sys.stdin:
    row = line.split('\t')
    code, requirement, _, why = row[0:4]

    if code == 'Code':
        print(TEMPLATE_HEADER.format(**locals()))
    elif code == '':
        print(TEMPLATE_SEPARATOR.format(**locals()))
    elif why == '':
        print(TEMPLATE_HEADING.format(**locals()))
    else:
        print(TEMPLATE.format(**locals()))
print('</table>')
