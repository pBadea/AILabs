
import random
import sys
import copy




class Board:
	def __init__(self, list=None):
		if list == None:
			self.layout = [[0 for i in range(0, 8)] for j in range(0, 8)]
		else:
			self.layout = list
		# initialize queens at random positions
		for i in range(0, 8):
			while 1:
				rand_row = random.randint(0, 7)
				rand_col = random.randint(0, 7)
				if self.layout[rand_row][rand_col] == 0:
					self.layout[rand_row][rand_col] = "Q"
					break
		

	# defines how to print the board
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
			# detailed_view is for printing out each movement on the board 
			# with_random_restart is for running the hill climb algorithm with random restart and is set by default to False
		def __init__(self, total_runs, detailed_view=True, passed_board=None,with_random_restart = False):
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
				if with_random_restart:
					self.hill_solution_with_random_restart()
				else:
					self.hill_solution()
			# this is the standard hill climbing algorithm 
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

			# curs 3 slide 19
		# Stochastisches Bergsteigen: nachster Zustand wird zuf ̈alligausgew ̈ahlt.
		# First-choice: Nachfolger werden zufallig erzeugt bis einneuer identifiziert wird.
		# Random-restart: Restart von einem zufallig generierten Zustand, falls die Suche nicht fortschreitet.
		# asta scrie in curs despre random restart, asa ca am schimbat hill_climb() 
		# astfel incat daca ajunge in local maxima sa dea restart 	
	

    # this is the ard hill climbing algorithm with random restart
    def hill_solution_with_random_restart(self):
			while 1:
				currViolations = self.cost
				self.get_lower_cost_board()
				# if fail start again with other board
				if currViolations == self.cost:
					break;
				self.total_steps += 1
				if self.detailed_view == True:
					print("Board Violations", self.compute_cost(self.current_board))
					print(self.current_board)
			if self.cost != 0:
				self.current_board = Board()
				self.hill_solution_with_random_restart()
				# if self.detailed_view == True:
					# print("NO SOLUTION FOUND")
			else:
				if self.detailed_view == True:
					print("SOLUTION FOUND")
				self.total_successes += 1
		return self.cost

		# returns amout of conflicts between Queens
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
		# and returns the move with the minimal number of conflicts
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

		# functioneaza doar ptr apelul hill_solution deoarece nu 
		# inteleg daca dupa ce face restart se pune ca win sau fail?
		def print_stats(self):
			print("Total Runs: ", self.total_runs)
			print("Total Success: ", self.total_successes)
			print("Success Percentage: ", float(
				self.total_successes)/float(self.total_runs))
			print("Average number of steps: ", float(
				self.total_steps)/float(self.total_runs))


# myBoard = Board()
# print(myBoard)
# i = 1
# while Q8P.cost != 0:
# 	Q8P = Eight_Queens_Problem(1, False)
# 	print("TEST" + str(i))
# 	i += 1
# print(Q8P.current_board)


# solution without random restart 
Q8P = Eight_Queens_Problem(1, True)
Q8P.print_stats()


# solution with random restart 
Q8P = Eight_Queens_Problem(1, True, None, True)
