#!/usr/bin/python3

class Transducer:
    def __init__(self,T):
        self.Q,self.E,self.G,self.D,self.s = T
        self.Tmap = {(p,x):(q,y) for p,x,q,y in self.D} 
        self.curr = self.s

    # input: a string into the transducer
    # output: the output string given the current state and transition function
    # return "noop 0" if the key is not in the map
    def step(self, w):
        try:
            q,y = self.Tmap[(self.curr,w)]
            self.curr = q
            #print(q)
            return y
            
        except KeyError:
            #print(self.curr)
            return "noop"
