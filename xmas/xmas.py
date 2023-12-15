import os
import json
import pyfiglet
from rich.console import Console
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

console = Console()
extra_vars = os.environ.get('EXTRA_VARS')

if extra_vars:
    extra_vars_data = json.loads(extra_vars)
    name = extra_vars_data.get('from')
else:
    name = ''


msg_xmas = pyfiglet.figlet_format("Merry Christmas")
if name:
    name = "from " + name
    msg_name = pyfiglet.figlet_format(name)

#console.print(msg_xmas_in_colour)
log.info(f'[red]{msg_xmas}', extra={"markup": True})
if name:
    log.info(f'[green]{msg_name}', extra={"markup": True})