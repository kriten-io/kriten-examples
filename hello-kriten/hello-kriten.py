import os
import json
from pprint import pprint

return_result = {}
secrets = {}

secrets_path = '/etc/secret/'

print('Hello, Kriten!\n')

# Kriten exposes input variables for the Job as env variable 'EXTRA_VARS' in json format
# Following code reads it and prints out content

extra_vars = os.environ.get('EXTRA_VARS')

if extra_vars:
    extra_vars_data = json.loads(extra_vars)
    #pprint('Extra vars:')
    #pprint(extra_vars_data)
    return_result['extra_vars'] = extra_vars_data

else:
    print("No extra vars provided.")
    return_result['extra_vars'] = {}
    
print('\n')
# Kriten exposes task secrets to the Job container as files stored in /etc/secret/ directory.
# Following code reads those files and prints in format 'filename:content'

secret_files = os.listdir(secrets_path)

if secret_files:
    print('Revealing secrets, which are no longer secrets!\n')
    for file_name in secret_files:
        if os.path.isfile(secrets_path + file_name):
            with open(secrets_path + file_name, 'r') as f:
                value = f.read()
                #print(f'{file_name}:{value}')
                secrets[file_name] = value

else:
    print("No task secrets provided.")

return_result['secrets'] = secrets

print('^JSON')
print(json.dumps(return_result))
print('^JSON')

print('\n')
print('Script completed.')
