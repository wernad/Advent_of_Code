import threading
import time

import intcode_computer as ic

class netComputer(ic.IntcodeComputer):
    def __init__(self, *args, **kwargs):
        super(netComputer, self).__init__(*args, **kwargs)
        self.incoming = []
        self.name = ''

    def read_packet(self):
        if self.incoming:
            incoming_packet = self.incoming.pop(0)
            self.input = [value for _, value in incoming_packet.items()]
            #print('PC {} received \'X: {} Y: {}\''.format(self.name, incoming_packet['X'], incoming_packet['Y']))
        elif len(self.input) > 0:
            if self.input[-1] != -1:
                self.input.append(-1)

    def send_packet(self):
        new_packet = dict()
        
        if self.process_intcode() == -1:
            return
        new_packet['addr'] = self.output.pop(0)
        
        
        self.process_intcode()
        new_packet['X'] = self.output.pop(0)
        
        self.process_intcode()
        new_packet['Y'] = self.output.pop(0)
        return new_packet

def find_packet(computer, name):
    global NAT_packet
    global computers
    computer.name = str(name)

    while not NAT_packet:
        computer.read_packet()
        #print('PC {} input: {}'.format(computer.name, computer.input))
        new_packet = computer.send_packet()
        if not new_packet:
            continue
        #print('After PC {} input: {}'.format(computer.name, computer.input))
        
        if new_packet['addr'] == 255:
            if not NAT_packet:
                print('Part 1:', new_packet['Y'])
            NAT_packet = new_packet
        else:
            #print('PC {} send \'X: {} Y: {}\' to {}'.format(computer.name, new_packet['X'], new_packet['Y'], new_packet['addr']))
            computers[new_packet['addr']].incoming.append(new_packet)

def NAT():
    global NAT_packet
    global computers

    idle_counter = 0
    last_NAT_message = None
    while True:
        if idle_counter >= 25:
            if last_NAT_message == NAT_packet:
                print('Part 2:', NAT_packet['Y'])
                NAT_packet = -1
                break
            print('NAT send X: {} Y: {}'.format(NAT_packet['X'], NAT_packet['Y']))
            computers[0].input = [value for _, value in NAT_packet.items()]
            computers[0].input[0] = 10
            last_NAT_message = NAT_packet
            idle_counter = 0
        elif not any(comp.incoming for comp in computers.values()):
            print(idle_counter)
            idle_counter += 1
            time.sleep(0.5)
        else:
            idle_counter = 0

puzzle_input = ic.load_input('23')

computers = {i: netComputer(puzzle_input, True, True) for i in range(50)}
for addr, _ in computers.items():
    computers[addr].input = [addr]

NAT_packet = None

threads = list()

for i in range(50):
    print(i)
    new_thread = threading.Thread(target=find_packet, args=(computers[i],i,))
    new_thread.daemon = True
    new_thread.start()
    threads.append(new_thread)

for thread in threads:
    thread.join()

#NAT()
#time.sleep(15)

