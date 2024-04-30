import os, asyncio, nmap, time, pynetbox, json
from nats.aio.client import Client as NATS
from dotenv import load_dotenv

class DiscoverNetwork():

    # Class Variables
    nats_server = ""
    subscribe_subject = ""
    publish_subject = ""
    network_devices = []
    subnet_cidr = ""
    netbox_url = ""
    netbox_token = ""
    nb = None


    def __init__(self):
        # Load environment
        load_dotenv()
        self.nats_server = os.getenv("NATS_SERVER")
        self.publish_subject = os.getenv("PUBLISH_SUBJECT")
        self.subscribe_subject = os.getenv("SUBSCRIBE_SUBJECT")
        self.subnet_cidr = os.getenv("SUBNET_CIDR")
        self.netbox_url = os.getenv("NETBOX_URL")
        self.netbox_token = os.getenv("NETBOX_TOKEN")
        # Report environment
        print(f"""Loaded environment for {os.path.basename(__file__)}
            NATs Server: {self.nats_server}
            Publishing to subject: {self.publish_subject}""")


    def scan_network(self) -> list:
        ### Scan the subnet and figure out if any devices are there that shouldn't be
        # Initialise nmap PortScanner
        nm = nmap.PortScanner()

        # Scan the subnet
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{current_time}: Scanning {self.subnet_cidr}...")
        nm.scan(hosts=self.subnet_cidr, arguments='-sn')

        print(f"Found hosts: {nm.all_hosts()}")

        return nm.all_hosts()

    def fetch_nb(self, nb) -> list:
        devices = list(nb.dcim.devices.all())
        ips = []

        for device in devices:
            ips.append(device.name)

        return ips
            
    def add_to_nb(self, nb, hosts, nb_devices) -> None:
        for host in hosts:
            if host in nb_devices:
                print(f"Ignoring host {host} as it is already present in netbox")
            else:
                self.network_devices.append(host)
                nb.dcim.devices.create(
                    name = host,
                    # site = nb.dcim.devices.get(name='local').id,
                    site = 1,
                    # location = nb.dcim.locations.get(name='location').id,
                    # rack = nb.dcim.racks.get(facility_id=1).id,
                    device_type = nb.dcim.device_types.get(slug='server').id,
                    device_role = 2,
                    # device_role = nb.dcim.device_role.get(name='norole').id,
                    status='active',
                )


    async def main_loop(self) -> None:
        nb = pynetbox.api(
            self.netbox_url,
            token=self.netbox_token
        )

        hosts = self.scan_network()
        nb_devices = self.fetch_nb(nb)

        self.add_to_nb(nb,hosts, nb_devices)
        if self.network_devices: 
            print(self.network_devices)
            
            # Create a NATS client
            self.nc = NATS()
            # Connect to the NATS server
            await self.nc.connect(self.nats_server)

            msg = {}
            devices = "\n".join(self.network_devices)
            msg["msg"] = "New devices added to the network:\n" + devices
            valid_json = str(msg).replace("'", "\"")
            
            await self.nc.publish(self.publish_subject,f"{valid_json}".encode())




if __name__ == "__main__":
    discover_network = DiscoverNetwork()
    asyncio.run(discover_network.main_loop())

