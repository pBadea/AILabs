import random
import sys
import copy
from optparse import OptionParser


class Board:
		def __init__(self, list=None):
				if list == None:
						self.layout = [[0 for i in range(0, 8)] for j in range(0, 8)]
				# initialize queens at random positions
				for i in range(0, 8):
						while 1:
								rand_row = random.randint(0, 7)
								rand_col = random.randint(0, 7)
								if self.layout[rand_row][rand_col] == 0:
										self.layout[rand_row][rand_col] = "Q"
										break
		# define how to print the board

		def __repr__(self):
				board_string = ""
				print(" _______________________________")
				for i in range(0, 8):
						for j in range(0, 8):
								# the purpose of these if branches is to generate a graphical representation of the board
								if(j == 0):
										board_string += "|_"
								if str(self.layout[i][j]) == "0":
										tile_to_be_added = "_"
								else:
										tile_to_be_added = "Q"
								if(j < 7):
										board_string += tile_to_be_added + "_|_"
								else:
										board_string += tile_to_be_added + "_|"
						board_string += "\n"
				return (board_string)


class Eight_Queens_Problem:

		def __init__(self, total_runs, detailed_view=True, passed_board=None):
				self.total_runs = total_runs
				self.total_successes = 0
				self.total_steps = 0
				self.detailed_view = detailed_view
				for i in range(0, total_runs):
						if self.detailed_view == True:
								print("####################")
								print("BOARD", i)
								print("####################")
						self.current_board = Board(passed_board)
						self.cost = self.compute_cost(self.current_board)
						self.hill_solution()

		def hill_solution(self):
				while 1:
						currViolations = self.cost
						self.get_lower_cost_board()
						if currViolations == self.cost:
								break
						self.total_steps += 1
						if self.detailed_view == True:
								print("Board Violations", self.compute_cost(self.current_board))
								print(self.current_board)
				if self.cost != 0:
						if self.detailed_view == True:
								print("NO SOLUTION FOUND")
				else:
						if self.detailed_view == True:
								print("SOLUTION FOUND")
						self.total_successes += 1
				return self.cost

		def compute_cost(self, board):
				horiz_vertic_cost = 0
				diagonal_cost = 0
				for i in range(0, 8):
						for j in range(0, 8):
								if(board.layout[i][j] == "Q"):
										# subtract 2 so that the Q doesn't count itself
										horiz_vertic_cost -= 2
										for k in range(0, 8):
												# check for vertical conflicts
												if(board.layout[i][k] == "Q"):
														horiz_vertic_cost += 1
												# check for horizontal conflicts
												if(board.layout[k][j] == "Q"):
														horiz_vertic_cost += 1
										# check for diagonal conflicts
										k, l = i+1, j+1
										while k < 8 and l < 8:
												if board.layout[k][l] == "Q":
														diagonal_cost += 1
												k += 1
												l += 1
										k, l = i+1, j-1
										while k < 8 and l >= 0:
												if board.layout[k][l] == "Q":
														diagonal_cost += 1
												k += 1
												l -= 1
										k, l = i-1, j+1
										while k >= 0 and l < 8:
												if board.layout[k][l] == "Q":
														diagonal_cost += 1
												k -= 1
												l += 1
										k, l = i-1, j-1
										while k >= 0 and l >= 0:
												if board.layout[k][l] == "Q":
														diagonal_cost += 1
												k -= 1
												l -= 1
				return((diagonal_cost + horiz_vertic_cost)/2)

		# this function moves every queen to every spot, with only one move
		# and returns themove number of conflicts

		def get_lower_cost_board(self):
				current_cost = self.compute_cost(self.current_board)
				lowest_available = self.current_board
				# move one queen at a time, the optimal single move by brute force
				for q_row in range(0, 8):
						for q_col in range(0, 8):
								if self.current_board.layout[q_row][q_col] == "Q":
										# get the lowest cost by moving this queen
										for m_row in range(0, 8):
												for m_col in range(0, 8):
														if self.current_board.layout[m_row][m_col] != "Q":
																# try placing the queen here and see if it's any better
																test_board = copy.deepcopy(self.current_board)
																test_board.layout[q_row][q_col] = 0
																test_board.layout[m_row][m_col] = "Q"
																test_cost = self.compute_cost(test_board)
																if test_cost < current_cost:
																		current_cost = test_cost
																		lowest_available = test_board
				self.current_board = lowest_available
				self.cost = current_cost

		def print_stats(self):
				print("Total Runs: ", self.total_runs)
				print("Total Success: ", self.total_successes)
				print("Success Percentage: ", float(
						self.total_successes)/float(self.total_runs))
				print("Average number of steps: ", float(
						self.total_steps)/float(self.total_runs))


# myBoard = Board()
# print(myBoard)
Q8P = Eight_Queens_Problem(1, False)
i = 1
while Q8P.cost != 0:
		Q8P = Eight_Queens_Problem(1, False)
		print("TEST" + str(i))
		i += 1
print(Q8P.current_board)
