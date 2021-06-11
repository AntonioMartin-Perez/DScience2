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
        for var in self.domains:
            # print('variable:', var)
            domain = self.domains[var].copy()    # Copio el dominio para no entrar en conflicto de iterar y modificar
            # print('variable domain: ',domain)
            for word in domain:
                if len(word) != var.length:
                    self.domains[var].remove(word)

        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        xDomain = self.domains[x].copy()
        yDomain = self.domains[y].copy()
        overlap = self.crossword.overlaps[(x,y)] # The pair (i, j) should be interpreted to mean that the ith character of v1’s value must be the same as the jth character of v2’s value.
        for word in xDomain:
            compatible = False
            for word2 in yDomain:
                if word[overlap[0]] == word2[overlap[1]]:
                    compatible = True
                    break
            if not compatible:
               self.domains[x].remove(word)
               revised = True         
        return revised
        # raise NotImplementedError

    def ac3(self, arcs=None): # each arc is a tuple (x, y) of a variable x and a different variable y
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Generate all arcs in csp
        if arcs == None:
            arcs = list()
            for var in self.domains.keys():
                for neighbor in self.crossword.neighbors(var):
                    arcs.append(
                        (var,neighbor)
                    )

        # Enforce arc consistency one by one
        while len(arcs) != 0:
            (x,y) = arcs.pop()              # variables x and y that compose the arc
            if self.revise(x,y):
                if len( self.domains[x] ) == 0:
                    # print(False)
                    # break
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.append(
                            (neighbor, x)
                        )
        return True
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        complete = True
        for var in self.crossword.variables:
            if var not in assignment.keys() or len( assignment[var] ) == 0:
                complete = False
        
        return complete
        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        s = set()
        for word in assignment.values():
            s.add(word)
        if len(s) != len(assignment.values()):
            return False
        
        self.enforce_node_consistency()
        self.ac3()

        for variable in assignment.keys():
            if assignment[variable] not in self.domains[variable]:
                return False
                
            neighbors = self.crossword.neighbors(variable)
            for neighbor in neighbors:
                if neighbor in assignment.keys():
                    (overlapVar,overlapNeighbor) = self.crossword.overlaps[variable,neighbor]
                    if assignment[variable][overlapVar] != assignment[neighbor][overlapNeighbor]:
                        return False

        return True
        # raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        orderedDomain = []
        varDomain = self.domains[var].copy()
        # varDomain.add('whatever')                     # Test
        neighborDomain = []
        
        # store neighbor values in NeighborDomain
        for neighbor in self.crossword.neighbors(var):
            # print(creator.domains[neighbor])
            if neighbor not in assignment.keys():
                neighborDomain.append(self.domains[neighbor] )
            # neighborDomain.append({'SEVEN'})              # Test

        # print('neighborDomain = ',neighborDomain)

        # count how many times a word appears in the neighborhood
        for word in varDomain:
            count = 0
            for domain in neighborDomain:
                for word2 in domain:
                    if word == word2:
                        count += 1
            orderedDomain.append(
                (word,count)
            )
        
        def takeSecond(elem):
            return elem[1]

        orderedDomain.sort(key = takeSecond)

        # print("orderedDomain =", orderedDomain)

        def takeFirst(elem):
            return elem[0]

        # print( list( takeFirst(element) for element in orderedDomain) )
        return list( takeFirst(element) for element in orderedDomain) 

        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        assignedVariables = set( assignment.keys() )
        
        possibleVariables = []
        for variable in self.domains.keys():
            if variable not in assignedVariables:
                possibleVariables.append(
                    ( variable , len( self.domains[variable] ) , len(self.crossword.neighbors(variable)) )    # var, number of remaining values in its domain, degree
                )

        # def takeSecond(elem):
        #     return elem[1]
        # def takeThird(elem):
        #     return elem[2]

        # possibleVariables.sort(key = takeThird, reverse = True)         # order by highest degree
        # possibleVariables.sort(key = takeSecond)                        # order by lowest remaining value

        possibleVariables.sort(key = lambda x: (x[1],x[2]))               # Order list according to two fields

        return  possibleVariables[0][0]
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        
        # new_assignment = assignment.copy()
        # new_assignment[var]...
        var = self.select_unassigned_variable(assignment)
        varOrderedDomain = self.order_domain_values(var,assignment)
        new_assignment = assignment.copy()
        for value in varOrderedDomain:
            new_assignment[var] = value
            if self.consistent(new_assignment) and value not in assignment.values():
                assignment[var] = value

                # print()
                # print('assignment: ',assignment)
                # print()
                # # print('domains: ', self.domains[list(assignment.keys())[-1]])
                # print('domains: ', len( self.domains[list(assignment.keys())[-1]] ) ) 


                result = self.backtrack(assignment)
                if result != False:
                    return result
                # assignment.pop(var) Ya no hace falta (creo)
            new_assignment.pop(var)
        return False
        # raise NotImplementedError


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



"""
######################################### Testing ######################################

structure   =   "data\\structure2.txt"
words       =   "data\\words2.txt"

# Generate crossword
crossword = Crossword(structure, words)
creator = CrosswordCreator(crossword)

# creator.enforce_node_consistency()  # enforces unary constraints checking length
# creator.ac3()                       # enforces binary constraints revising each arc
# assignment = creator.solve()


a = {
 Variable(0, 1, 'down', 5): 'SEVEN',    
#  Variable(0, 1, 'down', 5): 'EIGHT',    
 Variable(1, 4, 'down', 4): 'NINE',
#  Variable(1, 4, 'down', 4): 'FIVE',
 Variable(0, 1, 'across', 3): 'SIX',
 Variable(4, 1, 'across', 4): 'NINE'
}
b = {
#  Variable(0, 1, 'down', 5): 'SEVEN',    
#  Variable(0, 1, 'down', 5): 'EIGHT',    
#  Variable(1, 4, 'down', 4): 'NINE',
#  Variable(1, 4, 'down', 4): 'FIVE',
#  Variable(0, 1, 'across', 3): 'SIX',
#  Variable(4, 1, 'across', 4): 'NINE'
}

# creator.assignment_complete(a)
# creator.consistent(a)

# var = list(creator.domains.keys() )[0]
# var = list(a.keys() )[0]
# creator.order_domain_values(var,a)

# creator.select_unassigned_variable(b)
# creator.backtrack(b)
c = creator.solve()
# c = {Variable(0, 6, 'down', 6): 'ASSUME', Variable(5, 1, 'across', 3): 'TOE', Variable(1, 3, 'down', 5): 'SHOOT', Variable(2, 3, 'across', 4): 'BEAT', Variable(1, 0, 'down', 4): 'POOR', Variable(1, 0, 'across', 4): 'INTO'}
# print(c)
creator.print(c)

# C:/Users/yomis/anaconda3/envs/DataScience/python.exe c:/Users/yomis/OneDrive/WiP/CS50ai/crossword/generate.py data\structure0.txt data\words0.txt
# """