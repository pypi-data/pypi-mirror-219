import click
from eros_core import Eros
from .decorators import eros_check
from .utils.transport_status_log import TransportStatusHandler
import re

def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)

def cb_log_failed(data:bytes):
    # Here we want to sanitize the data, so its nice and printable
    # This can contain any bytes, more effor is needed
    
    #Remove zero bytes
    data = data.replace(b'\x00',b'')
    
    # Don't print empty packets
    if len(data) == 0:
        return
    # Decode the data, ignore errors
    data = data.decode('utf-8', errors='ignore')
    
    #REmoving the colors to emphasize that the packets are not valid eros packets
    data = escape_ansi(data)
    
    # Recolor the packet
    data = click.style(data, fg='bright_black')
    print(f"{data}",end="")
    
def cb_log(data:bytes):
    print(data.decode(),end="")
    
@click.command(name="log", help="Log the data of a specific channel")
@click.pass_context
@eros_check
@click.option('--channel', default=1, help='Channel to log')
@click.option('--log_failed', '-f',is_flag=True, show_default=True, default=False, help='also log failed packets (which could not be decoded)')
def app_log(ctx,channel,log_failed):
    eros = ctx.obj.get('eros')
    click.echo(click.style(f"Starting the logger", fg='green'))
    eros.attach_channel_callback(channel, cb_log)
    if log_failed:
        eros.attach_fail_callback(cb_log_failed)
    TransportStatusHandler(eros)
