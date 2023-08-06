from eros_core import Eros, ErosTCP
import time
import click

@click.group(chain=True)
@click.option('--ip', default='192.168.0.1', help='IP address to use for TCP communication')
@click.option('--port', default=6767, help='Port to use for TCP communication')
@click.pass_context
def tcp(ctx, ip, port):
    click.echo(f"Opening TCP with IP {ip} and port {port}")
    ctx.ensure_object(dict)
    transport = ErosTCP(ip, port,timeout = 3, auto_reconnect = True)
    ctx.obj['eros'] = Eros(transport)
    