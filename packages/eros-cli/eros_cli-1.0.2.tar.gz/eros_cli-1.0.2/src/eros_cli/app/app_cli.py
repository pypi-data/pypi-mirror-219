import click
from eros_core import Eros
from .utils.eros_terminal import ErosTerminal
from .decorators import eros_check
from .utils.transport_status_log import TransportStatusHandler
@click.command(name="cli", help="User oriented Command Line Interface for the Eros")
@click.pass_context
@eros_check
@click.option('--main_channel', default=5, help='Main Channel to connect to')
@click.option('--aux_channel',  default=6, help='Auxilary Channel to connect to')
def app_cli(ctx, main_channel, aux_channel):
    eros = ctx.obj.get('eros')
    
    TransportStatusHandler(eros)
    
    # Create the terminal
    terminal = ErosTerminal(eros, main_channel, aux_channel)

    #Block until the terminal is closed, use ctrl-c to exit
    terminal.run()
 
   
