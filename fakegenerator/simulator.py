from random import randint, random
from typing import Union, List, Tuple

def randfloat(a,b):
    return randint(a*100,b*100)/100

class ChargerDevice:
    def __init__(self, device_id : str) -> None:
        self.id = device_id
        self.status = "free"
        self.distance = 9999
        self.chargeLevel = 0
        self.time = 0

        self._counter = 0
        self._chargingSpeed = 20
        
    def __repr__(self) -> str:
        pass

    def step(self):
        if self.status == "free":
            if random() <= 0.3:
                self.status = "occupied"
                self.distance = 3
                self.chargeLevel = randint(0,60)
                self.time = (100-self.chargeLevel)/self._chargingSpeed
                self._counter = 1

        if self.status == "occupied":
            if random() <= (self.chargeLevel/100) or self.chargeLevel<80:
                self.chargeLevel = self.chargeLevel + self._chargingSpeed
                self.time = (100-self.chargeLevel)/self._chargingSpeed
                if self.chargeLevel >= 100:
                    self.status = "free"
                    self.distance = 9999
                    self.chargeLevel = 0
                    self.time = 0

            else: # Car leaves without fully charged
                self.status = "free"
                self.distance = 9999
                self.chargeLevel = 0
                self.time = 0

        return (
            (self.id, "distanceUltrasonic", self.distance),
            (self.id, "status", self.status),
            (self.id, "levelOfCharging", self.chargeLevel),
            (self.id, "remainingTimeForFullCharge", self.time)
        )

class Device:
    """ Represents a device that has multiple
    attributes and can send data when given a 
    mqtt client
    """
    def __init__(self, data : dict) -> None:
        self.device_id = data["device_id"]
        self.simulators : List[Simulator] = []
        for attr in data["attributes"]:
            if attr["type"] == "Inverse":
                self.simulators.append(attr["id"])
            else:
                self.simulators.append(Simulator(json=attr))
    
    def __repr__(self):
        return f"{self.device_id}:\n\t{self.simulators}"

    def step(self) -> Tuple[Tuple]:
        # Returns tuple with the values for the publish function
        # ((device_id, attr, value), (device_id, attr, value)...)
        out = []
        for sim in self.simulators:
            if type(sim) == str:
                v =self.simulators[0].boundary[-1] - out[0][2]
                out.append( (self.device_id, sim, v) )
            else:
                out.append((self.device_id, sim.id, sim.step()))
        return tuple(out)


        
        

class Simulator:
    """ Simulates the data of one kind of attribute
    """
    def __init__(self, json: dict) -> None:
        
        start = json["range"]
        boundary = None
        self.id = json["id"]
        if "bound" in json.keys():
            boundary = json["bound"]

        self.current = start
        self.boundary = boundary
        if type(start) == list:
            if type(start[0]) == float:
                self.current = randfloat(*start)
                if boundary:
                    self.boundary = [float(i) for i in boundary]
                
                if boundary == None: boundary = start
                i = 0.10
                # variation is 10% of the limit values
                self.variation = (boundary[1]-boundary[0])*i
                

            elif type(start[0]) == int:
                self.current = randint(start[0], start[1])
                if boundary:
                    self.boundary = [int(i) for i in boundary]
                if boundary == None: boundary = start
                i = 0.1
                self.variation = (boundary[1]-boundary[0])*i
                while self.variation < 1:
                    i += 0.05
                    self.variation = (boundary[1]-boundary[0])*i

            elif type(start[0]) == str:
                self.current = start[randint(0,len(start)-1)]
                self.boundary = start

    def __repr__(self):
        return f"{self.id}={self.current}"

    def step(self):
        if type(self.current) == str:
            return self.boundary[randint(0,len(self.boundary)-1)]

        var = randfloat(-1,1)*self.variation
        if (type(self.current) == float):
            self.current = round(self.current+var,2)
        elif (type(self.current) == int):
            self.current = round(self.current+var)

        if not(self.boundary): return self.current
        
        if self.current >= self.boundary[1]:
            self.current = self.boundary[1]
        if self.current <= self.boundary[0]:
            self.current = self.boundary[0]

        return self.current

if __name__ == "__main__":
    attr = {
                "device_id": "charger"
            }

    import matplotlib.pyplot as plt
    
    a = ChargerDevice(attr)
    plt.figure()
    n = 12
    x = [10*i for i in range(n)]
    y1 = []
    y2 = []
    for i in range(n):
        a.step()
        y1.append(a.chargeLevel)
        y2.append(a.time)

    plt.plot(x,y1)
    plt.plot(x,y2,"+")
    plt.show()
