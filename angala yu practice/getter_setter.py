class fruits:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    def __str__(self) -> str:
        return f"{self._name}"
    
    def __repr__(self)-> None:
        return f"fruits({self._name})"


apple:fruits = fruits("apple")

apple.name = "banana"
print(apple)
print(apple.__repr__())