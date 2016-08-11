# Gregory Kehne

# This stack-based sudoku solver was inspired by Project Euler problem 96
# (https://projecteuler.net/problem=96)
# Its main method, 'solve(sudokufilename)', takes a .txt file containing
# sudokus as input and creates a .txt file 'solved_sudokufilename' of the
# solved puzzles.


# Returns a string representation of s
def stringSu(s):
    sustring = ""
    for i in range(0, len(s)):
        surow = ""
        for j in range(0, len(s[i])):
            surow = surow + " " + str(s[i][j])
        sustring = sustring + surow + '\n'
    return sustring


# Returns a deep copy of s.
def deepCopy(s):
    copy = []
    for i in range(0, 9):
        rowcopy = []
        for j in range(0, 9):
            rowcopy.append(s[i][j])
        copy.append(rowcopy)
    return copy


# This method reads multiple sudokus from the file 'sudokufilename', which
# must be in the same format as the file given by Project Euler (sudoku.txt)
def readSus(sudokufilename):
    list = []  # list of sudokus
    with open(sudokufilename, 'r') as file:
        i = 0  # line counter in the txt file
        current = []  # current sudoku being read in
        for line in file:
            if i % 10 == 0:
                current = []
            else:
                r = []  # current row in the current sudoku
                for n in range(0, 9):
                    r.append(int(line[n]))
                current.append(r)
            if i % 10 == 9:
                list.append(current)  # add the sudoku to the list of sudokus
            i = i + 1
    return list


# Initializes the possibility matrix corresponding to s. A number n is in the
# list at poss[i][j] if n is not entered anywhere in the same row, column, or
# box as the entry i,j
def possMatrix(s):
    poss = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            p = []
            if s[i][j] == 0:
                for n in range(1, 10):
                    if not (inRow(i, j, n, s) or
                            inCol(i, j, n, s) or
                            inBox(i, j, n, s)):
                        p.append(n)
            row.append(p)
        poss.append(row)
    return poss


# The following methods determine whether the number n in sudoku s is in the
# same row, column, or box as the entry i,j
def inRow(i, j, n, s):
    for d in range(0, 9):
            if s[i][d] == n:
                return True
    return False


def inCol(i, j, n, s):
    for d in range(0, 9):
            if s[d][j] == n:
                return True
    return False


def inBox(i, j, n, s):
    for c in range(3 * (i // 3), 3 * (i // 3) + 3):
        for d in range(3 * (j // 3), 3 * (j // 3) + 3):
            if s[c][d] == n:
                return True
    return False


# The following methods determine whether the number n in sudoku s
# is a possible entry for a (distinct) entry in the same row, column,
#  or box as the entry i,j
def inPossRow(i, j, n, poss):
    for d in range(0, 9):
            if not d == j and n in poss[i][d]:
                return True
    return False


def inPossCol(i, j, n, poss):
    for d in range(0, 9):
            if not d == i and n in poss[d][j]:
                return True
    return False


def inPossBox(i, j, n, poss):
    for c in range(3 * (i // 3), 3 * (i // 3) + 3):
        for d in range(3 * (j // 3), 3 * (j // 3) + 3):
            if (not (c == i and d == j)) and n in poss[c][d]:
                return True
    return False


# This determines if s is solved
def solved(s):
    for i in range(0, 9):
        for j in range(0, 9):
            if s[i][j] == 0:
                return False
    return True


# This determines if there is an unsatisfiable spot in s, based on its poss
def broken(s, poss):
    for i in range(0, 9):
        for j in range(0, 9):
            if s[i][j] == 0 and len(poss[i][j]) == 0:
                return True
    return False


# OUTLINE FOR SOLVESU METHOD:
#     for each sudoku, push it onto its own stack
#         pop a sudoku off of the stack
#
#         while the sudoku isnt solved, and while progress is being made,
#             make logical moves, and trim decision tree
#
#             if the sudoku is impossible ("LOGIC IS BROKEN" condition),
#             then pop from the stack and discard it.
#
#         if the sudoku is solved, return it!
#         if it isnt solved, but no progress is being made, look for an
#         entry with a small possibilities list, push the sudokus with all
#         of those guesses onto the stack
def SOLVESU(s):
    stack = []
    stack.append(s)
    cur = s  # current sudoku
    while not solved(cur):
        if len(stack) == 0:
            print("ERROR: empty")
            quit
        elif len(stack) > 1000:
            print("STACK IS HUUUUGE!")
            quit

        cur = stack.pop()  # get the next sudoku from the stack

        poss = possMatrix(cur)  # creates the corresponding su of possibilities

        # make logical moves on cur:
        prog = True  # this ensures progress on logically solving s
        while prog and not broken(cur, poss):
            prog = False
            for i in range(0, 9):
                for j in range(0, 9):
                    if cur[i][j] == 0 and not prog:
                        if len(poss[i][j]) == 1:
                            cur[i][j] = poss[i][j][0]
                            poss = possMatrix(cur)
                            prog = True
                        else:
                            if len(poss[i][j]) > 1:
                                for n in poss[i][j]:
                                    if (not inPossRow(i, j, n, poss) or
                                            not inPossCol(i, j, n, poss) or
                                            not inPossBox(i, j, n, poss)):
                                        cur[i][j] = n
                                        poss = possMatrix(cur)
                                        prog = True
        # time to make a guess on an entry:
        if not solved(cur) and not broken(cur, poss):
            # select an unsolved entry for which to guess all possibilities:
            choice = False
            l = 1  # the number of choices to explore for the guess
            r = 0  # the row coordinate at which the guess will be made
            c = 0  # the column coordinate at which the guess will be made
            while not choice:
                l = l + 1
                for i in range(0, 9):
                    for j in range(0, 9):
                        if len(poss[i][j]) == l:
                            choice = True
                            r = i
                            c = j
            # push the sudokus with the guesses made onto the stack:
            for n in poss[r][c]:
                guesssu = deepCopy(cur)
                guesssu[r][c] = n
                stack.append(guesssu)
                # print('push')
    return cur


# This is the main method.
# This creates a corresponding .txt file with the solved sudokus in it
def solve(sudokufilename):
    sus = readSus(sudokufilename)
    # write the solutions to file:
    with open("solved_" + sudokufilename, 'w') as file:
        for i in range(len(sus)):
            x = SOLVESU(sus[i])
            file.write("Sudoku " + str(i + 1) + ":" + '\n' +
                        stringSu(x) + '\n')  # headers to the sudokus


# This answers the original Project Euler question (given their input file).
def answerQuestion(sudokufilename):
    sus = readSus(sudokufilename)
    count = 0
    solvedcount = 0
    for s in sus:
        x = SOLVESU(s)
        solved = 1
        for n in range(0, 9):
            for m in range(0, 9):
                if x[n][m] == 0:
                    solved = 0
        # The problem asks for the sum of the first 3 digits, considered
        # as a single number, from each sudoku.
        solvedcount = solvedcount + solved
        count = count + 100 * x[0][0] + 10 * x[0][1] + x[0][2]
    print("Number of sodukus solved: " + str(solvedcount) + "/50")
    print("Sum of 3-digit numbers from the upper left boxes: " + str(count))


# Default behavior: solve the "sudoku.txt" file of sudokus.
if __name__ == '__main__':
    solve("sudoku.txt")

