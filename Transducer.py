#!/usr/bin/python3

class Transducer:
    def __init__(self,M):
        self.Q,self.E,self.G,self.D,self.s = M
        self.Tmap = {(p,x):q for p,x,q,y in self.D} 

    # input: a string into the transducer
    # output: the output string given the current state and transition function
    # Handles data input through args if action message needing data is at end of transition
    # return "noop 0" if the key is not in the map
    def step(self, w):
        try:
            if(w[-1] == '0'):
                q,y = self.Tmap[(self.s,w)]
                self.s = q
                return y
            else:
                i = w.index(" ")
                q,y = self.Tmap[(self.s,w[:i])]
                self.s = q
                return y + " " + w[i:]
            
        except KeyError:
            return "noop 0"
