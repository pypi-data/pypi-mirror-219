from eros_core import Eros, ErosUDP
import time
import click

@click.group(chain=True)
@click.option('--ip', default='192.168.0.1', help='IP address to use for UDP communication')
@click.option('--port', default=5555, help='Port to use for UDP communication')
@click.pass_context
def udp(ctx,ip, port):
    click.echo(f"Opening UDP with IP {ip} and port {port}")
    ctx.ensure_object(dict)

    transport = ErosUDP(ip, port)
    ctx.obj['eros'] = Eros(transport)
    