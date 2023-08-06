from ku import tcpsession, state
from .util import ansicol, genrancol, format_bytes
from time import time

reset = "\u001b[0m"

class stream(tcpsession):
    def __init__(self, client, server, proxy):
        self.id = id(self)   
        self.color = ansicol(*genrancol(1.17))

        print(self.color, F"#{self.id} {client.getpeername()}->{client.getsockname()}::{server.getsockname()}->{server.getpeername()}", reset)

    def clientbound(self, data):
        print(self.color, F"#{self.id} server->client  {len(data)}", reset)
    
    def serverbound(self, data):        
        print(self.color, F"#{self.id} client->server  {len(data)}", reset)
    
    def connection_made(self):
        print(self.color, F"#{self.id} connection_made", reset)
    
    def connection_lost(self, side, err):
        side = 'client' if side is self.client else 'server' if side is not None else 'proxy'
        print(self.color, F"#{self.id} connection_lost by {side} due to {err}", reset)
    
class transit(tcpsession):

    cs = 0
    sc = 0

    def clientbound(self, data):
        self.sc += len(data)

    def serverbound(self, data):        
        self.cs += len(data)
                
    def __repr__(self) -> str:
        if self._state != state.CONNECTED:
            return super().__repr__()
        ttime = ".".join([i.zfill(2) for i in str(round((time() - self.estab_time), 2)).split('.')])

        c_ = format_bytes(self.cs)
        cs = f"{str(round(c_[0], 2)).zfill(5)}{c_[1]}"

        s_ = format_bytes(self.sc)
        sc = f"{str(round(s_[0], 2)).zfill(5)}{s_[1]}"

        t = f"{cs} C <-> S {sc}"

        return f"#{id(self)}[{ttime}] / {self.client.getpeername()} / {t}"
