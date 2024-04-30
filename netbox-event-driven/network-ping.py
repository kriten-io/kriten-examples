import os, asyncio, pynetbox
from nats.aio.client import Client as NATS
from dotenv import load_dotenv

class DiscoverNetwork():

    # Class Variables
    nats_server = ""
    subscribe_subject = ""
    publish_subject = ""
    network_devices = []
    netbox_url = ""
    netbox_token = ""
    nb = None


    def __init__(self):
        # Load environment
        load_dotenv()
        self.nats_server = os.getenv("NATS_SERVER")
        self.publish_subject = os.getenv("PUBLISH_SUBJECT")
        self.subscribe_subject = os.getenv("SUBSCRIBE_SUBJECT")
        self.netbox_url = os.getenv("NETBOX_URL")
        self.netbox_token = os.getenv("NETBOX_TOKEN")
        # Report environment
        print(f"""Loaded environment for {os.path.basename(__file__)}
            NATs Server: {self.nats_server}
            Publishing to subject: {self.publish_subject}""")


    def fetch_nb(self, nb) -> list:
        devices = list(nb.dcim.devices.all())
        ips = []

        for device in devices:
            ips.append(device.name)

        return ips
            
    def ping_devices(self, nb_devices) -> None:
        for host in nb_devices:
            print(f"Pinging {host}")
            # response = os.system("ping -c 1 " + host)
            
            stream = os.popen('ping -c 1 {}'.format(host))
            output = stream.read()
            if '0 received' in output:
                print("No response")
                self.network_devices.append(host)

            # Building the command. Ex: "ping -c 1 google.com"
            # command = ['ping', '-c', '1', host]
            #
            # if subprocess.call(command) == 0:
            #     self.network_devices.append(host)


    async def main_loop(self) -> None:
        nb = pynetbox.api(
            self.netbox_url,
            token=self.netbox_token
        )

        nb_devices = self.fetch_nb(nb)
        
        self.ping_devices(nb_devices)

        if self.network_devices: 
            # Create a NATS client
            self.nc = NATS()
            # Connect to the NATS server
            await self.nc.connect(self.nats_server)

            msg = {}
            devices = "\n".join(self.network_devices)
            msg["msg"] = "Following devices did not respond to ping:\n" + devices
            valid_json = str(msg).replace("'", "\"")
            
            await self.nc.publish(self.publish_subject,f"{valid_json}".encode())




if __name__ == "__main__":
    discover_network = DiscoverNetwork()
    asyncio.run(discover_network.main_loop())

