import random
# Ask for rolling dice or not (y/n) (small or capital doesn't matter)

counter = 0
while True:
    decision = input("Do you want to roll dice ? (y/n) : ").lower()
    if decision=='y':
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        print(f'({die1}, {die2})')
        counter +=1
    elif decision=='n':
        print(f"You've rolled {counter} dice in this session.")
        print('Thanks for playing visit again!')
        break
    else:
        print("Invalid Choice!")

