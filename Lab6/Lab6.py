# Aufgabe 1 Teil A 
# Gruppe: Badea Patrick,Alexandru Tenie, Gati Mark
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.spatial.distance import cdist


class Firefly:
	def __init__(self, x_pos, y_pos, internal_clock=0):
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.internal_clock = internal_clock
		self.neighboured_fireflies = []

	def is_in_proximity_to_other_firefly(self, other_firefly, r):
		if(cdist([[self.x_pos, self.y_pos]], [[other_firefly.x_pos, other_firefly.y_pos]]) <= r):
			return True
		else:
			return False


class FirefliesProblem:
	def closest_node(self, node, nodes):
		nd = [node]
		res = nodes[cdist([node], nodes).argmin()]
		return res

	def generate_population(self, size):
		# a = np.random.randint(1000, size=(10, 2))
		self.population_size = size
		self.radius = 0.1
		self.fireflies = []
		self.points = []
		self.x_array = []
		self.y_array = []
		self.points = np.random.rand(self.population_size, 2)
		self.light_cycles = np.random.randint(50, size=self.population_size)
		i = 0
		for p in self.points:
			self.x_array.append(p[0])
			self.y_array.append(p[1])
			self.fireflies.append(Firefly(p[0], p[1], self.light_cycles[i]))
			i += 1

	def find_all_neighbours(self):
		i = 0
		for firefly in self.fireflies:
				fireflies_without_current_firefly = np.copy(self.fireflies)
				fireflies_without_current_firefly = np.delete(fireflies_without_current_firefly, i, axis=0)
				for other_firefly in fireflies_without_current_firefly:
				# if firefly is neighboured then increment contor of it's intrenal clock
					if (firefly.is_in_proximity_to_other_firefly(other_firefly, self.radius)):
						firefly.neighboured_fireflies.append(other_firefly)
									
	# this method sychronizes each firefly over a specific period of time
	# time stands for the nr. of timeunits which determines the number of iterations
	# a full light cycle is considered to be about 25 time units
	def synchronize_fireflies_over_a_specific_time_period(self, time, number_of_frames=25, detailed_view=True):
		# plt.scatter(self.x_array, self.y_array)
		self.find_all_neighbours()
		for t in range(time):
			# if(t % number_of_frames == 0  and detailed_view):
			# print("time:" + str(t))
			i = 0
			plt.clf()
			# vector de contorizare ptr. ciclurile de timp al vecinilor
			firefly_cycles_to_be_decremented = np.zeros(self.population_size)
			# loop trough every firefly an find it's neghbours to synch them up
			for firefly in self.fireflies:
				# print(firefly.internal_clock)
				# vector de contorizare ptr. ciclurile de timp al vecinilor; 50 = ciclu intreg
				time_counter = np.zeros(50)
				for other_firefly in firefly.neighboured_fireflies:
					time_counter[other_firefly.internal_clock] += 1
				#  if detailed_view is set to true plot every connection
				#  between current firefly and neighbours
				# if(detailed_view):
				for other_firefly in firefly.neighboured_fireflies:
					x_values = [firefly.x_pos, other_firefly.x_pos]
					y_values = [firefly.y_pos, other_firefly.y_pos]
					plt.plot(x_values, y_values, 'bo-')
					# if most of the nearby fireflies have a higher value than current firefly
					# then current firefly ends his blink cycle a second earlier
					if (firefly.internal_clock > np.argmax(time_counter)):
						firefly_cycles_to_be_decremented[i] = 1
				if(firefly.internal_clock <= 24 ):
					plt.scatter(self.x_array, self.y_array)
					plt.plot(firefly.x_pos, firefly.y_pos, 'ro')
					# self.plot_a_line_between_nerby_firefly([firefly.x_pos,firefly.y_pos],[other_firefly.x_pos,other_firefly.y_pos])
				if(firefly.internal_clock == 49):
					firefly.internal_clock = 0
				# pass a second in each firefly's internal clock
				else:
					firefly.internal_clock += 1
				i += 1
			# if(detailed_view):
				# plot every number_of_frames timeunits the image of
			if(t % number_of_frames == 0 and detailed_view):
				print("time:" + str(t))
				plt.show()
			# decrement 1 from the time cycle for the fireflies that need to synch up
			if(t % 25 == 0):
				print("##### ANOTHER 25 SECONDS HAVE PASSED #####")
				j = 0
				for firefly_flag in firefly_cycles_to_be_decremented:
					if(firefly_flag == 1):
						self.fireflies[j].internal_clock -= 1
					j += 1

	def plot_a_line_between_nerby_firefly(self, point, other_point):
		if(cdist([[point[0], point[1]]], [[other_point[0], other_point[1]]]) <= self.radius):
			x_values = [point[0], other_point[0]]
			y_values = [point[1], other_point[1]]
			plt.plot(x_values, y_values, 'bo-')

	def plot_fireflies_for_a_given_radius(self, r):
		self.radius = r
		plt.scatter(self.x_array, self.y_array)
		i = 0
		for point in self.points:
			points_without_current_point = np.copy(self.points)
			points_without_current_point = np.delete(
				points_without_current_point, i, axis=0)
			for second_point in points_without_current_point:
				self.plot_a_line_between_nerby_firefly(point, second_point)

			# closest_point = closest_node([point[0],point[1]], points_without_current_point)
			# if(cdist(point, points_without_current	_point) <= 0.1):
			# 	x_values = [point[0],closest_point[0]]
			# 	y_values = [point[1],closest_point[1]]
			# 	plt.plot(x_values, y_values, 'ro-')
			# i += 1
		plt.show()


firefliesProblem = FirefliesProblem()
firefliesProblem.generate_population(10)
firefliesProblem.plot_fireflies_for_a_given_radius(0.5)
firefliesProblem.synchronize_fireflies_over_a_specific_time_period(1000, 3,True)

