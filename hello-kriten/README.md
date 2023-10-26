# helo-kriten

There is a simple python script, which demonstrates access to input variables and secrets, provided by Kriten to the Job container, where the script is executed.

## To run on Kriten:

Where $KRITEN_URL is set to the URL of your Kriten instance.
eg. `export KRITEN_URL=http://kriten-community.kriten.io`

1. Login
```
curl -c ./token.txt $KRITEN_URL'/api/v1/login' \
--header 'Content-Type: application/json' \
--data '{
  "username": "root",
  "password": "root",
  "provider": "local"
}' 
```
2. Create a runner which references a Python image and the git repository.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/runners' \
--header 'Content-Type: application/json' \
--data '{
  "name": "kriten-examples",
  "image": "python:3.9-slim",
  "gitURL": "https://github.com/Kriten-io/Kriten-examples.git"
}'
```
3. Create a task that references the runner and the command to run the script.
```
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
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/hello-kriten' \
--header 'Content-Type: application/json' \
--data '{
  "name": "Ethan Hunt",
  "operation":"Mission impossible"
}'
```
   which returns a job identifier.
```
{"msg":"job executed successfully","value":"hello-kriten-ks67g"}
```
5. Read the job output.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/hello-kriten-ks67g' \
--header 'Content-Type: application/json'
```
   which returns a message.
```
Hello, Kriten!

Extra vars:
{'name': 'Ethan Hunt', 'operation': 'Mission impossible'}

Revealing secrets, which are no longer secret!
username:admin
super_secret:1234567890!
password:P@55w0rd!

Script complete.
```
