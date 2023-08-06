#
# [name] nkj.curvefit.py
# [exec] python3 -m nkj.scipy
#
# Written by Yoshikazu NAKAJIMA

import numpy as np
import scipy as sp
from scipy.optimize import curve_fit

import nkj as nk

# Gauss

def gauss_fit_mu0(x, y, mu0):
	nk.ldprint(["--> gauss_fit_mu0(,, mu0:{}".format(mu0)])
	mu = mu0
	def gauss_f(x, sigma, a):
		#
		#                 (x - mu)^2
		# f(x) = a exp(- -------------)
		#                 2 * sigma^2
		#
		return a * np.exp(-(x - mu)**2 / (2 * sigma**2))

	popt, pcov = curve_fit(gauss_f, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	sigma = popt[0]
	a = popt[1]

	nk.ldprint2("sigma: {}".format(sigma))
	nk.ldprint2("mu:    {}".format(mu))
	nk.ldprint2("a:     {}".format(a))

	nk.ldprint(["<-- sigmiod_fit(): sigma:{0:.6f}, a:{1:.6f}".format(sigma, a)])
	return sigma, a

def gauss_fit(x, y, mu=None):
	nk.ldprint(["--> gauss_fit(,, mu:{}".format(mu)])

	if (mu is not None):
		sigma, a = gauss_fit_mu0(x, y, mu)
		nk.ldprint(["<-- gauss_fit(): sigma:{0:.6f}, mu:{1:.6f}, a:{2:.6f}".format(sigma, mu, a)])
		return sigma, mu, a

	def gauss_f(x, sigma, mu, a):
		#
		#                 (x - mu)^2
		# f(x) = a exp(- -------------)
		#                 2 * sigma^2
		#
		return a * np.exp(-(x - mu)**2 / (2 * sigma**2))

	popt, pcov = curve_fit(gauss_f, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	sigma = popt[0]
	mu = popt[1]
	a = popt[2]

	nk.ldprint2("sigma: {}".format(sigma))
	nk.ldprint2("mu:    {}".format(mu))
	nk.ldprint2("a:     {}".format(a))

	nk.ldprint(["<-- gauss_fit(): sigma:{0:.6f}, mu:{1:.6f}, a:{2:.6f}".format(sigma, mu, a)])
	return sigma, mu, a

# Sigmoid

def sigmoid_fit_b0a0(x, y, b0=0.0, a0=1.0):
	nk.ldprint(["--> sigmiod_fit_b0a0(,, b0:{0}, a0:{1})".format(b0, a0)])
	b = b0
	a = a0
	def sigmoid_f_b0a0(x, tau, x0):
		#
		#                    a
		# f(x) = -------------------------- + b
		#         1 + exp(-(x - x0) / tau)
		#
		return a / (1.0 + np.exp(-(x - x0) / tau)) + b

	popt, pcov = curve_fit(sigmoid_f_b0a0, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	tau = popt[0]
	x0 = popt[1]

	nk.ldprint2("tau: {}".format(tau))
	nk.ldprint2("x0:  {}".format(x0))

	nk.ldprint(["<-- sigmiod_fit_b0a0(): tau:{0:.6f}, x0:{1:.6f}".format(tau, x0)])
	return tau, x0

def sigmoid_fit_a0(x, y, a0=1.0):
	nk.ldprint(["--> sigmiod_fit_a0()"])
	a = a0
	def sigmoid_f_a0(x, tau, x0, b):
		#
		#                    a
		# f(x) = -------------------------- + b
		#         1 + exp(-(x - x0) / tau)
		#
		return a / (1.0 + np.exp(-(x - x0) / tau)) + b

	popt, pcov = curve_fit(sigmoid_f_a0, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	tau = popt[0]
	x0 = popt[1]
	b = popt[2]

	nk.ldprint2("tau: {}".format(tau))
	nk.ldprint2("x0:  {}".format(x0))
	nk.ldprint2("b:   {}".format(b))

	nk.ldprint(["<-- sigmiod_fit_a0(): tau:{0:.6f}, x0:{1:.6f}, b:{2:.6f}".format(tau, x0, b)])
	return tau, x0, b

def sigmoid_fit_b0(x, y, b0=0.0):
	nk.ldprint(["--> sigmiod_fit_b0()"])
	b = b0
	def sigmoid_f_b0(x, tau, x0, a):
		#
		#                    a
		# f(x) = -------------------------- + b
		#         1 + exp(-(x - x0) / tau)
		#
		return a / (1.0 + np.exp(-(x - x0) / tau)) + b

	popt, pcov = curve_fit(sigmoid_f_b0, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	tau = popt[0]
	x0 = popt[1]
	a = popt[2]

	nk.ldprint2("tau: {}".format(tau))
	nk.ldprint2("x0:  {}".format(x0))
	nk.ldprint2("a:   {}".format(a))

	nk.ldprint(["<-- sigmiod_fit_b0(): tau:{0:.6f}, x0:{1:.6f}, a:{2:.6f}".format(tau, x0, a)])
	return tau, x0, a

def sigmoid_fit(x, y, b0=None, a0=None):
	nk.ldprint(["--> sigmoid_fit(,, b0:{0}, a0:{1})".format(b0, a0)])
	if (b0 is not None):
		if (a0 is not None):  # fix b and a
			tau, x0 = sigmoid_fit_b0a0(x, y, b0, a0)
			nk.ldprint(["<-- sigmoid_fit(): tau:{0:.6f}, x0:{1:.6f}, b:{2:.6f}, a:{3:.6f}".format(tau, x0, b0, a0)])
			return tau, x0, b0, a0
		else:  # estimate a and fix b
			tau, x0, a = sigmoid_fit_b0(x, y, b0)
			nk.ldprint(["<-- sigmoid_fit(): tau:{0:.6f}, x0:{1:.6f}, b:{2:.6f}, a:{3:.6f}".format(tau, x0, b0, a)])
			return tau, x0, b0, a
	elif (a0 is not None):  # estimate b and fix a
			tau, x0, b = sigmoid_fit_a0(x, y, b0)
			nk.ldprint(["<-- sigmoid_fit(): tau:{0:.6f}, x0:{1:.6f}, b:{2:.6f}, a:{3:.6f}".format(tau, x0, b, a0)])
			return tau, x0, b, a0

	# estimate b and a

	def sigmoid_f(x, tau, x0, b, a):
		#
		#                    a
		# f(x) = -------------------------- + b
		#         1 + exp(-(x - x0) / tau)
		#
		return a / (1.0 + np.exp(-(x - x0) / tau)) + b

	popt, pcov = curve_fit(sigmoid_f, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	tau = popt[0]
	x0 = popt[1]
	b = popt[2]
	a = popt[3]

	nk.ldprint2("tau: {}".format(tau))
	nk.ldprint2("x0:  {}".format(x0))
	nk.ldprint2("b:   {}".format(b))
	nk.ldprint2("a:   {}".format(a))

	nk.ldprint(["<-- sigmiod_fit(): tau:{0:.6f}, x0:{1:.6f}, b:{2:.6f}, a:{3:.6f}".format(tau, x0, b, a)])
	return tau, x0, b, a

# Extreme

def extreme_fit_x0(x, y, x0:float):
	nk.ldprint(["--> extreme_fit_x0(,, {})".format(x0)])
	nk.ldprint2(["x0: {}".format(x0)])
	nk.ldprint2(["x0.type: {}".format(type(x0))])
	xc = x0
	def extreme_f(x, w, a):
		#
		#                         x - xc      x - xc
		# f(x) = A * exp [-exp(- --------) - -------- + 1] + b
		#                           w           w
		#
		# ここでは +b （バイアス）は考えない
		#
		return a * np.exp(-np.exp(-(x - xc) / w) - (x - xc) / w + 1)

	popt, pcov = curve_fit(extreme_f, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	w = popt[0]
	a = popt[1]

	nk.ldprint2("w:  {}".format(w))
	nk.ldprint2("a:  {}".format(a))

	nk.ldprint(["<-- extreme_fit_x0(): w:{0:.6f}, a:{1:.6f}".format(w, a)])
	return w, a

def extreme_fit(x, y, x0=None):
	nk.ldprint(["--> extreme_fit(,, {})".format(x0)])
	nk.ldprint2(["x0: {}".format(x0)])

	if (x0 is not None):
		w, a = extreme_fit_x0(x, y, x0)
		nk.ldprint(["<-- extreme_fit(): a:{0:.6f}, xc:{1:.6f}, w:{2:.6f}".format(a, x0, w)])
		return w, x0, a

	def extreme_f(x, w, xc, a):
		#
		#                         x - xc      x - xc
		# f(x) = A * exp [-exp(- --------) - -------- + 1]
		#                           w           w
		#
		return a * np.exp(-np.exp(-(x - xc) / w) - (x - xc) / w + 1)

	popt, pcov = curve_fit(extreme_f, x, y)
	nk.ldprint2(["popt: {}".format(popt)])
	nk.ldprint2(["pcov: {}".format(pcov)])

	w = popt[0]
	xc = popt[1]
	a = popt[2]

	nk.ldprint2("w:  {}".format(w))
	nk.ldprint2("xc: {}".format(xc))
	nk.ldprint2("a:  {}".format(a))

	nk.ldprint(["<-- extreme_fit(): w:{0:.6f}, xc:{1:.6f}, a:{2:.6f}".format(w, xc, a)])
	return w, xc, a

