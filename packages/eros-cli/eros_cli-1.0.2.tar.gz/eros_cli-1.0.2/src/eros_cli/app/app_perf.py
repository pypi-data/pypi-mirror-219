import time
import click
from si_prefix import si_format
from rich.live import Live
from rich.table import Table

from eros_core import Eros
from .decorators import eros_check

from .utils.transport_status_log import TransportStatusHandler

     
def generate_perf_table(eros):
    """Make a new table."""
    table = Table(title="Eros Performance",title_justify="left")
    table.add_column("Channel",justify="right",style="cyan")
    table.add_column("RX",justify="right")
    table.add_column("RX rate",justify="right",style="blue")
    table.add_column("TX",justify="right")
    table.add_column("TX rate",justify="right",style="blue")
    for ch_id,(rx_channel,tx_channel) in eros.analytics.items():
        table.add_row( f"{ch_id}",
                        f"{si_format(rx_channel.get_total(), precision=2):>6s}B",
                        f"{si_format(rx_channel.get_rate(), precision=2)}b/s",
                        f"{si_format(tx_channel.get_total(), precision=2)}B", 
                        f"{si_format(tx_channel.get_rate(), precision=2)}b/s",) # f"{channel.get_rx_rate()}", f"{channel.get_total_rx()}

    return table
    
@click.command(name='perf', help='Shows the data transfer rate of each channel')
@click.option('--channel', default=1, help='Channel to log')
@click.pass_context
@eros_check
def app_perf(ctx,channel):
    eros = ctx.obj.get('eros')
    TransportStatusHandler(eros)
    
    click.echo(click.style(f"Starting the perf", fg='green'))
        
    with Live(generate_perf_table(eros), refresh_per_second=4) as live:
        while True:
            time.sleep(0.2)
            live.update(generate_perf_table(eros))

