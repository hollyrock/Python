"""Scipy_sinepy

Blow is same behavior in interactive mode:

Print sine of one angle:

>>> np.sin(np.pi/2.)
1.0
Print sines of an array of angles given in degrees:

>>> np.sin(np.array((0., 30., 45., 60., 90.)) * np.pi / 180. )
array([ 0.        ,  0.5       ,  0.70710678,  0.8660254 ,  1.        ])
Plot the sine function:

>>> import matplotlib.pylab as plt
>>> x = np.linspace(-np.pi, np.pi, 201)
>>> plt.plot(x, np.sin(x))
>>> plt.xlabel('Angle [rad]')
>>> plt.ylabel('sin(x)')
>>> plt.axis('tight')
>>> plt.show()

"""
import argparse

import numpy as np
from scipy import special, optimize
import matplotlib.pylab as plt

def main():
	# Parse command-line arguments
	parser = argparse.ArgumentParser(usage=__doc__)
	parser.add_argument("--order", type=int, default=3, help="order of Bessel function")
	parser.add_argument("--output", default="sine.png", help="output image file")
	args = parser.parse_args()

	# Compute sine curve
	x = np.linspace(0, 2*np.pi, 201)

	# Plot
	plt.plot(x, np.sin(x))
	plt.xlabel('Angle [rad]')
	plt.ylabel('sin(x)')
	plt.axis('tight')
	plt.show()
	
	# Produce output
	plt.savefig(args.output, dpi=96)

if __name__ == "__main__":
	main()