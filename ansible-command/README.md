# ansible-command

Simple Ansible playbook to run a show command on network devices.
This playbook prints output of command and illustrates self-services capability of running Ansible on Kriten.
Edit `hosts` to add names and IP addresses of devices reachable in your network.

Note: This playbook was tested with Ansible 2.9.

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
2. Create a runner which references an image with Ansible installed.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/runners' \
--header 'Content-Type: application/json' \
--data '{
  "name": "kriten-ansible-examples",
  "image": "evolvere/kriten-ansible:0.1",
  "gitURL": "https://github.com/kriten-io/kriten-examples.git"
}'
```
3. Create a task that references the runner and the command to run the script.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/tasks' \
--header 'Content-Type: application/json' \
--data '{
  "name": "network-command",
  "command": "ansible-playbook -i ansible-command/hosts ansible-command/command.yaml",
  "runner": "kriten-ansible-examples",
  "secret": {
      "network_username": "admin",
      "network_password": "admin"
  }
}'
```
4. Launch job.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/network-command' \
--header 'Content-Type: application/json' \
--data '{
  "target_hosts": "evo-eos02",
  "command": "show version"
}'
```
   which returns a job identifier.
```
{"msg":"job executed successfully","value":"network-command-jhvxx"}
```
5. Read the job's stdout output.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/network-command-jhvxx/log' \
--header 'Content-Type: application/json'
```
   which returns a message.
```
PLAY [Read extra_vars] *********************************************************

TASK [Reading target hosts from input vars and storing as localhost fact] ******
ok: [localhost]

PLAY [Network Configs Backup] **************************************************

TASK [Set command variable] ****************************************************
ok: [evo-eos02]

TASK [Cisco NXOS Command] ******************************************************
skipping: [evo-eos02]

TASK [Cisco IOS Command] *******************************************************
skipping: [evo-eos02]

TASK [Arista EOS Command] ******************************************************
ok: [evo-eos02]
[WARNING]: Platform linux on host evo-eos02 is using the discovered Python
interpreter at /usr/local/bin/python, but future installation of another Python
interpreter could change this. See https://docs.ansible.com/ansible/2.9/referen
ce_appendices/interpreter_discovery.html for more information.

TASK [Print command output into stdout] ****************************************
ok: [evo-eos02] => {
    "msg": [
        "Arista vEOS-lab\nHardware version: \nSerial number: C56AD1FD5F9532C2FD51A852146109EB\nHardware MAC address: 0050.56cd.2b91\nSystem MAC address: 0050.56cd.2b91\n\nSoftware image version: 4.27.0F\nArchitecture: x86_64\nInternal build version: 4.27.0F-24308433.4270F\nInternal build ID: 9088210e-613b-47db-b273-7c7b8d45a086\nImage format version: 1.0\n\nUptime: 9 weeks, 4 days, 18 hours and 16 minutes\nTotal memory: 4002360 kB\nFree memory: 2737704 kB"
    ]
}

PLAY RECAP *********************************************************************
evo-eos02                  : ok=3    changed=0    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0     
```
