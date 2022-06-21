# AI_Sudoku_Solver
Link to Project: https://flasksudokusolver.com/

Initial Implementation: Implements backtracking search algorithm using MRV and degree heuristics for the variable selection process to solve a given sudoku problem by the user. Algorithm's efficiency was improved by forward checking inferencing during search and AC-3 algorithm preprocessing prior to search.

Revised Implementation: Original implementatation of this approach is credited to Dante Sblendorio. Takes an iterative approach to solving the sudoku puzzle. Needed to add functions to the original implementation that check if the input puzzle was valid and if the final puzzle was solved. In addition, needed to add a function that flattens the 2D numPy array to a 1D array


Runtime Test Procedure:

1. Data Gathering: A sample of 9 million sudoku problems were downloaded (.csv file) from Kaggle's Sudoku Dataset (courtesy of Vopani) - https://www.kaggle.com/datasets/rohanrao/sudoku. Panda library was utilized to retrieve only the first 100 sudoku problems and store it in a data_frame
2. Testing: Each puzzle in the data frame was tested on both of the algorithms (initial implementation and revised implementation), independently. The puzzle ID and the runtime were stored in a dictionary while the search algorithm was running.
3. Analysis: The average runtime for each algorithm was taken. The percent change was calculated to be 1520%. 

*Raw data in runtime_test folder

*Note: We undertsand that the runtime for each puzzle will vary between computer to computer; however, the test was done to demonstrate the overall efficiency of the newer algorithm implementation.

The frontend of the web app was developed in HTML and CSS, while the backend was developed using Python/Flask. The web app was hosted on GitHub pages and deployed using AWS.
