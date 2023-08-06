from eros_core import Eros, ErosSerial
import time
import click

@click.group(chain=True)
@click.option('--port', default="auto", help='Port to use for UART communication')
@click.option('--baud', default=2000000, help='Baud rate for UART communication')
@click.option('--vid', default=4292, help='Vendor ID automatic serial port detection')
@click.pass_context
def uart(ctx,port, baud, vid):
    ctx.ensure_object(dict)
    
    try:
        transport = ErosSerial(port=port, baudrate=baud,vid=4292)
        ctx.obj['eros'] = Eros(transport)
        if port == "auto":
            click.echo(click.style(f"Opening UART with auto port detection (found {transport.port}) and baud {transport.baudrate}", fg='green'))
        else:
            click.echo(click.style(f"Opening UART with port '{transport.port}' and baud {transport.baudrate}", fg='green'))
    
    except Exception as e:
        click.echo(click.style(f"Failed to open UART: {e}", fg='red'))