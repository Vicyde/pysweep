import random
from collections import deque

class Cell:
    def __init__(self, value, visible=False, marked=False):
        self.isVisible = visible
        self.isMarked = marked
        self.value = 0

    def __repr__(self):
        return str("[" + str(self.value) +  ", " + ("true" if self.isVisible else "false") + "]")

class Playfield:
    def __init__(self, w, h, mines):
        self.width = w
        self.height = h
        self.data = []

        self.empty()
        self.place_mines(mines)
        self.calculate_numbers()

    # Set all cells to zero, invisible and unmarked
    def empty(self):
        self.data = []
        for x in range(self.width):
            self.data.append([])
            for y in range(self.height):
                self.data[-1].append(Cell(0))

    # Place mines at random coordinates
    def place_mines(self, count):
        options=[] 
        self.mines = count
        # When no mines are placed, every position is an option!
        for x in range(self.width):
            for y in range(self.height):
                options.append((x,y))

        positions = random.choices(options, k=self.mines)
        for (x, y) in positions:
            self.data[x][y].value = -1

    # Set for each cell its value to the number of neighbouring mines
    def calculate_numbers(self):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.data[x][y].value == -1:
                    continue
                self.data[x][y].value = self.count_neighbouring_mines(x, y) 

    # Counts the amount of neighbouring mines for a specified cell
    def count_neighbouring_mines(self, x, y):
        count = 0
        for i in range(-1,2):
            cx = x+i
            if cx < 0 or cx >= self.width:
                continue

            for j in range(-1,2):
                cy = y+j
                if cy < 0 or cy >= self.height:
                    continue

                if self.data[cx][cy].value == -1:
                    count += 1
        return count

    def openCell(self, x, y):
        self.data[x][y].isVisible = True
        # Are we a mine?
        if self.data[x][y].value == -1:
            return 1

        # Are we a number ourselves?
        if self.data[x][y].value != 0:
            return 0

        checked = [0] * (self.width*self.height)
        to_check = deque()

        # Let's add ourselves to the list for doing a neighbour check
        to_check.append( (x,y) )
        checked[(y*self.width+x)] = 1

        while to_check:
            # Who's neighbours do we want to check? 
            (x, y) = to_check.popleft()

            # For loops in order to check all 8 corners:
            for i in range(-1,2):
                for j in range(-1,2):
                    # Don't check ourself
                    if i == 0 and j == 0:
                       continue

                    cx=x+i
                    cy=y+j
                    idx= cy * self.width + cx

                    # Out of bound
                    if cx < 0 or cx >= self.width:
                        break 

                    # Out of bound
                    if cy < 0 or cy >= self.height:
                        continue

                    # Already checked?
                    if checked[idx] == 1:
                        continue

                    checked[idx] = 1

                    # is it a mine? Stop here and don't check it's neighbours      
                    if self.data[cx][cy].value == -1:
                        continue

                    self.data[cx][cy].isVisible = True

                    # We are a 0 value; check borders 
                    if self.data[cx][cy].value == 0:
                        to_check.append( (cx, cy) )
            
        return 0

    def checkwin(self):
        # total_cells - (visible + mines) = 0 -> Won
        # correctly_marked - mines = 0 -> Won
        visible = 0
        marked = 0

        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.data[x][y].value == -1 and self.data[x][y].isMarked:
                    marked += 1

                if self.data[x][y].isVisible:
                    visible += 1

        if marked - self.mines == 0: return True
        if (self.width * self.height) - (visible + self.mines) == 0: return True

        return False
