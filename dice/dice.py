#!/usr/bin/env python3
import sys, getopt
import time
import itertools
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as plticker
import numpy as np
from collections import defaultdict
from IPython.core.pylabtools import figsize

settings_showPercent = False
settings_showMiss = False

matplotlib.rcParams['font.size'] = 18
matplotlib.rcParams['figure.dpi'] = 300

dies = {}

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
dies["brown"]["damage"] = [-0,-0,-0,-1,-1,-2]
dies["white"] = {}
dies["white"]["damage"] = [-0,-1,-1,-1,-2,-3]
dies["black"] = {}
dies["black"]["damage"] = [-0,-2,-2,-2,-3,-4]

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

def descent(**kwargs):
	result, avgMiss = rollDice(**kwargs)
	if not settings_showMiss:
		result.pop('miss', None)

	avgRange = 0 if "ranged" not in result else sum(result["ranged"])/len(result["ranged"])
	avgDamage = 0 if "damage" not in result else sum(result["damage"])/len(result["damage"])
	surge = [1 if x > 0 else 0 for x in result["surge"]] if 'surge' in result else [0]
	# surge = [0 if 'surge' not in result else (1 if x > 0 else 0 for x in result["surge"])]
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
	figsize(9, 7)
	plt.hist(results, color=colors[:max(len(result),1)], edgecolor='black', label=labels,
		bins=np.arange(minData, maxData + 0.9999, 0.9999), density=True)
	
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
	if not settings_showMiss and len(results)>0:
		handles.append(mpatches.Patch(color='none', label=labels[3]))
	plt.legend(handles=handles)
	plt.show()

def usage(exitcode):
	print("dice.py [--blue|--red|--yellow|--green|--brown|--white|--black]")
	sys.exit(exitcode)

if __name__ == "__main__":
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
	descent(blue=blu, red=red, yellow=yel, green=gre, brown=bro, white=whi, black=bla)
