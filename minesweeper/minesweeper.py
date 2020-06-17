import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def layout(self):
        return [self.cells,self.count]

    def known_mines(self):
        #Takes the self cells, looks at the count
        if self.count == len(self.cells):
            return self.cells
        else:
            return None

    def known_safes(self):
        #Takes the self cells, looks at the count
        if self.count == 0:
            return self.cells
        else:
            return None


    def mark_mine(self, cell):

        self.cells = self.cells -{cell}
        count -= 1

    def mark_safe(self, cell):

        self.cells = self.cells - {cell}

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        #update all the sentences that contain this cell
        for sent in self.knowledge:
            sent.mark_safe(cell)

        surrounding_tiles = [(cell[0]-1,cell[1]-1),(cell[0]+1,cell[1]+1),(cell[0]-1,cell[1]+1),
                            (cell[0]+1,cell[1]-1), (cell[0],cell[1]+1),(cell[0],cell[1]-1),
                             (cell[0]+1,cell[1]),(cell[0]-1,cell[1])]
        #checking for cells located on the border
        if cell[0] == 0:
            surrounding_tiles.remove((cell[0]-1,cell[1]-1))
            surrounding_tiles.remove((cell[0]-1,cell[1]+1))
            surrounding_tiles.remove((cell[0]-1,cell[1]))
        if cell[0] == 7:
            surrounding_tiles.remove((cell[0]+1,cell[1]+1))
            surrounding_tiles.remove((cell[0]+1,cell[1]-1))
            surrounding_tiles.remove((cell[0]+1,cell[1]))
        if cell[1] == 0 and cell[0] == 0:
            surrounding_tiles.remove((cell[0]+1,cell[1]-1))
            surrounding_tiles.remove((cell[0],cell[1]-1))

        if cell[1] == 0 and cell[0] == 7:
            surrounding_tiles.remove((cell[0]-1,cell[1]-1))
            surrounding_tiles.remove((cell[0],cell[1]-1))

        if cell[1] == 0 and cell[0]!= 0 and cell[0] != 7:
            surrounding_tiles.remove((cell[0]-1,cell[1]-1))
            surrounding_tiles.remove((cell[0]+1,cell[1]-1))
            surrounding_tiles.remove((cell[0],cell[1]-1))

        if cell[1] == 7 and cell[0] == 0:
            surrounding_tiles.remove((cell[0]+1,cell[1]+1))
            surrounding_tiles.remove((cell[0],cell[1]+1))

        if cell[1] == 7 and cell[0] == 7:
            surrounding_tiles.remove((cell[0]-1,cell[1]+1))
            surrounding_tiles.remove((cell[0],cell[1]+1))


        if cell[1] == 7 and cell [0] != 0 and cell[0] != 7:
            surrounding_tiles.remove((cell[0]+1,cell[1]+1))
            surrounding_tiles.remove((cell[0]-1,cell[1]+1))
            surrounding_tiles.remove((cell[0],cell[1]+1))

        #making a new logical sentence
        new_sentence = Sentence(surrounding_tiles,count)

        #removing the safe tiles from this sentence
        for i in surrounding_tiles:
            if i in self.safes:
                new_sentence.mark_safe(i)

        #checking if all the surrounding cells are safe/mines or not
        if new_sentence.known_safes():
            for i in surrounding_tiles:
                self.safes.add(i)

        elif new_sentence.known_mines():
            for i in surrounding_tiles:
                self.mines.add(i)

        elif new_sentence.layout()[0]:
            self.knowledge.append(new_sentence)

        #Compare all sentences
        #see if one is contained in the other
        #if it is then subtract them and form a new sentence
        #check if the sentence has known safe or known mine
        #if it does then add to either self safes or self mines

        for sent in self.knowledge:
            for other_sent in self.knowledge:
                #making sure we dont compare the same sentence
                if sent != other_sent:
                    set1 = sent.layout()[0]
                    set2 = other_sent.layout()[0]

                    if set1.issubset(set2):
                        #print("Sentence 1 is: " + str(sent))
                        #print("Sentence 2 is: " + str(other_sent))
                        inferred_sent = Sentence(set2-set1,other_sent.layout()[1]-sent.layout()[1])
                        #print("Our new sentence is: "+ str(inferred_sent))

                        #making sure we don't add repeats to self knowledge
                        if inferred_sent.known_safes() != None:
                            for i in inferred_sent.layout()[0]:
                                self.safes.add(i)
                                #print("New safe added")

                        elif inferred_sent.known_mines() != None:
                            for i in inferred_sent.layout()[0]:
                                self.mines.add(i)
                                #print("new mine added")


                        elif  inferred_sent.known_safes() == None and inferred_sent.known_mines() == None and inferred_sent.layout()[0]:
                            if inferred_sent not in self.knowledge:
                                #print("The appended sentence is: " + str(inferred_sent))
                                self.knowledge.append(inferred_sent)


        #visualizing what sentences we currently have
        knowledgearr =[]
        for sent in self.knowledge:
            knowledgearr.append(str(sent))
        #print("Our knowledge is currently: "+str(knowledgearr))


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        moves = self.safes - self.moves_made
        #print("Safe moves available: "+str(moves))

        if moves:
            move_taken = random.choice(tuple(moves))
            #print("safe move taken was: " + str(move_taken))
            return move_taken

        else:
            return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #generating the set of coordinates/moves
        new_set = set()
        for i in range(0,8):
            for j in range(0,8):
                new_set.add((i,j))
        #print("Our new set is: " + str(new_set))
        #print("New set length is: "+ str(len(new_set)))
        new_set = new_set - self.mines
        new_set = new_set - self.moves_made
        if new_set:
            choice = random.choice(tuple(new_set))
            #print("random move is: "+str(choice))
            return choice
        else:
            return None
