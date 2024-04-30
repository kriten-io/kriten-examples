import requests, os, json
from dotenv import load_dotenv

class SlackBot:

    # Class Variables
    slack_url = ""

    def __init__(self):
        load_dotenv()
        self.slack_url = os.getenv("SLACK_URL")

    def send_message(self, message: str):
        message_payload = {
            "text": message
        }
        print(f"Sending message: {message}")
        try:
            response = requests.post(self.slack_url, json=message_payload)
            if response.status_code == 200:
                print("Message was sent successfully to slack")
            else:
                print("Message was not sent to slack, status_code:", response.status_code)
        except Exception as e:
            print("An exception occurred while sending a slack message", e)

if __name__ == "__main__":
    slackbot = SlackBot()
    slack_message = "No message provided"
    if 'EXTRA_VARS' in os.environ:
        os.environ['EXTRA_VARS']
        evars = os.environ['EXTRA_VARS']
        extra_vars = json.loads(evars)
        if extra_vars.get('msg'):
            slack_message = extra_vars['msg']
    slackbot.send_message(slack_message)

