#! /usr/bin/python3

import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
import matplotlib.pylab as plt
import numpy as np
from sys import argv, exit
import argparse

class SnakeGame():

	def __init__( self, size=60, fps=45, figsize=8):
		self.fps = fps
		self.refresh_delay = 1./fps
		self.figsize = figsize
		self.size = size

		self.lastKey = "down"
		self.score = 0
		self.movementDic = {"right": [0,1], "left": [0,-1], "up": [-1,0], "down": [1,0]}
		self.oppositeKey = {"up":"down", "down":"up", "left":"right", "right":"left"}
		self.onPause = False
		self.title_score_format = "SNAKE \t--\t score: {}"
		self.initialize_snake_food()
		self.initialize_window()

	def initialize_snake_food(self):
		snake = [[2,0], [1,0], [0,0]]
		snake_tab = np.zeros( (self.size,self.size), dtype=np.int8)
		head = snake[0]
		snake_tab[ head[0], head[1]] = 2
		for snake_case_x, snake_case_y in snake[1:]:
			snake_tab[snake_case_x][snake_case_y] = 1
		food = [5,5]
		self.snake = snake
		self.snake_tab = snake_tab
		self.food = food
		self.foodPoint = None

	def initialize_window(self):
		fig = plt.figure( figsize=(self.figsize,self.figsize))
		ax = fig.gca()
		fig.tight_layout(pad=0)
		ax.set_xticks(())
		ax.set_yticks(())
		self.food_markersize = 100*60./self.size
		fig.canvas.mpl_connect( "key_press_event", self.onKeyPress)
		fig.tight_layout(pad=0)
		self.snake_canvas = ax.imshow( self.snake_tab, vmin=0, vmax=2, cmap="Blues")
		self.fig = fig
		self.ax = ax
		self.UpdateScore()
		self.UpdateFood()

	def UpdateScore(self):
		self.fig.canvas.set_window_title( self.title_score_format.format(self.score))

	def UpdateFood( self):
		if self.foodPoint:
			self.foodPoint.set_visible( False)
			del self.foodPoint
		self.foodPoint = self.ax.scatter( *self.food[::-1], marker="*", c="#800000", s=self.food_markersize)

	def AddFood( self):
		self.food = None
		while self.food is None or self.food in self.snake:
			self.food = np.random.randint(0, self.size, size=(2,)).tolist()

	def onKeyPress( self, event):
		if event.key == " ":
			self.onPause = not self.onPause
		elif event.key in ["left", "right", "up", "down"] and event.key != self.oppositeKey[ self.lastKey]:
			self.lastKey = event.key

	def GameOverScreen(self):
		#snake has collided into itself, drawing game over screen before exiting
		self.snake_canvas.set_alpha( .25)
		self.foodPoint.set_alpha( .25)
		self.ax.text(0.5, 0.75,'GAME OVER', ha='center', va='center',\
					transform=self.ax.transAxes, fontsize=65, fontweight="bold")
		self.ax.text(0.5, 0.25,'Score: %d' %self.score, ha='center', va='center',\
					transform=self.ax.transAxes, fontsize=45, bbox={"boxstyle":"round","pad":0.5,"alpha":.5})

	def GameLoop(self):
		while True:
			if not self.onPause:
				head = self.snake[0]
				self.snake_tab[ head[0], head[1]] = 1
				movement = self.movementDic[ self.lastKey]
				newHead = [(head[0] + movement[0])%self.size, (head[1] + movement[1])%self.size]
				if newHead in self.snake:
					self.GameOverScreen()
					plt.pause(5)
					plt.close('all')
					exit()
				if self.food == newHead:
					#snake has eaten the food, score and length increase
					self.score += 1
					self.UpdateScore()
					self.AddFood()
					self.UpdateFood()
				else:
					tail = self.snake.pop(-1)
					self.snake_tab[ tail[0], tail[1]] = 0
				self.snake_tab[ newHead[0], newHead[1]] = 2
				self.snake.insert( 0, newHead)
				self.snake_canvas.set_data( self.snake_tab)
				plt.pause(self.refresh_delay)
			else:
				plt.pause( .25)


if __name__ == "__main__":

	#parsing game command line arguments
	parser = argparse.ArgumentParser( description="Snake Game")
	parser.add_argument( "--fps", help="Frame per second", type=int, default=45)
	parser.add_argument( "--size", help="Snake grid size", type=int, default=28)
	parser.add_argument( "--wsize", help="Main window size", type=int, default=8)
	args = parser.parse_args()
	args = vars(args)

	GameInstance = SnakeGame(size=args["size"], fps=args["fps"], figsize=args["wsize"])
	GameInstance.GameLoop()
