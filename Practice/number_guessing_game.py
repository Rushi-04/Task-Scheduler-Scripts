import random

print("Welcome to number guessing game!")
guess_num = random.randint(1,100)
while True:
    try:
        num = int(input("Guess the number: "))

        if num<guess_num:
            print('Too low!')
        elif num>guess_num:
            print('Too high!')
        else:
            print('Congratulations, you got it right.')
    except ValueError:
        print("Enter valid number")