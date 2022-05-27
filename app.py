#Dev: Sean Balakhanei

from flask import Flask, render_template, redirect, request, url_for
import algorithm

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST", "GET"])
def get_input():
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

    # Creating CSP object and calling backtracking algo
    csp = algorithm.CSP(input)
    csp.eliminate_domain_values()
    assignment = algorithm.backtracking_search(csp)[1]
    isSuccess = algorithm.backtracking_search(csp)[0]
    solution = algorithm.convert_1D_array(input, assignment, isSuccess)


    # If a solution exists, display it. Otherwise, the input is invalid.
    if isSuccess:
        return render_template("solve.html", solution=solution)
    else:
        return render_template("unsolvable.html", solution=input)

def start_again():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
