#!/usr/bin/python2
import sys
from Transducer import *

if __name__ == "__main__":
    frgui = open("fromGUI","r")
    togui = open("toGUI","w")
    #count = 0 #For debug

    #Dont include data
    Q = {0, 1, 2, 3, 4}
    inputAlphabet = {"click", "clickOnCanvas", "clickRecenterButton", "clickRecenterPane"
                     "clickRecenterTextBox", "clickTriChooseButton", "clickTriTypeChoice", "documentReady",
                     "mouseDownVertex", "mouseLeaveCanvas", "mouseMove", "mouseUpCanvas",
                     "recenterTextChange", "recenterTextFail", "recenterTextSucc"}
    outputAlphabet = {"noop", "showTP", "hideTP", 
                      "resetT", "showCP", "hideCP",
                      "checkCT", "errorCT", "moveC",
                      "selectV", "moveV", "resetV"}
    #Make sure to have data handling action-message at end of string
    #For multiple action-messages use "," seperator ****with no extra spaces**** and have " 0" for previous action-message
    #Each line a diffrent transition line and by number order
    transitions = {(0,"clickRecenterButton",1,"showCP"), 
                   (0, "clickTriChooseButton", 2, "showTP"),
                   (0, "mouseDownVertex", 3, "selectV"), 
                   (1,"click",0,"hideCP"), (1,"clickRecenterButton",0,"hideCP"), (1,"clickOnCanvas",0,"hideCP 0,moveC"),
                   (1, "clickTriChooseButton", 2, "hideCP 0,showTP"),
                   (1, "recenterTextChange", 4, "checkCT"),
                   (2, "clickRecenterButton", 1, "hideTP 0,showCP"), 
                   (2, "click", 0, "hideTP"), (2, "clickOnCanvas", 0, "hideTP"), (2, "clickTriChooseButton", 0, "hideTP"), (2, "clickTriTypeChoice", 0, "hideTP 0,resetT"),
                   (2, "mouseDownVertex", 3, "hideTP 0,selectV"),
                   (3, "mouseMove", 3, "moveV"), 
                   (3, "mouseLeaveCanvas", 0, "resetV"), (3, "mouseUpCanvas", 0, "moveV"),
                   (4, "recenterTextSucc", 0, "hideCP 0,moveC"), 
                   (4, "recenterTextFail", 1, "errorCT")}
    S = 0
    T = Q, inputAlphabet, outputAlphabet, transitions, S
    transducer = Transducer(T)
     
    while True:
        # Read event message
        try:
            msg,data = frgui.readline().split(maxsplit=1)
        except:
            break
        #count += 1 #For debug
        #print(f'Read({count}): {msg} {data}',file=sys.stderr) #3DEBUG!

        #Takes input string and steps through transducer to get output as well as put in it new state
        #Data is append on seperatly based on the format of the transitions

        response = transducer.step(msg)
            
        
        #Splits response in the case of multiple action-messages
        actionList = response.split(",",maxsplit=1)

        #Handles data appending
        if(actionList[-1] != "noop"):
            actionList[-1] += " " + data
        else:
            #Only noop transitions are for those not found in a state
            print("ERROR! Unexpected event message " + msg + " while in state " + str(transducer.curr), file=sys.stderr)
            actionList[-1] += " 0"

        #Loop to handle multiple action messages at once 
        for res in actionList:
            # Respond to GUI - flush to send line immediately!
            print(res + "\n",file=togui,flush=True)
            #print(f'Sent({count}): {res}',file=sys.stderr) #3DEBUG!

