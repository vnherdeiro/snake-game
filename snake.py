#! /usr/bin/python3

import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
import matplotlib.pylab as plt
import numpy as np
from sys import argv, exit

try:
	size = min( int(argv[1]), 100)
except:
	size = 60

refresh_delay = 0.1

lastKey = "down"
score = 0

snake = [[2,0], [1,0], [0,0]]
snake_tab = np.zeros( (size,size), dtype=np.int8)
head = snake[0]
snake_tab[ head[0], head[1]] = 2
for snake_case_x, snake_case_y in snake[1:]:
	snake_tab[snake_case_x][snake_case_y] = 1
food = [5,5]


fig = plt.figure( figsize=(8,8))
ax = fig.gca()
fig.tight_layout(pad=0)
ax.set_xticks(())
ax.set_yticks(())
onPause = False
food_markersize = 100*60./size
foodPoint = ax.scatter( *food[::-1], marker="*", c="#800000", s=food_markersize)


movementDic = {"right": [0,1], "left": [0,-1], "up": [-1,0], "down": [1,0]}
oppositeKey = {"up":"down", "down":"up", "left":"right", "right":"left"}
def onKeyPress( event):
	global onPause, lastKey
	if event.key == " ":
		onPause = not onPause
	elif event.key in ["left", "right", "up", "down"] and event.key != oppositeKey[ lastKey]:
		lastKey = event.key
		
fig.canvas.mpl_connect( "key_press_event", onKeyPress)
fig.tight_layout(pad=0)
title_score_format = "SNAKE \t--\t score: {}"
fig.canvas.set_window_title(title_score_format.format(score))


snake_canvas = ax.imshow( snake_tab, vmin=0, vmax=2, cmap="Blues")

while True:
	if not onPause:
		head = snake[0]
		snake_tab[ head[0], head[1]] = 1
		movement = movementDic[ lastKey]
		newHead = [(head[0] + movement[0])%size, (head[1] + movement[1])%size]
		if newHead in snake:
			#snake has collided into itself, drawing game over screen before exiting
			#snake_canvas.set_visible( False)
			#foodPoint.set_visible( False)
			snake_canvas.set_alpha( .25)
			foodPoint.set_alpha( .25)
			ax.text(0.5, 0.75,'GAME OVER', ha='center', va='center', transform=ax.transAxes, fontsize=65, fontweight="bold")
			ax.text(0.5, 0.25,'Score: %d' %score, ha='center', va='center', transform=ax.transAxes, fontsize=45, bbox={"boxstyle":"round","pad":0.5,"alpha":.5})
			plt.pause(5)
			exit()
		if food == newHead:
			#snake has eaten the food, score and length increase
			score += 1
			fig.canvas.set_window_title(title_score_format.format(score))
			food = None
			while food is None or food in snake:
				food = np.random.randint(0, size, size=(2,)).tolist() 
			foodPoint.set_visible( False)
			del foodPoint
			foodPoint = ax.scatter( *food[::-1], marker="*", c="#800000", s=food_markersize)
		else:
			tail = snake.pop(-1)
			snake_tab[ tail[0], tail[1]] = 0
		snake_tab[ newHead[0], newHead[1]] = 2
		snake.insert( 0, newHead)
		snake_canvas.set_data( snake_tab)
		plt.pause(refresh_delay)
	else:
		plt.pause( .25)
