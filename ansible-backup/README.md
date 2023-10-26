# ansible-backup

Simple Ansible playbook to backup network devices.
Edit `hosts` to add names and IP addresses of devices reachable in your network.
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
2. Create a runner which references an image with Ansible installed and the git repository.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/runners' \
--header 'Content-Type: application/json' \
--data '{
  "name": "kriten-ansible-examples",
  "image": "python:3.9-slim",
  "gitURL": "https://github.com/Kriten-io/Kriten-examples.git"
}'
```
3. Create a task that references the runner and the command to run the script.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/tasks' \
--header 'Content-Type: application/json' \
--data '{
  "name": "network-backup",
  "command": "python hello-kriten/hello-kriten.py",
  "runner": "kriten-ansible-examples",
  "secret": {
      "network_username": "admin",
      "network_password": "admin"
  }
}'
```
4. Launch job.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/network-backup' \
--header 'Content-Type: application/json' \
--data '{
  "target_hosts": "evo-eos02"
}'
```
   which returns a job identifier.
```
{"msg":"job executed successfully","value":"network-backup-ks67g"}
```
5. Read the job output.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/network-backup-ks67g' \
--header 'Content-Type: application/json'
```
   which returns a message.
```
```
