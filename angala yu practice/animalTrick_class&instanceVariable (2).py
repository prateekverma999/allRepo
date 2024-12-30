class Animal:
    all_trick = []  # Class-level list to store tricks from all animals

    def __init__(self, name):
        self.name = name  # Instance-level variable to store each animal's name
        self.tricks = []  # Instance-level list to store tricks of the specific animal

    def user_input(self):
        trick_input = input(f"Enter trick name for {self.name}: ")
        self.tricks.append(trick_input)
        Animal.all_trick.append(trick_input)  # Add the trick to the class-level list

    def perform_trick(self):
        self.user_input()
        print(f"{self.name} does {self.tricks}")

# Input number of animals
number_of_animals = int(input("Enter number of animals you want to train: "))

# List to store animal instances
animals = []

# Create animal instances and collect their tricks
for _ in range(number_of_animals):
    animal_name = input("Enter animal name: ")
    animal_instance = Animal(animal_name)  # Create an animal object
    animals.append(animal_instance)  # Add animal object to list

# Input number of tricks and perform them
trick_range = int(input(f"Enter number of tricks you want to append for each animal: "))

for _ in range(trick_range):
    for animal_instance in animals:
        animal_instance.perform_trick()  # Let each animal perform a trick

# Print all tricks performed by all animals
print("All tricks performed by all animals:", Animal.all_trick)
