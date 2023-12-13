import os
import json
import pyfiglet

extra_vars = os.environ.get('EXTRA_VARS')

if extra_vars:
    extra_vars_data = json.loads(extra_vars)
    name = extra_vars_data.get('from')
else:
    name = ''

msg_xmas = pyfiglet.figlet_format("Merry Christmas")
msg_name = pyfiglet.figlet_format(name)

print('\n')
print(msg_xmas)
print(msg_name)
print('\n')
