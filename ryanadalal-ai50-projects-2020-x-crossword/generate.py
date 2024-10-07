import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            remove = []
            for val in self.domains[var]:
                if var.length != len(val):
                    remove.append(val)
            for val in remove:
                self.domains[var].remove(val)
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        removal = []
        for xval in self.domains[x]:
            satisified = False
            for yval in self.domains[y]:
                assignment = dict()
                assignment[x] = xval
                assignment[y] = yval
                if self.consistent(assignment):
                    satisified = True
                    break
            if satisified == False:
                removal.append(xval)
                revised = True

        for val in removal:
            self.domains[x].remove(val)

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs
        if arcs == None:
            queue = self.getAllArcs()
        
        while len(queue) != 0:
            a = queue.pop()
            if self.revise(a[0], a[1]):
                if len(self.domains[a[0]]) == 0:
                    return False

                if self.getNeighbors(a[0]) != None:
                    for n in self.getNeighbors(a[0]):
                        if not n.__eq__(a[1]):
                            queue.append((n, a[0]))
        return True
    
    def getNeighbors(self, x):
        neighbors = []
        for var in self.crossword.variables:
            if (not var.__eq__(x)) and self.crossword.overlaps[x, var] != None:
                neighbors.append(var)
        
        return neighbors

    def getAllArcs(self):
        arcs = []
        for var1 in self.crossword.variables:
            for var2 in self.crossword.variables:
                if var1 != var2 and self.crossword.overlaps[var1, var2] != None:
                    arcs.append((var1, var2))
        return arcs

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment.keys() and assignment.get(var) == None:
                return False

        return True
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var1 in assignment.keys():
            if var1.length != len(assignment[var1]):
                return False
            for var2 in assignment.keys():
                if not var1.__eq__(var2):
                    overlap = self.crossword.overlaps[var1, var2]
                    if overlap != None and assignment[var1][overlap[0]] != assignment[var2][overlap[1]]:
                        return False
                    if assignment[var1] == assignment[var2]:
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def leastContrainValHeuristic(val):
            count = 0
            for neighbor in self.getNeighbors(var):
                if neighbor not in assignment:
                    for val2 in self.domains[neighbor]:
                        overlap = self.crossword.overlaps[var, neighbor]
                        if val[overlap[0]] != val2[overlap[1]]:
                            count += 1
            return count

        values = list(self.domains[var])
        values.sort(key=leastContrainValHeuristic)
        return values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        minimum = None
        for var in self.crossword.variables:
            if var not in assignment.keys():
                if minimum not in self.crossword.variables:
                    minimum = var
                if len(self.domains[var]) < len(self.domains[minimum]):
                    minimum = var
                elif len(self.domains[var]) == len(self.domains[minimum]):
                    if self.getNeighbors(var) != None and self.getNeighbors(minimum) != None:
                        if len(self.getNeighbors(var)) > len(self.getNeighbors(minimum)):
                            minimum = var
                    elif self.getNeighbors(var) != None and self.getNeighbors(minimum) == None:
                        minimum = var
        return minimum

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            checkAssign = assignment.copy()
            checkAssign[var] = value
            if self.consistent(checkAssign):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result != False:
                    return result
                del assignment[var]
        return False


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
