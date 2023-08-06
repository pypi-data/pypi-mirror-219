from eros_core import Eros, TransportStates
from blessed import Terminal
import threading
import time
from queue import Queue
from eros_core import Eros, CLIResponse, ResponseType, CommandFrame

COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

class ErosTerminal():
    def __init__(self, eros:Eros, main_channel, aux_channel) -> None:
        self.eros:Eros = eros
        self.main_channel = main_channel
        self.aux_channel = aux_channel

        self.resp = CLIResponse(eros, main_channel, self.rx_packet_callback)

        self.main_receive_buffer = b""
        self.main_transmit_queue = Queue()
                
        self.eros.attach_channel_callback(self.aux_channel, self.receive_aux)
       
        self.transmit_thread_handle = threading.Thread(target=self.transmit_thread, daemon=True)
    
        
    def transmit_thread(self):
        last_transmit = time.time()
        while True:
            buffer = bytearray()
            
            # If we are repeatedlt transmitting, wait a bit
            if time.time() - last_transmit < 0.025:
                time.sleep(0.025)
            
            while True:
                buffer += self.main_transmit_queue.get()
                if self.main_transmit_queue.empty():
                    break
            
            last_transmit = time.time()
            self.eros.transmit_packet(self.main_channel, bytes(buffer))
    
    def rx_packet_callback(self, packet):
        if packet.resp_type == ResponseType.NACK:
            if len(packet.data):
                self.terminal_write( f"{COLOR_RED}Error: {packet.data.decode()}{COLOR_RESET}\n")
            else:
                self.terminal_write( f"{COLOR_RED}Error{COLOR_RESET}\n")
        else:
            if len(packet.data):
                # If ends with a newline, print it without a newline
                if packet.data[-1] == 10:
                    self.terminal_write( f"{packet.data.decode()}")
                else:
                    self.terminal_write( f"{packet.data.decode()}\n")
            else:
                self.terminal_write( f"{COLOR_GREEN}OK{COLOR_RESET}\n")
            
    def receive_aux(self, data):
        self.terminal_write(f"{data.decode()}")
        
    def terminal_write(self, text):
        print(text, end="")
        
        # Smehow this is needed to make the terminal work
        with self.terminal.location(x=0, y=0):
            pass
            
                    
    def run(self):
        self.transmit_thread_handle.start()
        self.terminal = Terminal()

        print( self.terminal.clear)
        self.eros.transmit_packet(self.main_channel, "\n")
         
        with self.terminal.location(x=0, y=0):
            print(self.terminal.black_on_darkkhaki(self.terminal.center('EROS Terminal')))
                    
        with self.terminal.cbreak(): #), self.terminal.hidden_cursor()
            while True:

                # Read a character from the terminal
                inp = self.terminal.inkey()         
                #Send the character to the main channel     
                # self.main_transmit_buffer += inp.encode()  
                self.main_transmit_queue.put(inp.encode())
  
