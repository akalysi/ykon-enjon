# ykon enjon interpreter
# a language made for my conlang, ymyx-ykon

from bitarray import bitarray
import sys, traceback

data = None
mapping = {}
bit = 0
skip = 0
target = 0
stopped = False

def parse(i, line):
    global data, mapping, bit, skip, target, stopped

    try:
        if skip > 0:
            skip -= 1
            print(f"skipping line {i+1}")
            return
        
        # header
        if i == 0:
            # the first line is reserved for allocation, how many bits you will have to your use
            data = bitarray(int(line)) 
        elif i == 1:
            # the second line is reserved for the main way to store data, basically just a bunch of variables in which the names are data states
            pairs = line.split(",")
            for pair in pairs:
                chunk = pair.split(":")
                mapping[chunk[0]] = chunk[1]
        for cmd in line.split("/"):
            # injoen - verb, go forward
            if cmd == "injoen":
                if bit + 1 < len(data): bit += 1
            # injain - verb, go backward
            elif cmd == "injain":
                if bit > 0: bit -= 1
            # ixakin - verb, write
            elif cmd == "ixakin":
                nd = data[:bit+1].to01()
                out = mapping[nd].encode().decode("unicode_escape")
                print(out, end="")
            # ipaxit6 - verb, show
            elif cmd == "ipaxit":
                print(data[bit])
            # ykainat - noun, condition
            elif cmd == "ykainat":
                if data[bit] == 0:
                    skip += 1
            # ikanj - verb, change
            elif cmd == "ikanj":
                data[bit] = not data[bit]
            # itan - verb, to put in
            elif cmd == "itan":
                if input("") != "0":
                    data[bit] = 1
                else:
                    data[bit] = 0
            # ikonj - verb, move to
            elif cmd == "ikonj":
                nd = data[:bit+1].to01()
                target = int(mapping[nd])-1
            # imonj - verb, halt; destroy
            elif cmd == "imonj":
                stopped = True
        
    except Exception:
        traceback.print_exc()

def main(fname):
    global target
    with open(fname) as file:
        f = file.readlines()
    while not stopped:
        parse(target, f[target].strip())
        if len(f) > target + 1: target += 1

fname = sys.argv[1] if len(sys.argv) > 1 else "index.ykon"
main(fname)