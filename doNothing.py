#!/usr/bin/python3
import sys
from Transducer import *

if __name__ == "__main__":
    frgui = open("fromGUI","r")
    togui = open("toGUI","w")
    count = 0

    #Dont include data
    Q = {0, 1, 2, 3, 4, 5}
    inputAlphabet = {"click", "clickOnCanvas", "clickRecenterButton", "clickRecenterPane"
                     "clickRecenterTextBox", "clickTriChooseButton", "clickTriTypeChoice", "documentReady",
                     "mouseDownVertex", "mouseLeaveCanvas", "mouseMove", "mouseUpCanvas",
                     "recenterTextChange", "recenterTextFail", "recenterTextSucc"}
    outputAlphabet = {"noop", "showTP", "hideTP", 
                      "resetT", "showCP", "hideCP",
                      "checkCT", "errorCT", "moveC",
                      "selectV", "moveV", "resetV"}
    #Make sure to have data handling action-message at end of string
    #For multiple action-messages use ";" seperator
    transitions = {(0,"clickRecenterButton",1,"showCP"), (1,"click",0,"hideCP"), (1,"clickRecenterButton",0,"hideCP"), (1,"clickOnCanvas",0,"hideCP;moveC")}
    S = 0
    T = Q, inputAlphabet, outputAlphabet, transitions, S
    transducer = Transducer(T)
     
    while True:
        # Read event message
        try:
            msg,data = frgui.readline().split(maxsplit=1)
        except:
            break
        count += 1
        print(f'Read({count}): {msg} {data}',file=sys.stderr) #4DEBUG!

        # Choose action message to respond with
        # IMPORTANT! My example code does something silly ...
        # - if you click on a vertex, the "Recentering Pane" will appear,
        #   and when you leave the "canvas", it disappears.  See why?

        response = transducer.step(msg)
        #Just makes sure not to pass data accidentally for undefinded transitions
        if(response != "noop"):
            response += " " + data
        else:
            response += " 0"
        
        #Loop to handle multiple action messages at once
        actionList = response.split(";")
        for res in actionList:
            # Respond to GUI - flush to send line immediately!
            print(res + "\n",file=togui,flush=True)
            print(f'Sent({count}): {res}',file=sys.stderr) #4DEBUG!

