#Dev: Sean Balakhanei

from flask import Flask, render_template, redirect, request, url_for
import algorithm_revised, random

app = Flask(__name__)
difficulty = []
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST", "GET"])
def get_input():
    global difficulty
    # Creating matrix of spots algorithmically
    input = [[]]*9
    spots = [[]]*9
    y_axis = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    for i in range(len(spots)):
        spots[i] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        input[i] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    for i in range(9):
        for j in range(len(spots[i])):
            spots[i][j] += y_axis[i]
            input[i][j] += y_axis[i]
    
    # Getting input from user and storing in input matrix
    for i in range(len(spots)):
        for j in range(len(spots[i])):
            input[j][i] = (request.form[spots[i][j]])
            if input[j][i] == '':
                input[j][i] = 0
            input[j][i] = int(input[j][i])

    solution = algorithm_revised.solve(input)

    # If the board is user input, we cannot determine the difficulty
    if len(difficulty) == 0:
        difficulty = ["N/A", "black"]

    # If a solution exists, display it.
    # If the input puzzle is invalid, display Invalid Input
    # If there puzzle is valid, but there is no solution, display No Solution
    if solution[0] > 0:
        x = difficulty
        difficulty = []
        return render_template("solve.html", solution=solution, difficulty=x)
    else:
        type = "No Solution"
        x = difficulty
        difficulty = []
        return render_template("unsolvable.html", solution=[-1]*81, difficulty=x, type=type)

# Back to home page when user wants to input a new puzzle
def start_again():
    global difficulty
    difficulty = []
    return render_template("index.html")

# Display a computer generated board to be solved
# 25% of the time, the board will be generated randomly (odds are there will be no solution)
# To make this function more practical, 75% of the time a solvable Sudoku puzzle will be displayed

# Note: Given that generating solvable Sudoku puzzles is np complete, the solvable puzzles output by
# the "Generate Puzzle" function will be manually selected from several pre-defined puzzles
@app.route("/generate_board", methods=["POST"])
def generate_board():
    global difficulty
    input = ['1']*81
    num = random.randint(1, 4)
    if num == 1:
        # On average we're going to fill 3-4 boxes in each column with numbers 1-9
        # There may be overlap if the same position is selected twice, but it's not a big deal
        # Since the number of boxes is constant, O(1) time & space
        difficulty = ["Random", "black"]
        input = [0]*81
        for i in range(32):
            position = random.randint(0, 80)
            num = random.randint(1, 9)
            input[position] = num
    else:
        puzzle_number = random.randint(1, 8)
        if puzzle_number == 1:
            # Self-made puzzle (equivalent of Medium difficulty)
            difficulty = ["Medium", "orange"]
            input =[0,0,0,5,6,0,7,0,4,
                    6,8,0,0,7,0,0,9,0,
                    4,9,0,0,0,1,2,0,0,
                    8,5,0,4,0,0,0,1,0,
                    0,0,1,6,0,5,9,0,0,
                    0,2,0,0,0,3,0,5,8,
                    0,0,9,3,0,0,0,7,1,
                    0,1,0,0,2,0,0,3,6,
                    7,0,3,0,4,8,0,0,0]
        elif puzzle_number == 2:
            # Easy puzzle from Sudoku.com
            difficulty = ["Easy", "green"]
            input = [0,3,4,7,0,6,0,0,0,
                     0,0,0,0,5,0,2,0,0,
                     7,5,0,0,0,0,0,0,4,
                     9,7,0,2,6,1,0,4,8,
                     3,8,2,0,4,7,0,5,1,
                     0,0,6,0,0,0,0,9,2,
                     0,0,3,0,0,0,0,0,7,
                     8,0,0,5,0,2,4,0,0,
                     0,0,0,0,7,9,8,0,6]
        elif puzzle_number == 3:
            # Medium puzzle from Sudoku.com
            difficulty = ["Medium", "orange"]
            input = [7,0,8,0,0,1,4,0,0,
                     3,0,0,4,0,0,0,0,0,
                     0,9,4,5,0,0,0,7,6,
                     2,7,0,6,0,8,0,0,0,
                     6,0,3,0,0,0,7,0,2,
                     0,0,0,7,0,0,1,6,0,
                     0,0,0,0,5,4,0,0,1,
                     4,1,5,0,0,0,8,2,7,
                     0,0,0,0,0,0,0,0,4]
        elif puzzle_number == 4:
            # Hard puzzle from Sudoku.com
            difficulty = ["Hard", "red"]
            input = [0,9,0,0,0,0,0,6,0,
                     0,0,7,0,1,5,0,4,0,
                     0,0,4,6,0,3,1,0,0,
                     0,0,0,0,0,0,0,2,0,
                     9,0,0,0,5,0,0,0,3,
                     0,7,6,0,0,0,0,5,0,
                     0,0,0,0,3,2,6,0,0,
                     0,1,0,5,0,0,0,3,0,
                     0,5,0,7,0,4,2,0,9]
        elif puzzle_number == 5:
            # Expert puzzle from Sudoku.com
            difficulty = ["Expert", "purple"]
            input = [0,3,0,1,0,0,4,0,0,
                     0,0,6,0,0,0,0,5,3,
                     0,0,0,0,0,6,0,0,0,
                     9,0,4,0,0,0,5,0,0,
                     2,0,0,0,3,0,0,0,9,
                     0,0,0,0,4,0,8,0,0,
                     0,2,0,7,0,0,0,8,0,
                     5,0,0,9,2,8,0,0,0,
                     0,0,0,0,0,0,0,6,0]
        elif puzzle_number == 6:
            # Expert puzzle from Sudoku.com
            difficulty = ["Expert", "purple"]
            input = [5,8,6,4,0,0,0,0,3,
                     0,0,0,0,8,0,0,0,4,
                     0,0,0,9,0,0,0,0,7,
                     0,0,0,0,0,0,0,4,0,
                     0,0,0,0,0,9,7,2,0,
                     0,3,0,0,5,0,0,0,1,
                     7,0,0,0,0,0,0,6,0,
                     0,5,0,0,3,2,0,0,0,
                     2,0,0,0,6,0,0,0,0]
        elif puzzle_number == 7:
            # Hard puzzle from Sudoku.com
            difficulty = ["Hard", "red"]
            input = [1,0,0,0,3,0,4,0,0,
                     0,0,9,7,0,0,0,0,0,
                     0,0,0,1,0,6,0,0,3,
                     6,0,0,9,8,0,0,0,1,
                     0,0,3,0,0,0,0,0,9,
                     5,0,0,6,1,0,0,0,0,
                     0,0,0,0,0,0,0,6,2,
                     9,8,2,0,0,0,3,0,4,
                     7,3,0,0,2,0,0,8,0]
        elif puzzle_number == 8:
            # Hard puzzle from Sudoku.com
            difficulty = ["Easy", "green"]
            input = [0,4,0,6,0,2,0,3,1,
                     0,0,0,0,0,1,6,0,9,
                     6,0,0,5,4,0,8,2,7,
                     0,0,2,7,6,0,0,8,0,
                     5,0,6,0,0,0,0,7,4,
                     0,8,7,0,0,5,0,6,2,
                     1,6,0,0,8,0,0,5,0,
                     8,2,0,0,0,7,0,9,0,
                     7,0,0,0,0,6,2,0,0]

    # "Clean" data for HTML
    for i in range(len(input)):
        if input[i] <= 0:
            input[i] = ''
        else:
            input[i] = str(input[i])

    return render_template("index_generated.html", input=input, difficulty=difficulty)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')