# macfinder
Fake response to MAC address location

Example use case for Kriten.

## To test the code locally:
```
export EXTRA_VARS='{"macaddress": "00:50:56:9a:25:71"}'
python3 macfinder.py
```

## To run on Kriten:

Where $KRITEN_URL is set to the URL of your Kriten instance.
eg. `export KRITEN_URL=http://kriten.kriten.io`

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
curl -b ./token.txt $KRITEN_URL'/api/v1/login' \
--header 'Content-Type: application/json' \
--data '{
  "id": "python-utilities",
  "image": "python:3.9-slim",
  "gitURL": "https://github.com/Kriten-io/python-utilities-example.git"
}'
```
3. Create a task that references the runner and the command to run the script.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/login' \
--header 'Content-Type: application/json' \
--data '{
  "id": "macfinder",
  "command": "python macfinder",
  "runner": "python-utilities"
}'
```
4. Launch job.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/macfinder' \
--header 'Content-Type: application/json' \
--data '{
  "macaddress": "00:50:56:9a:25:71"
}'
```
   which returns a job identifier.
```
{"msg":"job executed successfully","value":"macfinder-9p8nc"}
```
5. Read the job output.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/macfinder-9p8nc' \
--header 'Content-Type: application/json'
```
   which returns a message.
```
MAC address: 00:50:56:9a:25:71 found on switch uk-lon-57 port 7/36.
```
