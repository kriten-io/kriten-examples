# macfinder
Fake response to MAC address location

Example use case for Kriten.

## To test the code locally:
```console
export EXTRA_VARS='{"macaddress": "00:50:56:9a:25:71"}'
python3 macfinder.py
```

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
  "name": "macfinder",
  "command": "python macfinder/macfinder.py",
  "runner": "kriten-examples"
}'
```
4. Launch job.
```console
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/macfinder' \
--header 'Content-Type: application/json' \
--data '{
  "macaddress": "00:50:56:9a:25:71"
}'
```
   which returns a job identifier.
```json
{"id":"macfinder-9p8nc", "msg":"job executed successfully"}
```
5. Read the job output.
```console
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/macfinder-9p8nc' \
--header 'Content-Type: application/json'
```
   which returns a message.
```console
MAC address: 00:50:56:9a:25:71 found on switch uk-lon-57 port 7/36.
```
