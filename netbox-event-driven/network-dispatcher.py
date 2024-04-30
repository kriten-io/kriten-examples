import os, asyncio, json, requests
from nats.aio.client import Client as NATS
from dotenv import load_dotenv

class NetworkDispatcher():

    # Class Variables
    nats_server = ""
    subscribe_subject = ""
    dispatch_task = ""
    kriten_url = ""
    kriten_username = ""
    kriten_password = ""
    kriten_token = ""

    def __init__(self):
        # Load environment
        load_dotenv()
        self.nats_server = os.getenv("NATS_SERVER")
        self.kriten_url = os.getenv("KRITEN_URL")
        self.kriten_username = os.getenv("KRITEN_USERNAME")
        self.kriten_password = os.getenv("KRITEN_PASSWORD")

        if 'EXTRA_VARS' in os.environ:
            os.environ['EXTRA_VARS']
            evars = os.environ['EXTRA_VARS']
            extra_vars = json.loads(evars)
            self.subscribe_subject = extra_vars['subscribe_subject']
            self.dispatch_task = extra_vars['dispatch_task']

        # Report environment
        print(f"""Loaded environment for {os.path.basename(__file__)}
            NATs Server: {self.nats_server}
            Subscribing to subject: {self.subscribe_subject}
            Dispatching task: {self.dispatch_task}
            """)

    def kriten_login(self) -> None:
        url = self.kriten_url+'/api/v1/login'
        payload = {
            "username": self.kriten_username,
            "password": self.kriten_password,
            "provider": "local"
        }

        r = requests.post(url, data=json.dumps(payload))
        if r.status_code != 200:
            print(f"Error during login. Status code: {r.status_code}")
            exit()
        self.kriten_token = r.json()['token']


    async def message_handler(self, msg) -> None:
        self.kriten_login()
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")
        print(f"Dispatching task: '{self.dispatch_task}'")

        headers = {
            "Authorization": "Bearer "+self.kriten_token,
            "content-type": "application/json"
        }
        url = self.kriten_url+'/api/v1/jobs/' + self.dispatch_task
        r = requests.post(url, headers=headers, data=data)

    async def main_loop(self) -> None:
        # Create a NATS client
        self.nc = NATS()
        
        # Connect to the NATS server
        await self.nc.connect(self.nats_server)

        # Subscribe to subject
        await self.nc.subscribe(self.subscribe_subject, cb=self.message_handler)
        print(f"Subscribed to {self.subscribe_subject}")

        # Keep the script running to receive messages
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            print("Disconnecting...")
            await self.nc.close()
        except Exception as e:
            print(e)



if __name__ == "__main__":
    discover_network = NetworkDispatcher()
    asyncio.run(discover_network.main_loop())

