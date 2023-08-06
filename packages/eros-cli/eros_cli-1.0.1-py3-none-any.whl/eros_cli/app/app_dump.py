import click
from eros_core import Eros
from .decorators import eros_check
from .utils.transport_status_log import TransportStatusHandler

def dump(channel, data):
    print(f"[CH {channel}] {data}")
    
@click.command(name="dump", help="Dump all all the received data from the eros")
@click.pass_context
@eros_check
def app_dump(ctx):
    eros = ctx.obj.get('eros')
    TransportStatusHandler(eros)
    click.echo(click.style(f"Starting the dump", fg='green'))
    eros.attach_catch_callback(dump)
   
