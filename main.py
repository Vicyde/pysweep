import math
from playfield import Playfield

colored_numbers = ["\033[37m.\033[0m", # 0,
                   "\033[32m1\033[0m", # 1,
                   "\033[34m2\033[0m", # 2,
                   "\033[35m3\033[0m", # 3,
                   "\033[33m4\033[0m", # 4,
                   "\033[36m5\033[0m", # 5,
                   "\033[37m6\033[0m", # 6,
                   "\033[31m7\033[0m", # 7,
                   "\033[30;44m8\033[0m", # 8,
                   "\033[30;31m9\033[0m", # 9,
                   "\033[3;33;41mX\033[0m", # Mine, 
                   "\033[0;34;43mV\033[0m", # Flag
                   "\033[37m#\033[0m", # Terrain
                   ]

def print_field(field, showAll=False):

    # Print row numbers
    print('    ',end='')
    for x in range(field.width):
        print('%02d' % x, end=' ')
    print()

    # Print separator
    print('   ',end='')
    for x in range(field.width):
        print('---', end='')
    print()

    for y in range(field.height):
        for x in range(field.width):
            if x == 0:
                print('%02d' % y, ':', end=' ')


            if field.data[x][y].isVisible == True or showAll == True:
                if field.data[x][y].value == -1:
                    print(colored_numbers[10], end='  ')
                else:
                    print(colored_numbers[field.data[x][y].value],end='  ')

            elif field.data[x][y].isMarked == True:
                print(colored_numbers[11], end='  ')
            else:
                print(colored_numbers[12], end='  ')

        print()


if __name__=='__main__':
    width = int(input("Width of the field: "))
    height = int(input("Height of the field: "))
    mines_perc = int(input("% of mines: "))

    mines = math.floor(1.0 * width * height * (mines_perc / 100.0))

    print("Okay! Here goes! %d mines to find. Good luck!" % mines)
    field = Playfield(width, height, mines)
    while True:
        print('\033[0m')
        print_field(field)
        print()

        inp = input("Give position ([X] [Y]) or mark position (M [X] [Y]):").upper().split()
        if len(inp) < 1:
            print("Invalid input")
            continue

        if inp[0] == 'Q':
            print("Goodbye!")
            break

        if(inp[0] == 'M'):
            try:
                x = int(inp[1])
                y = int(inp[2])
                field.data[x][y].isMarked = not field.data[x][y].isMarked
            except ValueError:
                print("Invalid coordinates. Try again")
                continue

        if inp[0].isdigit():
            try:
                x = int(inp[0])
                y = int(inp[1])
            except ValueError:
                print("Invalid coordinates. Try again")
                continue

            result = field.openCell(x, y)

        if field.checkwin() == True:
            print()
            print("YOU WON!")
            break

        if result == 1:
            print()
            print("BOOM! GAME OVER!")
            break

    print()
    print_field(field, True)
