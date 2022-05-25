#!/usr/bin/python3
# Author: Shubh Savani
# Date Due: 05/12/22
# Date Submitted: 05/24/22

import argparse  # so we can parse the command line
import sys  # so we can write the output file


# Variable Class
class Variable:
    # constructor
    def __init__(self, value, location, domain):
        self.value = value
        self.location = location
        self.domain = domain
        self.block_num = self.find_block_number()  # Uses the row and column to find the block number

    # Getter methods
    def get_value(self):
        return self.value

    def get_location(self):
        return self.location

    def get_domain(self):
        return self.domain

    def get_block_num(self):
        return self.block_num

    # Setter Methods
    def update_value(self, new_value):
        self.value = new_value

    def update_domain(self, value):
        self.domain.remove(value)

    # Auxiliary methods
    def __str__(self):
        return "(" + str(self.location[0]) + ", " + str(self.location[1]) + ") = " + str(self.value)

    def __eq__(self, other):  # Returns true if the two variables have the same location (row and column) in the puzzle
        self_row = self.location[0]
        self_col = self.location[1]
        other_row = other.location[0]
        other_col = other.location[1]
        return self_row == other_row and self_col == other_col

    def __ne__(self, other):  # Returns true if the are not in the same location
        self_row = self.location[0]
        self_col = self.location[1]
        other_row = other.location[0]
        other_col = other.location[1]
        return self_row != other_row or self_col != other_col

    def find_block_number(self):  # uses the row and column to assign a block number to a variable
        row = self.location[0]
        col = self.location[1]
        if 0 <= row <= 2:
            if 0 <= col <= 2:
                block_num = 0
            elif 3 <= col <= 5:
                block_num = 1
            elif 6 <= col <= 8:
                block_num = 2
        elif 3 <= row <= 5:
            if 0 <= col <= 2:
                block_num = 3
            elif 3 <= col <= 5:
                block_num = 4
            elif 6 <= col <= 8:
                block_num = 5
        else:
            if 0 <= col <= 2:
                block_num = 6
            elif 3 <= col <= 5:
                block_num = 7
            elif 6 <= col <= 8:
                block_num = 8
        return block_num


# Constraint Class
class Constraint:  # Manages a set of variables that cannot equal each other since they are in the same unit
    def __init__(self, variables):
        self.variables = variables  # list of variables involved in the constraint

    # Getter methods
    def get_variables(self):
        return self.variables

    # Setter methods
    def update_constraint(self, variable):  # Adds a variable to the constraint
        self.variables.append(variable)

    # Auxiliary methods
    def __str__(self):
        output = "{"
        for variable in self.variables:
            output += str(variable) + ", "
        output += "}"
        return output

    def __len__(self):
        return len(self.variables)

    def __eq__(self, other):  # checks for equality if they have the same variables in the constraint
        self_var1 = self.variables[0]
        self_var2 = self.variables[1]
        other_var1 = other.variables[0]
        other_var2 = other.variables[1]
        return (self_var1 == other_var1 and self_var2 == other_var2) or (self_var1 == other_var2 and self_var2 ==
                                                                         other_var1)

    def is_Consistent(self, new_value):
        variable_values = [var.get_value() for var in self.variables]
        return new_value not in variable_values


# ConstraintCollection class
class ConstraintCollection:  # holds all the constraints in the CSP
    def __init__(self, collection):
        self.constraints = collection  # holds of list of constraints

    # Getter methods
    def get_collection(self):
        return self.constraints

    # Setter methods
    def update_collection(self, constraint):  # adds a constraint to the array
        self.constraints.append(constraint)

    def constraint_exists(self, constraint):  # checks if a constraint already exists in the array - to avoid repeats
        for constraint_ind in range(len(self.constraints)):
            existing_constraint = self.constraints[constraint_ind]
            if constraint == existing_constraint:
                return True
        return False

    def find_var_constraints(self, unassigned_var):  # given an unassigned var, a list of constraints will
        # output that the var is involved with
        var_constraints = []
        for constraint_ind in range(len(self.constraints)):
            constraint = self.constraints[constraint_ind]
            constraint_variables = constraint.get_variables()
            for var_ind in range(len(constraint)):
                var = constraint_variables[var_ind]
                if unassigned_var == var:
                    var_constraints.append(constraint)
        return var_constraints

    def have_Constraint(self, var1, var2):  # checks the database of constraints to see
        # if two variables have constraints with each other
        var1_constraints = self.find_var_constraints(var1)
        for ind in range(len(var1_constraints)):
            constraint = var1_constraints[ind]
            constraint_vars = constraint.get_variables()
            for var_ind in range(len(constraint_vars)):
                const_var = constraint_vars[var_ind]
                if var2 == const_var:
                    return True
        return False


class Assignment:  # manages the list of assignments given to each variable during the backtracking algorithm search
    def __init__(self, initial):
        self.assignments = initial

    def get_assignments(self):
        return self.assignments

    def add_assignment(self, var):  # adds a variable to the assignment list
        self.assignments.append(var)

    def remove_assignment(self, var):  # removes an assignment, if there is a failure that occurs
        var.update_value(0)
        self.assignments.remove(var)

    def __len__(self):
        return len(self.assignments)

    def is_Consistent(self, var, constraint_network):  # checks if the variable value is consistent
        # with the previous assignment values
        for ind in range(len(self.assignments)):
            past_assignment = self.assignments[ind]
            if constraint_network.have_Constraint(var, past_assignment):
                past_assignment_val = past_assignment.get_value()
                var_val = var.get_value()
                if past_assignment_val == var_val:
                    return False
        return True

    def __str__(self):
        output = ""
        if len(self) == 0:
            return "{}"
        for var_ind in range(len(self.assignments)):
            variable = self.assignments[var_ind]
            output += str(variable) + ", "
        return output


class CSP:
    def __init__(self, puzzle):  # keeps track of the entire CSP
        self.unassigned_vars = []
        self.assigned_vars = []
        self.num_vars = 0
        self.blocks = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        self.rows = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        self.columns = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        self.constraint_collection = ConstraintCollection([])

        for row in range(len(puzzle)):  # Traverses through the puzzle and creates/stores
            # unassigned and assigned variables in the given puzzle
            for col in range(len(puzzle[row])):
                value = puzzle[row][col]
                location = row, col
                if value == 0:  # if so, then the variable is unassigned
                    domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    unassigned_var = Variable(value, location, domain)

                    self.num_vars += 1  # keeps track of the number of unassigned vars from the beginning
                    # (before the backtracking search algorithm starts)

                    # Store the variable in the correct block, row, and column
                    block_num = unassigned_var.get_block_num()
                    self.blocks[block_num].append(unassigned_var)
                    self.rows[row].append(unassigned_var)
                    self.columns[col].append(unassigned_var)
                    self.unassigned_vars.append(unassigned_var)
                else:  # the variable already has a value from the beginning. Need to store as an assigned variable
                    domain = [value]
                    assigned_var = Variable(value, location, domain)
                    self.assigned_vars.append(assigned_var)

        for unassigned_ind in range(len(self.unassigned_vars)):  # goes through each unassigned variable and
            # creates constraints for each variable with other unassigned vars
            # by searching through the block, row, and column that it is in
            variable = self.unassigned_vars[unassigned_ind]
            var_row = variable.get_location()[0]
            var_col = variable.get_location()[1]
            var_block_num = variable.get_block_num()

            # Add neighbor variables from each unit into list of unassigned vars that have constraints with this var
            neighbor_vars = []
            for neighbor_ind in range(len(self.blocks[var_block_num])):  # Traverses through each block in search
                # and add each neighbor that isn't variable to the list of vars that have a constraint with variable
                neighbor = self.blocks[var_block_num][neighbor_ind]
                if variable != neighbor:
                    neighbor_vars.append(neighbor)
            for neighbor_ind in range(len(self.rows[var_row])):  # does the same for all row that the
                # unassigned var is in
                neighbor = self.rows[var_row][neighbor_ind]
                if variable != neighbor:
                    neighbor_vars.append(neighbor)
            for neighbor_ind in range(len(self.columns[var_col])):  # same process for the column the var is in
                neighbor = self.columns[var_col][neighbor_ind]
                if variable != neighbor:
                    neighbor_vars.append(neighbor)

            for neighbor_ind in range(len(neighbor_vars)):  # traverses through each neighbor
                # and creates a new constraint. Adds constraint to the constraint collection
                neighbor = neighbor_vars[neighbor_ind]
                new_constraint = Constraint([variable, neighbor])
                if not self.constraint_collection.constraint_exists(new_constraint):  # checks the constraint network
                    # to see if the constraint does not already exist
                    self.constraint_collection.update_collection(new_constraint)

    def __len__(self):
        return self.num_vars

    def get_constraint_collection(self):
        return self.constraint_collection

    def select_unassigned_var(self):  # selects a new variable based on the MRV heuristic and degree heuristics
        next_var = None
        for ind in range(len(self.unassigned_vars)):
            ordered_domains = self.minimum_remaining_values()  # uses MRV to find all the domain lengths
            # for each unassigned variable

            length = 1  # starts with the variables with the smallest domain
            next_var_found = False
            while not next_var_found:
                candidates = ordered_domains[length]  # retrieves the singular var or list of variables
                # that have a domain of that length
                if len(candidates) > 1:  # checks if multiple variables have the same domain length - there's a tie
                    next_var = self.degree_heuristic(candidates)  # if so, degree heuristics is used to
                    # find the next var
                    next_var_found = True
                elif len(candidates) == 1:  # in the case there is no tie
                    next_var = candidates[0]
                    next_var_found = True
                else:  # if there are no variables with that domain length
                    length += 1
        return next_var

    def degree_heuristic(self, domain_lengths):  # chooses the most constrained variable given a list of variables
        # that were tied in terms of domain lengths
        constraints = self.count_constraints(domain_lengths)  # retrieves a dict of all of the variables
        # associated with the number of constraints each of them hold with other unassigned vars

        next_var = None
        max_num_constraints = -1
        for constraint_num in constraints.keys():
            if constraint_num >= max_num_constraints:
                max_num_constraints = constraint_num
        next_var_found = False
        while not next_var_found:
            max_constraint_vars = constraints[max_num_constraints]
            if len(max_constraint_vars) >= 1:
                next_var = max_constraint_vars[len(max_constraint_vars) - 1]
                max_constraint_vars.pop()
                next_var_found = True
            else:
                max_num_constraints -= 1
        return next_var

    def count_constraints(self, tied_vars):
        var_constraints = {}
        for var_ind in range(len(tied_vars)):
            var = tied_vars[var_ind]
            count = len(self.constraint_collection.find_var_constraints(var))
            if count not in var_constraints.keys():
                var_constraints[count] = [var]
            else:
                var_constraints[count].append(var)
        return var_constraints

    def eliminate_domain_values(self):
        for unassigned_var_ind in range(len(self.unassigned_vars)):
            unassigned_var = self.unassigned_vars[unassigned_var_ind]
            for assigned_var_ind in range(len(self.assigned_vars)):
                assigned_var = self.assigned_vars[assigned_var_ind]
                assigned_var_row = assigned_var.get_location()[0]
                assigned_var_col = assigned_var.get_location()[1]
                assigned_var_block_num = assigned_var.get_block_num()

                unassigned_var_row = unassigned_var.get_location()[0]
                unassigned_var_col = unassigned_var.get_location()[1]
                unassigned_var_block_num = unassigned_var.get_block_num()

                if unassigned_var_row == assigned_var_row or unassigned_var_col == assigned_var_col or \
                        unassigned_var_block_num == assigned_var_block_num:
                    assigned_var_value = assigned_var.get_value()
                    unassigned_var_domain = unassigned_var.get_domain()
                    if assigned_var_value in unassigned_var_domain:
                        unassigned_var.update_domain(assigned_var_value)

    def minimum_remaining_values(self):
        domains_ordered = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
        for var_ind in range(len(self.unassigned_vars)):
            var = self.unassigned_vars[var_ind]
            domain_length = len(var.get_domain())
            domains_ordered[domain_length].append(var)
        return domains_ordered

    def remove_unassigned_var(self, unassigned_var):
        for var_ind in range(len(self.unassigned_vars)):
            if unassigned_var == self.unassigned_vars[var_ind]:
                self.unassigned_vars[var_ind], self.unassigned_vars[len(self.unassigned_vars) - 1] = \
                    self.unassigned_vars[len(self.unassigned_vars) - 1], self.unassigned_vars[var_ind]
        self.unassigned_vars.pop()

    def add_unassigned_var(self, unassigned_var):
        self.unassigned_vars.append(unassigned_var)


# Parsing CSP Arc ----------------------------------------------------------------------------------------------------


def file_reader(file_name):
    puzzle = []
    file = open(file_name)
    for ind in range(9):
        line = file.readline()
        row = line.split()
        puzzle.append(row)
    # convert each value in puzzle from a string to an integer
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            val_str = puzzle[row][col]
            puzzle[row][col] = int(val_str)
    return puzzle


def apply_solution(puzzle, assignment):
    for var_ind in range(len(assignment.get_assignments())):
        variable = assignment.get_assignments()[var_ind]
        var_row = variable.get_location()[0]
        var_col = variable.get_location()[1]
        puzzle[var_row][var_col] = variable.get_value()
    print_puzzle(puzzle)


def write_output_file(input_file_name, puzzle, assignment):
    input_num = int(input_file_name[5])
    output_file_name = f"Output{input_num}.txt"
    sys.stdout = open(output_file_name, "w")

    # Print out the solution info in the correct format
    apply_solution(puzzle, assignment)


def print_puzzle(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            print(puzzle[row][col], end=" ")
        print()


def backtrack(csp, assignment):
    if len(assignment) == len(csp):  # checks if the assignment is complete
        return True, assignment
    var = csp.select_unassigned_var()
    if var is None:  # if None is returned from select_unassigned_var, then all the vars must be assigned
        return True, assignment
    var_domain = var.get_domain()
    for domain_value in var_domain:  # rotates through each domain value until the right one is
        # consistent with the other assignments
        var.update_value(domain_value)  # sets the variable to its new value
        if assignment.is_Consistent(var, csp.get_constraint_collection()):  # checks if the variable is consistent
            # with the other assigned variables
            assignment.add_assignment(var)  # if so, then the variable is added to the assignment object
            csp.remove_unassigned_var(var)  # the variable is also removed from the list of unassigned_vars
            # so that the select_unassigned_var() method does not pick this var again (unless added back in again)
            result = backtrack(csp, assignment)  # recursively calls backtracking algorithm with new assignment
            if result[0]:  # if the recursive call is successful/true,
                # then the result will be sent back up in the recursive calls
                return result
            assignment.remove_assignment(var)  # if the recursive call fails, then the var is removed
            # from the assignment obj
            var.update_value(0)  # the variable is reset back to 0
            csp.add_unassigned_var(var)  # the variable is added back to the list of unassigned variables
    return False, assignment  # if none of the domain values are consistent with the past variable assignments


def backtracking_search(csp):
    assignment = Assignment([])
    return backtrack(csp, assignment)


def main():
    # Get the input file from the cmd command
    parser = argparse.ArgumentParser(description='Solve Sudoku Puzzle with Backtracking Algorithm '
                                                 'with MRV/degree heuristics and RGB order')
    parser.add_argument('filename', help='The input file containing the initial and goal state')
    cmdline = parser.parse_args()
    file_name = cmdline.filename

    # Parses the file and creates a 2D array that stores each cell as an int value and handles error inputs
    sudoku_puzzle = file_reader(file_name)

    # Outputs the sudoku problem (before it is solved) to the terminal
    print("Input: ")
    print_puzzle(sudoku_puzzle)
    print()

    # Creates the constraint solve problem given the sudoku puzzle array
    csp = CSP(sudoku_puzzle)

    # Removes invalid domain values that conflict with assigned variables from each unassigned variable
    csp.eliminate_domain_values()

    # Sends the csp into the backtracking search algorithm to get solved
    solution = backtracking_search(csp)

    is_success = solution[0]
    if is_success:  # checks if the puzzle was solvable
        assignment = solution[1]
        write_output_file(file_name, sudoku_puzzle, assignment)  # writes the output file with the solved puzzle
    else:  # the puzzle was not solvable given the user inputs
        print("Failure. Puzzle is not solvable.")


if __name__ == "__main__":
    main()

# ra0Eequ6ucie6Jei0koh6phishohm9
