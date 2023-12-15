# hello-kriten

There is a simple python script, which demonstrates access to input variables and secrets, provided by Kriten to the Job container, where the script is executed.

## To run on Kriten:

Where $KRITEN_URL is set to the URL of your Kriten instance.
eg. `export KRITEN_URL=http://kriten-community.kriten.io`

1. Login
```console
curl -c ./token.txt $KRITEN_URL'/api/v1/login' \
--header 'Content-Type: application/json' \
--data '{
  "username": "root",
  "password": "root",
  "provider": "local"
}' 
```
2. Create a runner which references a Python image and the git repository.
```console
curl -b ./token.txt $KRITEN_URL'/api/v1/runners' \
--header 'Content-Type: application/json' \
--data '{
  "name": "kriten-examples",
  "image": "python:3.9-slim",
  "gitURL": "https://github.com/kriten-io/kriten-examples.git"
}'
```
3. Create a task that references the runner and the command to run the script.
```console
curl -b ./token.txt $KRITEN_URL'/api/v1/tasks' \
--header 'Content-Type: application/json' \
--data '{
  "name": "hello-kriten",
  "command": "python hello-kriten/hello-kriten.py",
  "runner": "kriten-examples",
  "secret": {
      "username": "admin",
      "password": "P@55w0rd!",
      "super_secret": "1234567890!"
  }
}'
```
4. Launch job.
```console
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/hello-kriten' \
--header 'Content-Type: application/json' \
--data '{
  "agent_name": "Ethan Hunt",
  "operation":"Mission impossible"
}'
```
   which returns a job identifier.
```json
{"msg":"job executed successfully","value":"hello-kriten-ks67g"}
```
5. Read the job output.
```console
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/hello-kriten-ks67g' \
--header 'Content-Type: application/json'
```
   which returns a message.
```json
{
  "id": "hello-kriten-rqlvg",
  "owner": "root",
  "startTime": "Fri Dec 15 17:11:35 UTC 2023",
  "completionTime": "Fri Dec 15 17:11:40 UTC 2023",
  "failed": 0,
  "completed": 1,
  "stdout": "Hello, Kriten!\n\nThis script demonstrates Kriten's capabilities.\nIt reads input variables (EXTRA_VARS) and secrets, and prints them.\n\n\n^JSON\n\n{\"extra_vars\": {\"agent_name\": \"Ethan Hunt\", \"operation\": \"Mission impossible\"}, \"secrets\": {\"password\": \"P@55w0rd!\", \"username\": \"admin\", \"super_secret\": \"1234567890!\"}}\n^JSON\n\n\n\nScript completed.\n",
  "json_data": {
    "extra_vars": {
      "agent_name": "Ethan Hunt",
      "operation": "Mission impossible"
    },
    "secrets": {
      "password": "P@55w0rd!",
      "super_secret": "1234567890!",
      "username": "admin"
    }
  }
}

```
```console
Hello, Kriten!

This script demonstrates Kriten's capabilities.
It reads input variables (EXTRA_VARS) and secrets, and prints them.


{'extra_vars': {'agent_name': 'Ethan Hunt', 'operation': 'Mission impossible'},
 'secrets': {'password': 'P@55w0rd!',
             'super_secret': '1234567890!',
             'username': 'admin'}}


Script completed.
```
