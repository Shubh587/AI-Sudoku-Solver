#!/usr/bin/python3
# Developer: Shubh Savani

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

    def prune_domain(self, value):
        self.domain.remove(value)

    def set_domain(self, new_domain):
        self.domain = new_domain

    def add_domain_val(self, value):
        self.domain.append(value)  # appends the value to the end of the list
        self.domain.sort()  # sorts the list in increasing order from 1 - 9

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

    def is_Assigned(self, variable):
        # Traverse through each variable in assignments and return True if the given variable is already assigned
        for ind in range(len(self.assignments)):
            assigned_var = self.assignments[ind]
            if variable == assigned_var:
                return True
        return False

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
                        unassigned_var.prune_domain(assigned_var_value)

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

    def forward_checking(self, unassigned_var, assignment):
        # print("X: ", unassigned_var)
        # print()
        unassigned_var_val = unassigned_var.get_value()
        constraints = self.constraint_collection.find_var_constraints(unassigned_var)
        # print("X's Constraints: ")
        # for ind in range(len(constraints)):
        #     print(constraints[ind])
        # print()
        inferences = {}  # holds all the variables and their new domains due to pruning
        for ind in range(len(constraints)):
            constraint = constraints[ind]
            constraint_vars = constraint.get_variables()
            for var_ind in range(len(constraint_vars)):
                variable = constraint_vars[var_ind]
                var_domain = variable.get_domain()
                var_location = variable.get_location()
                pruned_vals = []
                if not assignment.is_Assigned(variable):
                    if unassigned_var != variable:
                        if unassigned_var_val in var_domain:
                            pruned_vals.append(unassigned_var_val)
                            # print("Y: ", variable)
                            # print("Y's Domain: ", var_domain)
                            # print()
                            if len(var_domain) == 1:  # checks if we would prune the last val and result to a failure
                                #  print("Here")
                                return False, inferences  # the value assignment to this unassigned variable failed
                            inferences[var_location] = pruned_vals
        return True, inferences

    def find_unassigned_var(self, var_location):
        for ind in range(len(self.unassigned_vars)):
            unassigned_var = self.unassigned_vars[ind]
            unassigned_var_loc = unassigned_var.get_location()
            unassigned_var_row = unassigned_var_loc[0]
            unassigned_var_col = unassigned_var_loc[1]
            if unassigned_var_row == var_location[0] and unassigned_var_col == var_location[1]:
                return unassigned_var
        return None

    def apply_inferences(self, inferences):
        connected_vars_locations = inferences.keys()
        for var_loc in connected_vars_locations:
            connected_var = self.find_unassigned_var(var_loc)
            if connected_var is not None:
                pruned_vals = inferences[var_loc]
                for val in pruned_vals:
                    connected_var.prune_domain(val)

    def reverse_inferences(self, inferences):
        connected_vars_locations = inferences.keys()
        for var_loc in connected_vars_locations:
            connected_var = self.find_unassigned_var(var_loc)
            if connected_var is not None:
                pruned_vals = inferences[var_loc]
                for val in pruned_vals:
                    connected_var.add_domain_val(val)

    def add_unassigned_var(self, unassigned_var):
        self.unassigned_vars.append(unassigned_var)


def file_reader(file_name):
    puzzle = []
    file = open(file_name)
    valid_inputs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for ind in range(9):
        line = file.readline()
        row = line.split()
        puzzle.append(row)
    #  convert each value in puzzle from a string to an integer
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            val_str = puzzle[row][col]
            if val_str not in valid_inputs:
                raise ValueError("Input must be an integer from 0 to 9")
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


def convert_1D_array(puzzle, assignment, is_solvable):
    solution = []
    if is_solvable:
        # Convert the assignment into a dictionary that holds the location of the variable and the given assigned value
        var_assignments = {}
        for ind in range(len(assignment)):
            variable = assignment.get_assignments()[ind]
            var_loc = variable.get_location()
            var_val = variable.get_value()
            var_assignments[var_loc] = var_val
        for row in range(len(puzzle)):
            for col in range(len(puzzle[row])):
                val = puzzle[row][col]
                if val == 0:  # we know an unassigned var is supposed to go here
                    unassigned_var_val = var_assignments[row, col]
                    solution.append(unassigned_var_val)
                else:  # this is an assigned var
                    solution.append(val)
    else:  # the backtracking algorithm failed to solve the puzzle
        solution = [-1] * 81
    return solution


def print_puzzle(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            print(puzzle[row][col], end=" ")
        print()


def parse_rows(puzzle):
    rows = {}
    for row in range(len(puzzle)):
        rows[row] = [puzzle[row][col] for col in range(len(puzzle[row])) if puzzle[row][col] != 0]
    return rows


def parse_cols(puzzle):
    cols = {}
    for col in range(len(puzzle)):
        cols[col] = [puzzle[row][col] for row in range(len(puzzle[col])) if puzzle[row][col] != 0]
    return cols


def parse_blocks(puzzle):
    blocks = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            value = puzzle[row][col]
            if value != 0:
                block_num = None
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
                blocks[block_num].append(value)
    return blocks


def given_enough_clues(puzzle):
    num_clues = 0
    for row in range(len(puzzle)):
        for col in range(len(puzzle[row])):
            value = puzzle[row][col]
            if value != 0:
                num_clues += 1
    if 0 <= num_clues <= 16:
        return False
    return True


def is_viable(puzzle):
    if not given_enough_clues(puzzle):  # check if there are enough clues given for the algo to solve
        return False
    rows = parse_rows(puzzle)
    cols = parse_cols(puzzle)
    blocks = parse_blocks(puzzle)

    # check every unit to make sure there are no invalid inputs
    for row_ind in rows.keys():
        row = rows[row_ind]
        row.sort()
        for ind in range(len(row) - 1):
            curr_val = row[ind]
            next_val = row[ind + 1]
            if curr_val == next_val:
                return False
    for col_ind in cols.keys():
        col = cols[col_ind]
        col.sort()
        for ind in range(len(col) - 1):
            curr_val = col[ind]
            next_val = col[ind + 1]
            if curr_val == next_val:
                return False
    for block_ind in blocks.keys():
        block = blocks[block_ind]
        block.sort()
        for ind in range(len(block) - 1):
            curr_val = block[ind]
            next_val = block[ind + 1]
            if curr_val == next_val:
                return False
    return True


# def backtrack(csp, assignment):  # basic version (no forward checking)
#     if len(assignment) == len(csp):  # checks if the assignment is complete
#         return True, assignment
#     var = csp.select_unassigned_var()
#     if var is None:  # if None is returned from select_unassigned_var, then all the vars must be assigned
#         return True, assignment
#     var_domain = var.get_domain()
#     for domain_value in var_domain:  # rotates through each domain value until the right one is
#         # consistent with the other assignments
#         var.update_value(domain_value)  # sets the variable to its new value
#         if assignment.is_Consistent(var, csp.get_constraint_collection()):  # checks if the variable is consistent
#             # with the other assigned variables
#             assignment.add_assignment(var)  # if so, then the variable is added to the assignment object
#             csp.remove_unassigned_var(var)  # the variable is also removed from the list of unassigned_vars
#             # so that the select_unassigned_var() method does not pick this var again (unless added back in again)
#             result = backtrack(csp, assignment)  # recursively calls backtracking algorithm with new assignment
#             if result[0]:  # if the recursive call is successful/true,
#                 # then the result will be sent back up in the recursive calls
#                 return result
#             assignment.remove_assignment(var)  # if the recursive call fails, then the var is removed
#             # from the assignment obj
#             var.update_value(0)  # the variable is reset back to 0
#             csp.add_unassigned_var(var)  # the variable is added back to the list of unassigned variables
#     return False, assignment  # if none of the domain values are consistent with the past variable assignments
#

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
            inferences = csp.forward_checking(var, assignment)
            # print(inferences)
            # print()
            if inferences[0]:  # checks if the forward checking inference failed or not
                csp.apply_inferences(inferences[1])  # apply the forward checking inferences to CSP
                result = backtrack(csp, assignment)  # recursively calls backtracking algorithm with new assignment
                if result[0]:  # if the recursive call is successful/true,
                    # then the result will be sent back up in the recursive calls
                    return result
                csp.reverse_inferences(inferences[1])  # the inferences failed and need to be removed from CSP
            assignment.remove_assignment(var)  # if the recursive call fails, then the var is removed
            # from the assignment obj
            var.update_value(0)  # the variable is reset back to 0
            csp.add_unassigned_var(var)  # the variable is added back to the list of unassigned variables
    return False, assignment  # if none of the domain values are consistent with the past variable assignments


def backtracking_search(csp):
    assignment = Assignment([])
    return backtrack(csp, assignment)


# def main():
#     # Get the input file from the cmd command
#     parser = argparse.ArgumentParser(description='Solve Sudoku Puzzle with Backtracking Algorithm '
#                                                  'with MRV/degree heuristics and RGB order')
#     parser.add_argument('filename', help='The input file containing the initial and goal state')
#     cmdline = parser.parse_args()
#     file_name = cmdline.filename
#
#     # Parses the file and creates a 2D array that stores each cell as an int value and handles error inputs
#     sudoku_puzzle = file_reader(file_name)
#
#     # Outputs the sudoku problem (before it is solved) to the terminal
#     print("Input: ")
#     print_puzzle(sudoku_puzzle)
#     print()
#
#     # Checks if the initial puzzle given is viable
#     if is_viable(sudoku_puzzle):
#         # Creates the constraint solve problem given the sudoku puzzle array
#         csp = CSP(sudoku_puzzle)
#         # Removes invalid domain values that conflict with assigned variables from each unassigned variable
#         csp.eliminate_domain_values()
#
#         # Send the csp into the backtracking search algorithm to get solved
#         solution = backtracking_search(csp)
#         is_success = solution[0]
#
#         # outputs entire puzzle as a 1D array for the HTML program to process and output to the user
#         assignment = solution[1]
#         output = convert_1D_array(sudoku_puzzle, assignment, is_success)
#     else:
#         output = [-1] * 81
#     print(output)
#
#     # if is_viable(sudoku_puzzle):
#     #     csp = CSP(sudoku_puzzle)
#     #     csp.eliminate_domain_values()
#     #     solution = backtracking_search(csp)
#     #     is_success = solution[0]
#     #
#     #     if is_success:  # checks if the puzzle was solvable
#     #         assignment = solution[1]
#     #         write_output_file(file_name, sudoku_puzzle, assignment)  # writes the output file with the solved puzzle
#     #     else:  # the puzzle was not solvable given the user inputs
#     #         print("Failure. Puzzle is not solvable.")
#     # else:
#     #     print("Failure. Puzzle is not solvable.")
#
#
# if __name__ == "__main__":
#     main()

# ra0Eequ6ucie6Jei0koh6phishohm9
