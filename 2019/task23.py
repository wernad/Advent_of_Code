import threading
import time
from collections import deque

import intcode_computer as ic

class netComputer(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(netComputer, self).__init__(*args, **kwargs)
        self.incoming = deque()
        self.name = ''
        self._lock = threading.Lock()

    #Reads the oldest packet in queue. If queue is empty, takes -1 as input but only if it is not there yet.
    def read_packet(self):
        with self._lock:
            if self.incoming and not self.input:
                incoming_packet = self.incoming.popleft()
                self.input = [value for _, value in incoming_packet.items()][1:]
            elif len(self.input) > 0:
                if self.input[-1] != -1:
                    self.input.append(-1)

    #Sends a new packet. Packet is a dictionary of address and X,Y values.
    def send_packet(self):
        with self._lock:
            new_packet = dict()

            if self.process_intcode() == -1:
                return
            new_packet['addr'] = self.output.pop(0)

            self.process_intcode()
            new_packet['X'] = self.output.pop(0)

            self.process_intcode()
            new_packet['Y'] = self.output.pop(0)
        return new_packet

#Each thread runs while network's up, continuously reading and sending packets.
def run_pc(computer, name):
    global NAT_packet
    global computers
    global network_up
    computer.name = str(name)

    while network_up:
        computer.read_packet()

        new_packet = computer.send_packet()
        if not new_packet:
            continue

        if new_packet['addr'] == 255:
            #Prints first NAT packet.
            if not NAT_packet:
                print('Part 1:', new_packet['Y'])
            NAT_packet = new_packet
        else:
            computers[new_packet['addr']].incoming.append(new_packet)

#Checks if networks idle, if so, sends packet to reset network.
def NAT():
    global NAT_packet
    global computers
    global network_up

    last_NAT_message = {
        'addr': None, 
        'X': None, 
        'Y': None
        }
    while True:
        if not any(comp.incoming for comp in computers.values()):
            time.sleep(3) #Three seconds of no new packets means network's idle.
            if not any(comp.incoming for comp in computers.values()):
                if last_NAT_message['Y'] == NAT_packet['Y']:
                    print('Part 2:', NAT_packet['Y'])
                    network_up = False
                    break
                computers[0].input = [value for _, value in NAT_packet.items()][1:]
                last_NAT_message = NAT_packet    

network_up = True
puzzle_input = ic.load_input('23')
NAT_packet = None

#Dictionary used to read and send packets among threads.
computers = {i: netComputer(puzzle_input, True, True) for i in range(50)}
for addr, _ in computers.items():
    computers[addr].input = [addr, -1]

threads = list()
for i in range(50):
    new_thread = threading.Thread(target=run_pc, args=(computers[i],i,))
    new_thread.daemon = True
    new_thread.start()
    threads.append(new_thread)

NAT()

for x in threads:
    x.join()