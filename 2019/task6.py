with open('input') as file:
    program_input = file.read()
    program_input = program_input.split('\n')
    program_input = [x.split(')') for x in program_input]

class SpaceObj:
    def __init__(self, name):
        self.name = name
        self.center = None #Object around which self orbits
        self.satellites = [] #Objects that orbit around self
        self.depth = 0
    
    def insert_satellite(self, satellite):
        self.satellites.append(satellite)
    
    def set_center(self, center):
        self.center = center
    
    def set_depth(self, depth):
        self.depth = depth
    
    def get_name(self):
        return self.name

    def get_center(self):
        return self.center

    def get_satellites(self):
        return self.satellites
    
    def get_depth(self):
        return self.depth

def count_orbits(obj, depth=0): #Recursive count of direct and indirect orbits
    count = 0
    obj.set_depth(depth)
    if obj.get_satellites():
        for x in obj.get_satellites():
            count += count_orbits(x, depth+1)
    
    return count + depth
    
def find_object(name, obj):
    found = None
    if obj.get_name() == name:
        found = obj
    elif obj.get_satellites():
        for x in obj.get_satellites():
            found = find_object(name, x)
            if found:
                return found
    return found

def print_all(obj):
    center = obj.get_center().get_name() if obj.get_center() else None
    print(obj.get_name(), center)
    if obj.get_satellites():
        for x in obj.get_satellites():
            print_all(x)

orbits = []
known_objects = []
for i in program_input: #All entries from input are converted to 'SpaceObj' objects
    obj1 = SpaceObj(i[0]) 
    obj2 = SpaceObj(i[1])
    if obj1.get_name() not in known_objects:
        orbits.append(obj1)
        known_objects.append(obj1.get_name())
    if obj2.get_name() not in known_objects:
        obj2.set_center(obj1)
        orbits.append(obj2)
        known_objects.append(obj2.get_name())
    else:
        for i in orbits:
            if i.get_name() == obj2.get_name():
                i.set_center(obj1)

inner_objects = []

for i in orbits: #Finds all inner objects
        if i.get_center() != None:
            inner_objects.append(i.get_center().get_name())
inner_objects = list(dict.fromkeys(inner_objects))

while inner_objects: #Inserts all objects to their corresponding centers, starting from the 'edge'
    edges = [] #Outer most objects
    centers = [] #and their centers
    for i, v in enumerate(orbits):
        if v.get_name() not in inner_objects:
            edges.append(v)
            for x in orbits:
                if x.get_name() == v.get_center().get_name():
                    centers.append(x)
    for x in edges:
        for y in orbits: 
            if x.get_center().get_name() == y.get_name():
                y.insert_satellite(x)
                break
        orbits = [i for i in orbits if i.get_name() != x.get_name()]
    inner_objects.clear()
    for i in orbits:
        if i.get_center() != None:
            inner_objects.append(i.get_center().get_name())
orbits = orbits[0]
print(count_orbits(orbits))

SAN_obj = find_object('SAN', orbits)
YOU_obj = find_object('YOU', orbits)

#print_all(orbits)

transfer_count = 0
if SAN_obj and YOU_obj:
    while SAN_obj.get_center() != None or YOU_obj.get_center() != None:
        print(SAN_obj.get_center(), YOU_obj.get_center())
        if SAN_obj.get_center().get_name() == YOU_obj.get_center().get_name():
            print('1')
            break
        elif SAN_obj.get_depth() == YOU_obj.get_depth():
            print('2')
            SAN_obj = SAN_obj.get_center()
            YOU_obj = YOU_obj.get_center()
            transfer_count += 2
        elif SAN_obj.get_depth() > YOU_obj.get_depth():
            print('3')
            YOU_obj = YOU_obj.get_center()
            transfer_count += 1
        elif SAN_obj.get_depth() < YOU_obj.get_depth():
            print('4')
            SAN_obj = SAN_obj.get_center()
            transfer_count += 1
print(transfer_count)