import click
import time
import threading
import zmq as pyzmq
from eros_core import Eros
from .decorators import eros_check
from .utils.transport_status_log import TransportStatusHandler

def poll_socket(socket, timetick = 100):
    poller = pyzmq.Poller()
    poller.register(socket, pyzmq.POLLIN)
    # wait up to 100msec
    try:
        while True:
            obj = dict(poller.poll(timetick))
            if socket in obj and obj[socket] == pyzmq.POLLIN:
                yield socket.recv()
    except KeyboardInterrupt:
        pass

def zmq_broker(eros,port):
    try:
        context = pyzmq.Context()
        pub_socket = context.socket(pyzmq.PUB)
        pub_socket.bind(f'tcp://127.0.0.1:{port}')
        
        sub_socket = context.socket(pyzmq.SUB)
        sub_socket.bind(f'tcp://127.0.0.1:{port+1}')
        sub_socket.subscribe("")
        
        def zmq_transmit(data):
            pub_socket.send(data)
            
            
        eros.attach_raw_callback(zmq_transmit)
        
        poller = pyzmq.Poller()
        poller.register(sub_socket, pyzmq.POLLIN)

        # transmit packets from eros to zmq
        for packet in poll_socket(sub_socket):
            eros.transmit_packet(None, packet)
    finally:
        click.echo(click.style(f"Closing the zmq broker", fg='red'))

    
    
@click.command(name="zmq", help="Start the zmq broker which allows other applications to connect")
@click.option('--port', default=2000, type=int, help='Port to bind to')
@click.pass_context
@eros_check
def app_zmq(ctx,port):
    eros = ctx.obj.get('eros')
    TransportStatusHandler(eros)
    click.echo(click.style(f"Starting the zmq broker", fg='green'))
    
    # Start the zmq broker
    thread = threading.Thread(target=zmq_broker, args=(ctx.obj['eros'],port),daemon=True)
    thread.start()
