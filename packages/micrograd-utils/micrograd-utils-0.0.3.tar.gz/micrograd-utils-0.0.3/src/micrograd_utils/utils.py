#!/bin/python3

from micrograd.engine import *
from micrograd.nn import *

def dump_parameters(m, filename="params.txt"):
	nout = []
	for l in range(len(m.layers)):
		if l == 0:
			nin = len(m.layers[l].neurons[0].w)
		nout.append(len(m.layers[l].neurons))
			
	with open(filename, "w") as f:
		f.write("MLP(" + str(nin) + ", " + str(nout) + ")")
		f.write("\n")
		f.write(str(['Value(data=' + str(v.data) + ')' for v in m.parameters()]).replace("'",""))

def load_parameters(filename="params.txt"):
	with open(filename, "r") as f:
		lines = f.readlines()
		model = eval(lines[0])
		params = eval(lines[1])
		for p, q in zip(model.parameters(), params):
			p.data = q.data
	return model


