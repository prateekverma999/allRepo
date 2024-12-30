print("Welcome to Tip Calculator")

totalBill = float(input("what was the totyal bill?\n"))
tip = int(input("How much tip would you like to give? 10, 12, 15\n"))
totalPeople = float(input("How many people to split the bill?\n"))
tipper = (totalBill/100)*tip
split = (totalBill+tipper)/totalPeople
print(f"Each person should pay: {round(split,2)}")