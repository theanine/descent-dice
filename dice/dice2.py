#!/usr/bin/env python3
import sys, getopt
import time
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as plticker
import numpy as np
import curses
from curses.textpad import Textbox, rectangle
from collections import defaultdict
from IPython.core.pylabtools import figsize

# matplotlib.use("Qt4agg")

settings_showPercent = False
settings_showMiss = False

matplotlib.rcParams['font.size'] = 18
matplotlib.rcParams['figure.dpi'] = 300

dies = {}
diceValues = [0,0,0,0,0,0,0]

# ATK
dies["blue"] = {}
dies["blue"]["ranged"] = [0,2,3,4,5,6]
dies["blue"]["damage"] = [0,2,2,2,1,1]
dies["blue"]["surge"]  = [0,1,0,0,0,1]
dies["blue"]["miss"]   = [1,0,0,0,0,0]

dies["red"] = {}
dies["red"]["ranged"] = [0,0,0,0,0,0]
dies["red"]["damage"] = [1,2,2,2,3,3]
dies["red"]["surge"]  = [0,0,0,0,0,1]
dies["red"]["miss"]   = [0,0,0,0,0,0]

dies["yellow"] = {}
dies["yellow"]["ranged"] = [1,1,2,0,0,0]
dies["yellow"]["damage"] = [0,1,1,1,2,2]
dies["yellow"]["surge"]  = [1,0,0,1,0,1]
dies["yellow"]["miss"]   = [0,0,0,0,0,0]

dies["green"] = {}
dies["green"]["ranged"] = [0,0,1,1,0,1]
dies["green"]["damage"] = [1,0,0,1,1,1]
dies["green"]["surge"]  = [0,1,1,0,1,1]
dies["green"]["miss"]   = [0,0,0,0,0,0]

# DEF
dies["brown"] = {}
dies["brown"]["ranged"] = [0,0,0,0,0,0]
dies["brown"]["damage"] = [-0,-0,-0,-1,-1,-2]
dies["brown"]["surge"]  = [0,0,0,0,0,0]
dies["brown"]["miss"]   = [0,0,0,0,0,0]
dies["white"] = {}
dies["white"]["ranged"] = [0,0,0,0,0,0]
dies["white"]["damage"] = [-0,-1,-1,-1,-2,-3]
dies["white"]["surge"]  = [0,0,0,0,0,0]
dies["white"]["miss"]   = [0,0,0,0,0,0]
dies["black"] = {}
dies["black"]["ranged"] = [0,0,0,0,0,0]
dies["black"]["damage"] = [-0,-2,-2,-2,-3,-4]
dies["black"]["surge"]  = [0,0,0,0,0,0]
dies["black"]["miss"]   = [0,0,0,0,0,0]

def drawPlot():
    backend = plt.rcParams['backend']
    if backend in matplotlib.rcsetup.interactive_bk:
        figManager = matplotlib._pylab_helpers.Gcf.get_active()
        if figManager is not None:
            canvas = figManager.canvas
            if canvas.figure.stale:
                canvas.draw()
            canvas.start_event_loop(0.001)

def doProdSum(list_of_dicts):
    # We reorganize the data by key
    lists_by_key = defaultdict(list)
    for d in list_of_dicts:
        for k, v in d.items():
            lists_by_key[k].append(v)

    # Then we generate the output
    out = {}
    for key, lists in lists_by_key.items():
        out[key] = [sum(prod) for prod in itertools.product(*lists)]

    return out

def rollDice(**kwargs):
	# add dice to pool
	dice = []
	for key, value in kwargs.items():
		dice.extend([dies[key] for i in range(0, value)])

	# "roll" dice
	rolled = doProdSum(dice)

	# adjust dice for misses
	hit = [0 if x > 0 else 1 for x in rolled['miss']] if 'miss' in rolled else [0]
	for i in rolled:
		if i == 'miss':
			continue
		rolled[i] = [a*b for a,b in zip(hit, rolled[i])]

	avgMiss = 1 - (sum(hit) / len(hit))
	return rolled, avgMiss

pltBars = []
def descentHelper():
	result, avgMiss = rollDice(blue   = diceValues[0],
							   red    = diceValues[1],
							   yellow = diceValues[2],
							   green  = diceValues[3],
							   brown  = diceValues[4],
							   white  = diceValues[5],
							   black  = diceValues[6])
	if not settings_showMiss:
		result.pop('miss', None)

	avgRange = 0 if "ranged" not in result else sum(result["ranged"])/len(result["ranged"])
	avgDamage = 0 if "damage" not in result else sum(result["damage"])/len(result["damage"])
	surge = [1 if x > 0 else 0 for x in result["surge"]] if 'surge' in result else [0]
	avgSurge = sum(surge) / len(surge)
	
	# Configure histogram settings
	colors = ['#009E73', '#D55E00', '#F0E442', '#56B4E9'] # '#E69F00' (orange)
	labels = ['ranged ({0:.1f})'.format(avgRange),
			  'damage ({0:.1f})'.format(avgDamage),
			  'surge ({0:.1f}%)'.format(avgSurge * 100),
			  'miss ({0:.1f}%)'.format(avgMiss * 100)]

	results = list(result.values())
	minData = min(map(lambda x: min(x), results)) if len(results) > 0 else 0
	maxData = max(map(lambda x: max(x), results)) if len(results) > 0 else 0
	
	# Make the histogram using matplotlib
	global pltBars
	[b.remove() for b in pltBars]
	_, _, pltBars = plt.hist(results, color=colors[:max(len(result),1)], edgecolor='black', label=labels[:max(len(result),1)],
		bins=np.arange(minData, maxData + 0.9999, 0.9999), density=True)

	# Rescale the display to fit the data
	frame1 = plt.gca()
	frame1.relim()
	frame1.autoscale_view()

	# Place a legend to the right of this smaller subplot.
	handles, _ = frame1.axes.get_legend_handles_labels()
	if not settings_showMiss and len(results)>0:
		handles.append(mpatches.Patch(color='none', label=labels[3]))
	plt.legend(handles=handles)
	drawPlot()

def descent():
	colors = ['#009E73', '#D55E00', '#F0E442', '#56B4E9'] # '#E69F00' (orange)

	# Make the histogram using matplotlib
	figsize(5, 5)
	plt.hist([], color=colors[0], edgecolor='black',
		bins=np.arange(0, 0 + 0.9999, 0.9999), density=True)
	
	# Add labels
	plt.title('Descent: Dice Probability Distribution Graph')
	plt.xlabel('Amount')
	plt.ylabel('Percentile')

	# Add ticks on x-axis/y-axis
	frame1 = plt.gca()
	frame1.axes.xaxis.set_major_locator(plticker.MultipleLocator(base=1.0))
	frame1.axes.yaxis.set_major_locator(plticker.MultipleLocator(base=0.05))
	
	if settings_showPercent:
		frame1.axes.set_yticklabels(['{:,.0%}'.format(x) for x in frame1.axes.get_yticks()])
	
	# Place a legend to the right of this smaller subplot.
	handles, _ = frame1.axes.get_legend_handles_labels()
	if not settings_showMiss:
		handles.append(mpatches.Patch(color='none'))
	plt.legend(handles=handles)
	plt.ion()
	plt.show(block=False)

def main(stdscr):
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	
	stdscr.addstr(0, 0, "Enter Dice: (ESC to quit)")
	stdscr.addstr(2, 1, "Blue:")
	stdscr.addstr(3, 1, "Red:")
	stdscr.addstr(4, 1, "Yellow:")
	stdscr.addstr(5, 1, "Green:")
	stdscr.addstr(6, 1, "Brown:")
	stdscr.addstr(7, 1, "White:")
	stdscr.addstr(8, 1, "Black:")
	
	curses.curs_set(0)
	editwin = curses.newwin(8,2, 2,11)
	rectangle(stdscr, 1,9, 1+7+1, 1+11+1)
	
	stdscr.nodelay(True)
	selected = 0
	counter = 100
	while True:
		c = stdscr.getch()
		if c >= ord('0') and c <= ord('9'):
			if diceValues[selected] != int(chr(c)):
				diceValues[selected] = int(chr(c))
				counter = 0
		elif c == 258: # down
			selected += 1
			if selected > 6:
				selected = 6
		elif c == 259: # up
			selected -= 1
			if selected < 0:
				selected = 0
		elif c == 27:
			plt.close()
			curses.endwin()
			return

		# Draw stuff
		for i in range(0,7):
			stdscr.addstr(i+2, 11, str(diceValues[i]), curses.color_pair(1 if i == selected else 0))
	
		# Wait 1/100 of a second
		time.sleep(0.01)
		counter -= 1
		if counter <= 0:
			descentHelper()
			counter = 100

if __name__ == "__main__":
	descent()
	curses.wrapper(main)
