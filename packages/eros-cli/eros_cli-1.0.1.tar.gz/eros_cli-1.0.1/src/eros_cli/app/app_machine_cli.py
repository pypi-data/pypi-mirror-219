import click
from eros_core import Eros, CLIResponse
from .decorators import eros_check
import time
from .utils.transport_status_log import TransportStatusHandler

@click.command("m-cli", help="Machine oriented Command Line Interface for the Eros")
@click.option('--channel', default=7, type=int, help='Channel to connect to')
@click.pass_context
@eros_check
def app_machine_cli(ctx, channel):

    eros = ctx.obj.get('eros')
    click.echo(click.style(f"Starting the machine cli on channel {channel}", fg='green'))
    TransportStatusHandler(eros)
            
    # Create a new RequestResponse object
    resp = CLIResponse(eros, channel, enable_queue=True)

    # Send test commands
    while True:        
        print('m-cli>', end="")
        cmd = input()
        
        resp.send(cmd)
        
        print(resp.receive_packet())
