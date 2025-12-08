#!/usr/bin/python3

class Transducer:
    def __init__(self,M):
        self.Q,self.E,self.G,self.D,self.s = M
        self.Tmap = {(p,x):q for p,x,q,y in self.D} 

    def step(self,q, w):
        try:
            q,y = self.Tmap[(q,w)]
            return q,y
        except KeyError:
            print("KeyError")
            return False