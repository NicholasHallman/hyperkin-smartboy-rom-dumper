import serial
import serial.tools.list_ports
import re
import sys

# Rom header starts at 

gamename = ""
rb = 0
count = 0

def isRom(s):
    global gamename
    global rb
    global count
    code = s.read(2).decode('ascii')
    if code == "nr":
        print("Waiting for game...")
    if code == "nm":
        count += 1
        gamename = s.read(10).decode('ascii')
        print("Name: " + gamename)
        if(count > 10):
            s.write("sd".encode('ascii'))
            count = 0
    if code == "rb":
        rb = int(s.read(3).decode('ascii'))
        print("Block?: " + str(rb))
    if code == "st":
        print("Start Rom!: ")
        s.read(6)
        return True
    return False
    

rom = bytes()
data = bytes()

comlist = serial.tools.list_ports.comports()
connected = []
for element in comlist:
    connected.append(element.device)

# find the smart boy

for com in connected:
    try:
        ser = serial.Serial(com, 9600, timeout=5, parity=serial.PARITY_EVEN, rtscts=1)
    except serial.SerialException:
        print("Device in use! quiting")
        sys.exit() 
    while not isRom(ser):
        print("-------")
    for i in range(rb):
        print("-- part " + str(i) + " --")
        rom = rom + ser.read(16384)

for i in range(2):
    print(" -- extra data " + str(i) + " --")
    extra = ser.read(16000)
    if len(extra) == 0:
        break
    data = data + extra

print("Writing to ROM File...")

f = open(gamename + ".rom", "wb")
f.write(rom)
    
f = open(gamename + "extras.rom", "wb")
f.write(data)

