import click
import logging
from .transport import drv_tcp, drv_udp, drv_zmq, drv_uart
import time

# Main entrypoint for the CLI
@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode')
def cli(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)-7s (%(msecs)6d) [%(name)s]: %(message)s')
    else:
        # disable logging
        logging.disable(logging.CRITICAL)


# Gets called art the end of the command chain
@drv_uart.uart.result_callback()
@drv_zmq.zmq.result_callback()
@drv_tcp.tcp.result_callback()
@drv_udp.udp.result_callback()
def process_pipeline(data,**kwargs):
    for ret in data:
        if ret == False:
            return
    click.echo(click.style(f"Waiting for applicaiton to finish", fg='white'))
    
    # Block until the application is finished
    while True:
        time.sleep(1)
        
        
# Register the transport selection commands
cli.add_command(drv_uart.uart)
cli.add_command(drv_udp.udp)
cli.add_command(drv_tcp.tcp)
cli.add_command(drv_zmq.zmq)


        
# Register the log command with the transport groups
def attach_app(app):
   drv_uart.uart.add_command(app)
   drv_tcp.tcp.add_command(app)
   drv_udp.udp.add_command(app)
   drv_zmq.zmq.add_command(app)
    
from .app.app_log  import app_log
from .app.app_cli  import app_cli 
from .app.app_zmq  import app_zmq
from .app.app_perf import app_perf
from .app.app_machine_cli import app_machine_cli
from .app.app_dump import app_dump

attach_app(app_log)
attach_app(app_cli)
attach_app(app_zmq)
attach_app(app_perf)
attach_app(app_machine_cli)
attach_app(app_dump)


if __name__ == '__main__':
    cli()