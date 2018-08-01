####Imports####
from datetime import datetime

####Functions####
#Fill coordinate matrix of puzzle
def fillHelper(helper, n2):
    for i in range(0, n2):
        #i = an + b
        b = i%n
        a = (i-b)/n
        #[column, row, horizontal square number, vertical square number]
        helper += [[int(b), int(a), int((b-b%m)/m), int((a-a%m)/m)]]

#Check puzzle state validity
def isValid(sudoku):
    for i in range(0, n2):
        for j in range(i+1, n2):
            if sudoku[i] != "." and sudoku[i] == sudoku[j]:
                if helper[i][0] == helper[j][0] or helper[i][1] == helper[j][1] or (helper[i][2] == helper[j][2] and helper[i][3] == helper[j][3]):
                    return False
    return True

#Check if the puzzle state is a solution
def isSolution(sudoku):
    return (sudoku.find('.') == -1 and isValid(sudoku))

#Replace a '.' by all possible numbers to create a set of possible solution approximations
def assessOptions(options):
    sudoku = options[0]
    o_new = []
    for i in range(0, n2):
        if sudoku[i] == '.':
            for j in range(0, n):
                s_new = sudoku[:i] + str(j+1) + sudoku[(i+1):]
                if isValid(s_new):
                    o_new += [s_new]
            break
    return o_new + options[1:]

####Execute####
#Enter puzzle
fname = input('Enter the file name: ')
try:
    if fname == '':
        fname = 'sample.txt'
    fhand = open(fname)
except:
    print('File cannot be opened:', fname)
    quit()

#Basic parameters
puzzle = fhand.read()
n2 = len(puzzle)
n = int(n2**0.5)
m = int(n**0.5)
options = [puzzle]
helper = []

#Close File
fhand.close()

#Time
start_time = datetime.now()

print("Puzzle sizes: # of fields: " + str(n2) + ", row length: " + str(n) + ", square size: " + str(m))

#Preliminary checks
fillHelper(helper, n2)

if not isValid(options[0]):
    print("The sudoku puzzle is invalid!")
    quit()

if not isSolution(options[0]):
    print("The sudoku puzzle is not yet a solution.")
else:
    print("The sudoku puzzle is already a solution!")
    quit()

#Investigate Options
while len(options) > 0 and options[0].find('.') != -1:
    options = assessOptions(options)

#Post-check & print solution
if len(options) == 0:
    print("No solution found!")
else:
    print("Solution is: "+options[0])
    fnamesplit = str(fname).split('.')
    fsolname = fnamesplit[0] + '_solution.' + fnamesplit[1]
    fhand = open(fsolname, "w")

    for j in range(0, n):
        if (j%m) == 0:
            fhand.write("-")
        fhand.write("--")
    fhand.write("--\n")

    for i in range(0, n2):
        if (i%m) == 0:
            fhand.write("|")

        fhand.write("|"+str(options[0][i]))

        if (i+1)%n == 0:
            fhand.write("||\n")
            for j in range(0, n):
                if (j%m) == 0:
                    fhand.write("-")
                fhand.write("--")
            fhand.write("--\n")

    fhand.close()

#Print timing
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
