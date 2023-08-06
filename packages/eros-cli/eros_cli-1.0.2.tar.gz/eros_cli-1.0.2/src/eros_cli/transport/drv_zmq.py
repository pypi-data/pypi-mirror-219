from eros_core import Eros,ErosZMQ
import time
import click


@click.group(chain=True)
@click.option('--port', default=2000, help='Port to use for ZMQ communication')
@click.pass_context
def zmq(ctx, port):
    click.echo(f"Opening ZMQ with port {port}")
    ctx.ensure_object(dict)
    transport = ErosZMQ( port)
    ctx.obj['eros'] = Eros(transport)

