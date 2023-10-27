# ansible-command

Simple Ansible playbook to run a show command on network devices.
This playbook prints output of command and illustrates self-services capability of running Ansible on Kriten.
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
  "target_hosts": "evo-eos02"
}'
```
   which returns a job identifier.
```
{"msg":"job executed successfully","value":"network-command-jhvxx"}
```
5. Read the job output.
```
curl -b ./token.txt $KRITEN_URL'/api/v1/jobs/network-command-jhvxx' \
--header 'Content-Type: application/json'
```
   which returns a message.
```
2023-10-26T19:01:43.737368852+01:00 PLAY [Read extra_vars] *********************************************************
2023-10-26T19:01:43.750652076+01:00 
TASK [Reading target hosts from input vars and storing as localhost fact] ******
2023-10-26T19:01:43.799909602+01:00 ok: [localhost]
2023-10-26T19:01:43.824098540+01:00 
PLAY [Network Configs Backup] **************************************************
2023-10-26T19:01:43.828378501+01:00 
2023-10-26T19:01:43.828416475+01:00 TASK [Cisco NXOS Backup] *******************************************************
skipping: [evo-eos02]

TASK [Cisco NXOS remove timestamp from config] *********************************
skipping: [evo-eos02]

TASK [Cisco IOS Backup] ********************************************************
skipping: [evo-eos02]
2023-10-26T19:01:43.920653463+01:00 
TASK [Arista Backup] ***********************************************************
changed: [evo-eos02]
2023-10-26T19:01:47.609692968+01:00 [WARNING]: Platform linux on host evo-eos02 is using the discovered Python
interpreter at /usr/local/bin/python, but future installation of another Python
interpreter could change this. See https://docs.ansible.com/ansible/2.9/referen
ce_appendices/interpreter_discovery.html for more information.
2023-10-26T19:01:47.613041501+01:00 
TASK [Cisco ASA Backup] ********************************************************
skipping: [evo-eos02]

TASK [Display configuration file] **********************************************
changed: [evo-eos02]
2023-10-26T19:01:48.530224012+01:00 
TASK [Print to console] ********************************************************
2023-10-26T19:01:48.999344946+01:00 ok: [evo-eos02] => {
    "msg": "! Command: show running-config\n! device: evo-eos02 (vEOS-lab, EOS-4.27.0F)\n!\n! boot system flash:/vEOS-lab.swi\n!\nno aaa root\n!\nusername admin privilege 15 role network-admin secret sha512 $6$eHe0ZzHdG2HJSsGv$IL6MIn38jU8dsQfhRD6ahjZkC7sEALKTWzylmL7hLDum3wdeJ0.gfmgIWB4eoSvE8eVV5q1cq/jZRZGeFKnyy1\n!\ntransceiver qsfp default-mode 4x10G\n!\nservice routing protocols model ribd\n!\nhostname evo-eos02\n!\nspanning-tree mode mstp\n!\nmanagement api http-commands\n   no shutdown\n!\ninterface Ethernet1\n!\ninterface Management1\n   ip address dhcp\n!\nip routing\n!\nip route 0.0.0.0/0 192.168.10.251\n!\nend"
2023-10-26T19:01:48.999386355+01:00 }
2023-10-26T19:01:49.002087908+01:00 
2023-10-26T19:01:49.002124078+01:00 PLAY RECAP *********************************************************************
2023-10-26T19:01:49.002129405+01:00 evo-eos02                  : ok=3    changed=2    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0   
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```
