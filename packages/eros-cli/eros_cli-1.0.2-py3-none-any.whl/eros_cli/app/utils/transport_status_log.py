from eros_core import Eros, TransportStates

COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RESET = "\033[0m"

class TransportStatusHandler():
    def __init__(self, eros):
        eros: Eros        
        eros.transport_handle.attach_status_change_callback(self.status_change_callback)
    
        
    def status_change_callback(self, state):
        if (state == TransportStates.CONNECTING):
            print(f"{COLOR_YELLOW}Connection lost, reconnecting...{COLOR_RESET}")
        if (state == TransportStates.CONNECTED):
            print(f"{COLOR_GREEN}Connection established{COLOR_RESET}")
        if (state == TransportStates.DEAD):
            print(f"{COLOR_RED}Connection lost{COLOR_RESET}")