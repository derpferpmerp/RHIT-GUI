import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import math
import random
from numpy.random import randint as rnd

def genrd(width=81, height=51, complexity=.75, density =.75, b=True, bl=False):
	if b:
		shape = ((height//2)*2 + 1, (width//2)*2 + 1)
	else:
		shape = ((height//2)*2, (width//2)*2)
	complexity = int(complexity*(5*(shape[0]+shape[1])))
	density    = int(density*(shape[0]//2*shape[1]//2))
	Z = np.zeros(shape, dtype=bool)
	if b:
		Z[0,:] = Z[-1,:] = 1
		Z[:,0] = Z[:,-1] = 1
	for i in range(density):
		x, y = rnd(0,shape[1]//2)*2, rnd(0,shape[0]//2)*2
		Z[y,x] = 1
		for j in range(complexity):
			neighbours = []
			if x > 1:           neighbours.append( (y,x-2))
			if x < shape[1]-2:  neighbours.append( (y,x+2))
			if y > 1:           neighbours.append( (y-2,x))
			if y < shape[0]-2:  neighbours.append( (y+2,x))
			if len(neighbours):
				y_,x_ = neighbours[rnd(0,len(neighbours)-1)]
				if Z[y_,x_] == 0:
					Z[y_,x_] = 1
					Z[y_+(y-y_)//2, x_+(x-x_)//2] = 1
					x, y = x_, y_
	return [1 * Z if not bl else Z][0]


plt.style.use("dark_background")
sg.theme('Black')
def gen_rand_grid(d, density=1, opt="NICE", cmp=0.75):
	if opt == "RANDOM":
		try:
			grid = np.zeros((d, d), int)
			choices = np.random.choice(grid.size,random.randrange(round((3 / 4) * d * density), d * density), replace=False)
			grid.ravel()[choices] = 1
			return grid
		except ValueError:
			return None
	else:
		return genrd(width=d,height=d,density=round(3/4 * d) * density,complexity=cmp)

def distance(x1,y1,x2,y2):
	return round(math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2))

def gen_ending_coords(arr,sx,sy,seek=0):
	dcoords, ddist = [[],[]]
	for x,y in [list(g) for g in list(zip(*np.nonzero(arr == seek)))]:
		dcoords.append([x,y])
		ddist.append(distance(x,y,sx,sy))
	maxval = dcoords[ddist.index(max(ddist))]
	return maxval

def draw_plot(w=10,h=10,c=0.75,d=0.75,brdr=True,m=0.5,bl2=False,grid=False):
	grd = gen_rand_grid(w, density=d, opt="NICE", cmp=c)
	grid=grd
	xs,ys = [1,1]
	xe,ye = gen_ending_coords(grd,xs,ys)
	grd[xe,ye]=2
	grd[xs,ys]=3
	plt.figure(figsize=(10,10),dpi=100)
	cmap = colors.ListedColormap(["white", "black","#39ff14","red","blue"])
	bounds=[0,0.9,1.9,2.9,3.9,4.9]
	norm = colors.BoundaryNorm(bounds, cmap.N)
	if type(grid) == type(True):
		mzgenned = genrd(width=w,height=h,complexity=c,density=d,b=brdr,bl=bl2)
	else:
		mzgenned = grid
	plt.imshow(mzgenned,cmap=cmap,norm=norm,interpolation="nearest")
	plt.xticks([]),plt.yticks([])
	plt.style.use("dark_background")
	plt.show(block=False)

layout = [
	[
	sg.Text('Width: ', size=(15, 1)),sg.Slider(
        (5, 25),
        10,
        1,
        orientation="h",
        size=(20, 15),
        key="-WIDTH SLIDER-",
				enable_events=True
    )
	],
	[
	sg.Text('Complexity: ', size=(15, 1)),
	sg.Slider(
        (0.1, 1),
        0.5,
        0.01,
        orientation="h",
        size=(20, 15),
        key="-COMPLEXITY SLIDER-",
				enable_events=True
    )
	],
	[
	sg.Text('Density: ', size=(15, 1)),
	sg.Slider(
        (0.1, 1),
        0.5,
        0.01,
        orientation="h",
        size=(20, 15),
        key="-DENSITY SLIDER-",
				enable_events=True
    )
	],
	[sg.Button("Generate Graph")]
]


window = sg.Window(title="PacMan Config", layout=layout, margins=(100, 50))
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
		print(values)
		break
	elif event == 'Generate Graph':
		dens,compl,ws = [0.75,0.75,10]
		if values["-DENSITY SLIDER-"]:
			dens = float(values["-DENSITY SLIDER-"])
		if values["-COMPLEXITY SLIDER-"]:
			compl = float(values["-COMPLEXITY SLIDER-"])
		if values["-WIDTH SLIDER-"]:
			ws = int(round(float(values["-WIDTH SLIDER-"])))
		draw_plot(w=ws,h=ws,c=compl,d=dens)