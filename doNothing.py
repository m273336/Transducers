#!/usr/bin/python3
import sys
from Transducer import *

if __name__ == "__main__":
    frgui = open("fromGUI","r")
    togui = open("toGUI","w")
    count = 0

    Q = {0, 1, 2, 3, 4, 5}
    inputAlphabet = {"click", "clockOnCanvas", }
    outputAlphabet = {}
    transitions = {}
    S = 1
    transducer = Transducer(Q, inputAlphabet, outputAlphabet, transitions, S)
     
    while True:
        # Read event message
        try:
            msg,data = frgui.readline().split(maxsplit=1);
        except:
            break
        count += 1
        print(f'Read({count}): {msg} {data}',file=sys.stderr) #4DEBUG!

        # Choose action message to respond with
        # IMPORTANT! My example code does something silly ...
        # - if you click on a vertex, the "Recentering Pane" will appear,
        #   and when you leave the "canvas", it disappears.  See why?

        response = transducer.step(msg)
                
        # Respond to GUI - flush to send line immediately!
        print(response + "\n",file=togui,flush=True)
        print(f'Sent({count}): {response}',file=sys.stderr) #4DEBUG!

