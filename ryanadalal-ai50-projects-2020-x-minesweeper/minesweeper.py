import itertools
import random
import copy

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

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count:
            return copy.deepcopy(self.cells)
        else:
            return set()

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            return copy.deepcopy(self.cells)
        else:
            return set()

        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if self.cells.__contains__(cell):
            self.count -= 1
            self.cells.remove(cell)

        #raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        if self.cells.__contains__(cell):
            self.cells.remove(cell)

        #raise NotImplementedError

    def getCount(self):
        return self.count

    def getCells(self):
        return self.cells

    def subtractSubset(self, cells2, count2):
        s1 = copy.deepcopy(self.cells)
        s2 = copy.deepcopy(cells2)
        n1 = copy.deepcopy(self.count)
        n2 = copy.deepcopy(count2)
        
        resultSet = set()
        for i in s1:
            equal = False
            for j in s2:
                equal = i == j
                if equal:
                    break
            if equal == False:
                resultSet.add(i)
        
        n1 -= n2

        return Sentence(resultSet, n1)


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
        #1
        self.moves_made.add(cell)
        
        #2
        self.mark_safe(cell)
        
        #3
        def checkCell(c):
            if c == cell:
                return False
            elif c[0] < 0 or c[0] >= self.height:
                return False
            elif c[1] < 0 or c[1] >= self.width:
                return False
            elif self.safes.__contains__(c):
                return False
            else:
                return True

        sentence_cells = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if checkCell((cell[0] + i, cell[1] + j)):
                    sentence_cells.add((cell[0] + i, cell[1] + j))
        self.knowledge.append(Sentence(sentence_cells, count))

        #4
        
        for i in self.knowledge:
            for j in i.known_mines():
                self.mark_mine(j)
            for k in i.known_safes():
                self.mark_safe(k)

        #5
        resultingSentences = []
        for i in self.knowledge:
            for j in self.knowledge:
                if i != j:
                    if i.getCells().issubset(j.getCells()):
                        r = j.subtractSubset(i.getCells(), i.getCount())
                        if len(r.getCells()) != 0 and resultingSentences.__contains__(r) == False and self.knowledge.__contains__(r) == False:
                            resultingSentences.append(r)

        
        for i in resultingSentences:
            self.knowledge.append(i)

        
        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for i in self.safes:
            if self.moves_made.__contains__(i) == False:
                return i
        return None

        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        for i in range(self.height):
            for j in range(self.width):
                if self.moves_made.__contains__((i, j)) == False and self.mines.__contains__((i, j)) == False:
                    return (i, j)
        return None
        raise NotImplementedError
