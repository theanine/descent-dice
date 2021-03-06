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
from joblib import Memory
from curses.textpad import Textbox, rectangle
from collections import defaultdict
from IPython.core.pylabtools import figsize

# matplotlib.use("Qt4agg")

settings_showPercent = False
settings_showMiss = False
settings_surgePct = False
settings_debug = False
cum_enabled = 0
cum_mode = 1
cum_mode_str = "FWD"

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.dpi'] = 300
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8
matplotlib.rcParams['axes.labelsize'] = 16
matplotlib.rcParams['axes.titlesize'] = 16

dies = {}
GUIdice = [0,0,0,0,0,0,0]

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

tStart = [None]*10
tEnd = [None]*10
def timeStart(index):
	if not settings_debug and index > 0:
		return
	global tStart
	tStart[index] = time.time()

def timeEnd(index):
	if not settings_debug and index > 0:
		return
	global tEnd	
	tEnd[index] = time.time()

def timeDiff(index):
	if not settings_debug and index > 0:
		return
	if not tEnd[index] or not tStart[index]:
		return
	return tEnd[index] - tStart[index]

def timeDiffFormatted(index):
	if not settings_debug and index > 0:
		return
	td = timeDiff(index)
	if td is not None:
		return "{:.2f}s".format(td)
	else:
		return "**WAIT**"

memory = None
rollDiceCached = None
def cacheSetup():
	global rollDiceCached
	global memory
	location = './.cache'
	memory = Memory(location, verbose=0)
	rng = np.random.RandomState(42)
	rollDiceCached = memory.cache(rollDice)

def cacheClear():
	memory.clear(warn=False)

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
	hit = [0 if x > 0 else 1 for x in rolled['miss']] if 'miss' in rolled else []
	for i in rolled:
		if i == 'miss':
			continue
		rolled[i] = [a*b for a,b in zip(hit, rolled[i])]

	avgMiss = 1 - (sum(hit) / len(hit)) if len(hit) > 0 else 0
	return rolled, avgMiss

def diceFromGUI():
	blu = GUIdice[0];
	red = GUIdice[1];
	yel = GUIdice[2];
	gre = GUIdice[3];
	bro = GUIdice[4];
	whi = GUIdice[5];
	bla = GUIdice[6];
	return {'blue':blu, 'red':red, 'yellow':yel, 'green':gre, 'brown':bro, 'white':whi, 'black':bla}

figure = None
def descentSetup(cli):
	cacheSetup()
	
	colors = ['#009E73', '#D55E00', '#F0E442', '#56B4E9'] # '#E69F00' (orange)
	
	# Make the histogram using matplotlib
	figsize(9 if cli else 8.25, 6)
	plt.hist([], color=colors[0], edgecolor='black', bins=np.arange(0, 0 + 0.9999, 0.9999), density=True)
	plt.style.use('dark_background')
	
	# Add labels
	global figure
	figure = plt.gcf()
	figure.canvas.set_window_title('Descent: Dice Probability Distribution Graph')
	plt.title('Descent: Dice Probability Distribution Graph')
	plt.xlabel('Amount')
	plt.ylabel('Probability')
	plt.subplots_adjust(left=0.12, bottom=0.13, right=0.98, top=0.92)

	# Add ticks on x-axis/y-axis
	ax = plt.gca()
	ax.axes.xaxis.set_major_locator(plticker.MultipleLocator(base=1.0))
	ax.axes.yaxis.set_major_locator(plticker.MultipleLocator(base=0.05))
	
	if settings_showPercent:
		ax.axes.set_yticklabels(['{:,.0%}'.format(x) for x in ax.axes.get_yticks()])
	
	if not cli:
		plt.ion()
		plt.show(block=False)
		curses.wrapper(descentGUI)

pltBars = []
result = {}
avgMiss = 0
counter = 0
colors = ['#009E73', '#D55E00', '#F0E442', '#56B4E9'] # '#E69F00' (orange)
labels = []
hideMiss = True
def descentPlot(cli, reroll, **kwargs):
	if not cli:
		kwargs = diceFromGUI()

	cached = memory.cache(rollDice)
	timeStart(0)
	global result, avgMiss, counter
	counter += 1
	if reroll:
		result, avgMiss = rollDiceCached(**kwargs)
	timeEnd(0)
	timeStart(5)
	avgRange = 0 if "ranged" not in result else sum(result["ranged"])/len(result["ranged"])
	avgDamage = 0 if "damage" not in result else sum(result["damage"])/len(result["damage"])
	if settings_surgePct:
		surge = [1 if x > 0 else 0 for x in result["surge"]] if 'surge' in result else [0]
		avgSurge = sum(surge) / len(surge)
	else:
		avgSurge = 0 if "surge" not in result else sum(result["surge"])/len(result["surge"])
	
	# Configure histogram settings
	global colors, labels, hideMiss
	if reroll:
		colors = ['#009E73', '#D55E00', '#F0E442', '#56B4E9'] # '#E69F00' (orange)
		labels = ['ranged ({0:.1f})'.format(avgRange),
				  'damage ({0:.1f})'.format(avgDamage),
				  'surge ({0:.1f})'.format(avgSurge),
				  'miss ({0:.1f}%)'.format(avgMiss * 100)]
		if settings_surgePct:
			labels[2] = 'surge ({0:.1f}%)'.format(avgSurge * 100)

		hideMiss = False
		if not settings_showMiss:
			hideMiss = True
		if "miss" not in result or sum(result["miss"]) != 0:
			hideMiss = False

		if not settings_showMiss:
			result.pop('miss', None)
		if "miss" in result and sum(result["miss"]) == 0:
			result.pop('miss', None)
			colors.pop(3)
			labels.pop(3)
		if "surge" in result and sum(result["surge"]) == 0:
			result.pop('surge', None)
			colors.pop(2)
			labels.pop(2)
		if "damage" in result and sum(result["damage"]) == 0:
			result.pop('damage', None)
			colors.pop(1)
			labels.pop(1)
		if "ranged" in result and sum(result["ranged"]) == 0:
			result.pop('ranged', None)
			colors.pop(0)
			labels.pop(0)
	
	results = list(result.values())
	minData = min(map(lambda x: min(x), results)) if len(results) > 0 else 0
	maxData = max(map(lambda x: max(x), results)) if len(results) > 0 else 0

	# Make the histogram using matplotlib
	global pltBars
	[b.remove() for b in pltBars]
	_, _, pltBars = plt.hist(results, color=colors[:max(len(result),1)], edgecolor='black', cumulative=cum_mode*cum_enabled,
		label=labels[:max(len(result),1)], bins=np.arange(minData, maxData + 0.9999, 0.9999), density=True)
	plt.style.use('dark_background')

	global figure
	figure = plt.gcf()
	figure.canvas.set_window_title('Descent: Dice Probability Distribution Graph')
	ax = plt.gca()
	if not cli:
		# Rescale the display to fit the data
		ax.relim()
		ax.autoscale_view()

	# Place a legend to the right
	handles, _ = ax.axes.get_legend_handles_labels()
	if not settings_showMiss and not hideMiss and len(results)>0:
		handles.append(mpatches.Patch(color='none', label=labels[-1]))
	plt.legend(handles=handles)
	timeEnd(5)

	timeStart(6)
	if cli:
		plt.show()
	else:
		drawPlot()
	timeEnd(6)

def plotWasClosed():
	return not plt.fignum_exists(figure.number)

def descentGUI(stdscr):
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
	window = curses.initscr()
	editwin = curses.newwin(8,2, 2,11)
	rectangle(stdscr, 1,9, 1+7+1, 1+11+1)
	
	stdscr.nodelay(True)
	selected = 0
	counter = 100
	global cum_mode, cum_enabled, cum_mode_str
	while True:
		forceUpdate = False
		# User input
		timeStart(1)
		c = stdscr.getch()
		timeEnd(1)
		timeStart(2)
		if c >= ord('0') and c <= ord('9'):
			if GUIdice[selected] != int(chr(c)):
				GUIdice[selected] = int(chr(c))
				forceUpdate = True
		elif c == ord('c') or c == ord('C'):
			cum_enabled = ~cum_enabled
		elif c == 263 or c == 330: # DEL
			if GUIdice[selected] != 0:
				GUIdice[selected] = 0
				forceUpdate = True
		elif c == 258: # down
			selected += 1
			if selected > 6:
				selected = 6
		elif c == 259: # up
			selected -= 1
			if selected < 0:
				selected = 0
		elif c == 260: # left
			if cum_mode > 0:
				cum_mode = -cum_mode
				cum_mode_str = "REV"
				forceUpdate = True
		elif c == 261: # right
			if cum_mode < 0:
				cum_mode = -cum_mode
				cum_mode_str = "FWD"
				forceUpdate = True
		elif c == 27 or plotWasClosed(): # ESC
			stdscr.addstr(0, 0, "*********QUITTING********")
			stdscr.refresh()
			plt.close('all')
			curses.endwin()
			return
		timeEnd(2)

		# Draw console
		timeStart(3)
		stdscr.addstr(10, 1, "Cumulative Mode: {} ('C' to toggle)".format("OFF" if not cum_enabled else "ON ({})".format(cum_mode_str)))
		window.clrtoeol()
		stdscr.addstr(11, 1, "Last roll took: " + ("**WAIT**" if forceUpdate else timeDiffFormatted(0)))
		window.clrtoeol()
		if settings_debug:
			stdscr.addstr(12, 1, "User input took: {:.2f}s".format(timeDiff(1)))
			window.clrtoeol()
			stdscr.addstr(13, 1, "Process input took: {:.2f}s".format(timeDiff(2)))
			window.clrtoeol()
			stdscr.addstr(14, 1, "Drawing console took: {:.2f}s".format(timeDiff(3)))
			window.clrtoeol()
			stdscr.addstr(15, 1, "Plot setup took: {:.2f}s".format(timeDiff(5)))
			window.clrtoeol()
			stdscr.addstr(16, 1, "Plot drawing took: {:.2f}s".format(timeDiff(6)))
			window.clrtoeol()
		window.refresh()
		for i in range(0,7):
			stdscr.addstr(i+2, 11, str(GUIdice[i]), curses.color_pair(1 if i == selected else 0))
			stdscr.refresh()
		timeEnd(3)

		# Draw plot
		timeStart(4)
		time.sleep(0.01)
		counter -= 1
		if counter <= 0 or forceUpdate:
			descentPlot(False, forceUpdate)
			counter = 100
			forceUpdate = False
		timeEnd(4)

def usage(exitcode):
	print("dice.py [--blue|--red|--yellow|--green|--brown|--white|--black]")
	sys.exit(exitcode)

if __name__ == "__main__":
	for i, opt in enumerate(sys.argv):
		if opt == '--':
			break
		elif '=' not in opt:
			sys.argv[i] += '='
	try:
		opts, args = getopt.getopt(sys.argv[1:],"",["blue=","red=","yellow=","green=","brown=","white=","black="])
	except getopt.GetoptError:
		usage(2)

	blu = 0; red = 0; yel = 0; gre = 0; bro = 0; whi = 0; bla = 0
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage(0)
		elif opt in ("--blue"):
			blu += 1 if arg == "" else int(arg)
		elif opt in ("--red"):
			red += 1 if arg == "" else int(arg)
		elif opt in ("--yellow"):
			yel += 1 if arg == "" else int(arg)
		elif opt in ("--green"):
			gre += 1 if arg == "" else int(arg)
		elif opt in ("--brown"):
			bro += 1 if arg == "" else int(arg)
		elif opt in ("--white"):
			whi += 1 if arg == "" else int(arg)
		elif opt in ("--black"):
			bla += 1 if arg == "" else int(arg)

	kwargs = {'blue':blu, 'red':red, 'yellow':yel, 'green':gre, 'brown':bro, 'white':whi, 'black':bla}
	cli = False
	for key, value in kwargs.items():
		if value > 0:
			cli = True

	descentSetup(cli)
	descentPlot(cli, True, **kwargs)
