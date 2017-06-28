import sys
from emulator import FreematicsEmulator
import csv
import time
if len(sys.argv) != 2:
    exit("Please provide a csv file to play back")
emu = FreematicsEmulator()
emu.connect()
with open(sys.argv[1], 'r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        delay = row[0]
        if delay[0] == '#':
            delay = delay[1:]
        delay = int(delay)
        if delay != 0:
            time.sleep(delay/1000.0)
        emu.set_pid(hex(int(row[1], 16))[2:].zfill(4), int(row[2]))
