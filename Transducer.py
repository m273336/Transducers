#!/usr/bin/python3

class Transducer:
    def __init__(self,M):
        self.Q,self.E,self.G,self.D,self.s = M
        self.Tmap = {(p,x):q for p,x,q,y in self.D} 

    # input: a string into the transducer
    # output: the output string given the current state and transition function
    #         return "noop 0" if the key is not in the map
    def step(self, w):
        try:
            q,y = self.Tmap[(self.s,w)]
            self.s = q
            return y
        except KeyError:
            return "noop 0"
