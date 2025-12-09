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
    #For multiple action-messages use ";" seperator and have " 0" for previous action-message
    transitions = { (0, "documentReady", 1, "move <0, -1.33>; resetT"),
        (1,"clickRecenterButton",2,"showCP"), (1, "clickTriChooseButton", 3, "showTP"), (1, "mouseDownVertex", 4, "selectV"), 
                   (2,"click",1,"hideCP"), (2,"clickRecenterButton",1,"hideCP"), (2,"clickOnCanvas",1,"hideCP 0;moveC"), (2, "recenterTextChange", 5, "checkCT"), (2, "clickTriChooseButton", 3, "hideCP 0; chooseTP"),
                   (3, "clickRecenterButton", 2, "hideTP 0; showCP"), (3, "clickTriChooseButton", 1, "showTP"), (3, "click", 1, "hideTP 0; resetT"), (3, "mouseDownVertex", 4, "hideTP 0; selectV"),
                   (4, "mouseMove", 4, "moveV"), (4, "moveLeaveCanvas", 1, "resetV"), (4, "mouseUpCanvas", 1, "moveV"),
                   (5, "recenterTextSucc", 1, "hideCP 0; moveCP"), (5, "recenterTextFail", 5, "errorCT")
                   

                   }
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

