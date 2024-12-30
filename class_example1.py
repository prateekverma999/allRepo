class Lamp:
    def __init__(self, model:str,color:str, power_source:str):
        self.model = model
        self.color = color
        self.power_source = power_source
        self.is_on = False

    def turn_on(self):
        print(f"The {self.color} {self.model} lamp is turned on.")
        self.is_on = True

    def turn_off(self):
        print(f"The {self.color} {self.model} lamp is turned off.")
        self.is_on = False

    def describe(self):
        print(f"This lamp is a {self.color} {self.model} lamp, and it uses {self.power_source} power and {self.status()}.")

    def status(self):
        if self.is_on == True:
            return f"This lamp is Active"
        else:
            return f"This lamp is Inactive"

        


Lamp1:Lamp = Lamp("abc1","red","battery")
Lamp2:Lamp = Lamp("abc1","blue","240DC")

Lamp1.turn_on()
Lamp2.turn_off()
Lamp1.describe()
Lamp2.describe()
