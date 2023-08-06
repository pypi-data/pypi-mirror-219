#
# [name] nkj.func.py
# [exec] python3 -m nkj.func
#
# Written by Yoshikazu NAKAJIMA
#

import numpy as np

from nkj.str import *
from nkj.curvefit import *

#-- functions

def gauss_func(x, sigma=1.0, mu=0.0, a=1.0):
	#
	#                 (x - mu)^2
	# f(x) = a exp(- -------------)
	#                 2 * sigma^2
	#
	ldprint(["--> gauss_func(, sigma:{0:.6f}, mu:{1:.6f}, a:{2:.6f})".format(sigma, mu, a)])
	ldprint(["sigma: {}".format(sigma)])
	ldprint(["mu:    {}".format(mu)])
	ldprint(["A:     {}".format(a)])
	ldprint(["<-- gauss_func()"])
	return a * np.exp(-(x - mu)**2 / (2 * sigma**2))

def loggauss_func(x, sigma=1.0, mu=0.0, a=1.0):
	#
	#                 (x - mu)^2
	# f(x) = a exp(- -------------)
	#                 2 * sigma^2
	#
	ldprint(["--> loggauss_func(, sigma:{0:.6f}, mu:{1:.6f}, a:{2:.6f})".format(sigma, mu, a)])
	ldprint(["sigma: {}".format(sigma)])
	ldprint(["mu:    {}".format(mu)])
	ldprint(["A:     {}".format(a)])
	ldprint(["<-- loggauss_func()"])
	xp = np.log(x)
	return a * np.exp(-(xp - mu)**2 / (2 * sigma**2))

def sigmoid_func(x, tau=1.0, x0=0.0, b=0.0, a=1.0):
	#
	#                    1
	# f(x) = ------------------------- + b
	#         1 + exp(-(x - x0) / tau)
	#
	if (tau == 0.0):
		return b if (x < x0) else a + b
	if (tau < 0.0):
		print_warning("Tau should be positive in nkj.func.sigmoid_func()")
	return a / (1.0 + np.exp(-(x - x0) / tau)) + b if (np.abs(tau) > 1.0e-32) else b

def logsigmoid_func(x, tau=1.0, x0=0.0, b=0.0, a=1.0):
	#
	#                    1
	# f(x) = ------------------------- + b
	#         1 + exp(-(x - x0) / tau)
	#
	# x 軸に関係する x, tau, x0 のうち、x のみ対数変換して計算する．tau, x0 は、変数入力時に対数計算されるか、実数軸で表現されるかのどちらかと仮定．
	#
	tauabs = np.abs(tau)
	if (tauabs < 1.0e-32):
		return b
	logtau = np.log(tauabs)
	if (logtau == 0.0):
		return b if (x < x0) else a + b
	if (logtau < 0.0):
		print_warning("Tau should be positive in nkj.func.logsigmoid_func().")
	xabs = np.abs(x)
	if (xabs < 1.0e-32):
		return b
	xp = np.log(xabs)
	return a / (1.0 + np.exp(-(xp - x0) / logtau)) + b if (np.abs(tau) > 1.0e-32) else b

def extreme_func(x, w=1.0, xc=0.0, a=1.0):
	#
	#                         x - xc      x - xc
	# f(x) = A * exp [-exp(- --------) - -------- + 1]
	#                           w           w
	#
	return a * np.exp(-np.exp(-(x - xc) / w) - (x - xc) / w + 1)

def logextreme_func(x, w=1.0, xc=0.0, a=1.0):
	#
	#                         x - xc      x - xc
	# f(x) = A * exp [-exp(- --------) - -------- + 1]
	#                           w           w
	#
	xp = np.log(x)
	return a * np.exp(-np.exp(-(xp - xc) / w) - (xp - xc) / w + 1)

def erf_func(x):
	return sigmoid(x)

def gauss_cumulativeprobabilitydensity_func(x):
	#
	#           1              x
	# PHI(x) = --- (1 + erf(--------)
	#           2            sqrt(2)
	#
	return 0.5 * (1.0 + erf_func(x / np.sqrt(2.0)))

def skewnormal_func(psi, omega, alpha=0.0):   # Skew-Normal (SN) distribution
	#
	#                 1                x^2
	# phi(x) = -------------- * exp(- -----)
	#           sqrt(2 * pi)            2
	#
	#
	x = psi
	phi = gauss_func(x, 1.0, 0.0, 1.0 / np.sqrt(2.0 * np.pi))
	PHI = gauss_cumulativeprobabilitydensity_func(alpha * x)
	return 2.0 * phi * PHI

#-- statistics

def gauss_statistics(x):
	nk.ldprint(["--> gauss_statistics()"])
	mu = np.mean(x)
	sigma = np.std(x)
	nk.ldprint2(["mu:    {}".format(mu)])
	nk.ldprint2(["sigma: {}".format(sigma)])
	if (False):
		ave = 0.0
		for i in range(len(x)):
			ave += x[i]
		ave /= float(len(x))
		nk.ldprint2(["ave:   {}".format(ave)])
	if (False):
		dev = 0.0
		for i in range(len(x)):
			dev += (x[i] - mu)**2
		dev /= float(len(x))
		std = np.sqrt(dev)
		nk.ldprint2(["std:   {}".format(std)])
	nk.ldprint(["<-- gauss_statistics(): mu:{0:.6f}, sigma:{1:.6f}".format(mu, sigma)])
	return tuple((mu, sigma))

#-- classes

class gauss():
	_classname = "nkj.func.gauss"

	def __init__(self, sigma=1.0, mu=0.0, a=1.0):
		self._sigma = sigma
		self._mu = mu
		self._a = a

	def __str__(self):
		return "gauss(sigma:{0:.6f}, mu:{1:.6f}, a:{2:.6f})".format(self.getSigma(), self.getMu(), self.getA())

	@classmethod
	def getClassName(cls):
		return gauss._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getSigma(self):
		return self._sigma

	def setSigma(self, sigma):
		self._sigma = sigma

	@property
	def sigma(self):
		return self.getSigma()

	@sigma.setter
	def sigma(self, s):
		self.setSigma(s)

	def getVariance(self):
		return self.getSigma()**2

	def setVariance(self, var):
		self.setSigma(np.sqrt(var))

	@property
	def variance(self):
		return self.getVariance()

	@variance.setter
	def variance(self, var):
		self.setVariance(var)

	def getVar(self):
		return self.getVariance()

	def setVar(self, var):
		self.setVariance(var)

	@property
	def var(self):
		return self.getVar()

	@var.setter
	def var(self, v):
		self.setVar(v)

	def getMu(self):
		return self._mu

	def setMu(self, mu):
		self._mu = mu

	@property
	def mu(self):
		return self.getMu()

	@mu.setter
	def mu(self, m):
		self.setMu(m)

	def getX0(self):
		return self.getMu()
	
	def setX0(self, x0):
		self.setMu(x0)

	@property
	def x0(self):
		return self.getX0()

	@x0.setter
	def x0(self, mu):
		self.setX0(mu)

	def getN(self):
		return tuple((self.getMu(), self.getSigma()))

	def setN(self, n:tuple):
		self.setMu(n[0])
		self.setSigma(n[1])

	@property
	def N(self):
		return self.getN()

	@N.setter
	def N(self, n:tuple):
		self.setN(n)

	def getA(self):
		return self._a

	def setA(self, a):
		self._a = a

	@property
	def A(self):
		return self.getA()

	@A.setter
	def A(self, a):
		self.setA(a)

	def getGain(self):
		return self.getA()

	def setGain(self, gain):
		self.setA(gain)

	@property
	def gain(self):
		return self.getGain()

	@gain.setter
	def gain(self, g):
		self.setGain(g)

	def set(self, sigma=1.0, mu=0.0, a=1.0):
		self.setSigma(sigma)
		self.setMu(mu)
		self.setA(a)

	def get(self, x, sigma=None, mu=None, a=None):
		if (sigma is None):
			sigma = self.getSigma()
		if (mu is None):
			mu = self.getMu()
		if (a is None):
			a = self.getA()
		return gauss_func(x, sigma, mu, a)

	def val(self, x, sigma=None, mu=None, a=None):
		return self.get(x, sigma, mu, a)

	def fit(self, x, y, mu=None):
		ldprint(["--> gauss.fit(,, mu:{})".format(mu)])
		sigma, mu, a = gauss_fit(x, y, mu)
		self.set(sigma, mu, a)
		ldprint(["sigma: {}".format(self.getSigma())])
		ldprint(["mu:    {}".format(self.getMu())])
		ldprint(["a:     {}".format(self.getA())])
		ldprint(["<-- gauss.fit(): sigma:{0:.6f}, mu:{1:.6f}, a:{2:.6f}".format(self.getSigma(), self.getMu(), self.getA())])
		return sigma, mu, a

	def statistics(self, x):
		ldprint(["--> gauss.statistics()"])
		(mu, sigma) = gauss_statistics(x)
		self.setN((mu, sigma))
		ldprint(["<-- gauss.statistics()"])

class sigmoid():
	_classname = "nkj.func.sigmoid"
	"""
	_SIGMOID_TAU_SIGMA_COEFFICIENT = 1.66641484118516331581
	"""
	_SIGMOID_TAU_SIGMA_COEFFICIENT = 1.68197638782478364754

	def __init__(self, tau=1.0, x0=0.0, b=0.0, a=1.0):
		self._tau = tau
		self._x0 = x0
		self._b = b
		self._a = a

	def __str__(self):
		return "gauss(tau:{0:.6f}, x0:{1:.6f}, b:{2:.6f}, a:{3:.6f})".format(self.getTau(), self.getX0(), self.getB(), self.getA())

	@classmethod
	def getClassName(cls):
		return sigmoid._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getTau(self):
		return self._tau

	def setTau(self, tau):
		if (tau < 1.0):
			print_warning("The value less than 1 is given for tau.")
		self._tau = tau

	@property
	def tau(self):
		return self.getTau()

	@tau.setter
	def tau(self, t):
		self.setTau(t)

	def getSigma(self):
		#
		# tau = sqrt(2 * sigma^2) = sqrt(2) * sigma
		# sigma = tau / sqrt(2)
		#
		"""
		return self.getTau() / np.sqrt(2.0)
		"""
		return self._SIGMOID_TAU_SIGMA_COEFFICIENT * self.getTau()

	def setSigma(self, sigma):
		#
		# tau = sqrt(2 * sigma^2) = sqrt(2) * sigma
		#
		"""
		self.setTau(np.sqrt(2.0) * sigma)
		self.setTau(sigma / 2.0)
		"""
		self.setTau(sigma / self._SIGMOID_TAU_SIGMA_COEFFICIENT)

	@property
	def sigma(self):
		return self.getSigma()

	@sigma.setter
	def sigma(self, s):
		self.setSigma(s)

	def getVariance(self):
		return self.getSigma()**2

	def setVariance(self, var):
		self.setSigma(np.sqrt(var))

	@property
	def variance(self):
		return self.getVariance()

	@variance.setter
	def variance(self, var):
		self.setVariance(var)

	def getVar(self):
		return self.getVariance()

	def setVar(self, var):
		self.setVariance(var)

	@property
	def var(self):
		return self.getVar()

	@var.setter
	def var(self, v):
		self.setVar(v)

	def getX0(self):
		return self._x0

	def setX0(self, x0):
		self._x0 = x0

	@property
	def x0(self):
		return self.getX0()

	@x0.setter
	def x0(self, x0):
		self.setX0(x0)

	def getMu(self):
		return self.getX0()

	def setMu(self, mu):
		self.setX0(mu)

	@property
	def mu(self):
		return self.getMu()

	@mu.setter
	def mu(self, m):
		self.setMu(m)

	def getN(self):
		return tuple((self.getMu(), self.getSigma()))

	def setN(self, n:tuple):
		self.setMu(n[0])
		self.setSigma(n[1])

	@property
	def N(self):
		return self.getN()

	@N.setter
	def N(self, n:tuple):
		self.setN(n)

	def getB(self):
		return self._b

	def setB(self, b):
		self._b = b

	@property
	def b(self):
		return self.getB()

	@b.setter
	def b(self, b):
		self.setB(b)

	def getOffset(self):
		return self.getB()

	def setOffset(self, offset):
		self.setB(offset)

	@property
	def offset(self):
		return self.getOffset()

	@offset.setter
	def offset(self, offset):
		self.setOffset(offset)

	def getA(self):
		return self._a

	def setA(self, a):
		self._a = a

	@property
	def A(self):
		return self.getA()

	@A.setter
	def A(self, a):
		self.setA(a)

	def getGain(self):
		return self.getA()

	def setGain(self, gain):
		self.setA(gain)

	@property
	def gain(self):
		return self.getGain()

	@gain.setter
	def gain(self, g):
		self.setGain(g)

	def set(self, tau=1.0, x0=0.0, b=0.0, a=1.0):
		self.setTau(tau)
		self.setX0(x0)
		self.setB(b)
		self.setA(a)

	def get(self, x, tau=None, x0=None, b=None, a=None):
		if (tau is None):
			tau = self.getTau()
		if (x0 is None):
			x0 = self.getX0()
		if (b is None):
			b = self.getB()
		if (a is None):
			a = self.getA()
		return sigmoid_func(x, tau, x0, b, a)

	def get_log(self, x, tau=None, x0=None, b=None, a=None):
		if (tau is None):
			tau = self.getTau()
		if (x0 is None):
			x0 = self.getX0()
		if (b is None):
			b = self.getB()
		if (a is None):
			a = self.getA()
		return logsigmoid_func(x, tau, x0, b, a)

	def logget(self, x, tau=None, x0=None, b=None, a=None):
		return self.get_log(x, tau, x0, b, a)

	def val(self, x, tau=None, x0=None, b=None, a=None):
		return self.get(x, tau, x0, b, a)

	def logval(self, x, tau=None, x0=None, b=None, a=None):
		return self.get_log(x, tau, x0, b, a)

	def log(self, x, tau=None, x0=None, b=None, a=None):
		return self.logval(x, tau, x0, b, a)

	def fit(self, x, y, b=None, a=None):
		ldprint(["--> sigmoid.fit(,, b:{0}, a:{1})".format(b, a)])
		tau, x0, b, a = sigmoid_fit(x, y, b, a)
		self.set(tau, x0, b, a)
		ldprint(["<-- sigmoid.fit()".format()])
		return tau, x0, b, a

class extreme():
	_classname = "nkj.func.extreme"

	def __init__(self, w=1.0, xc=0.0, a=1.0):
		self._w = w
		self._xc = xc
		self._a = a

	def __str__(self):
		return "extreme(w:{0:.6f}, xc:{1:.6f}, a:{2:.6f})".format(self.getW(), self.getXc(), self.getA())

	@classmethod
	def getClassName(cls):
		return extreme._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getW(self):
		return self._w

	def setW(self, w):
		self._w = w

	@property
	def w(self):
		return self.getW()

	@w.setter
	def w(self, w):
		self.setW(w)

	def getXc(self):
		return self._xc

	def setXc(self, xc):
		self._xc = xc

	@property
	def xc(self):
		return self.getXc()

	@xc.setter
	def xc(self, xc):
		self.setXc(xc)

	def getA(self):
		return self._a

	def setA(self, a):
		self._a = a

	@property
	def A(self):
		return self.getA()

	@A.setter
	def A(self, a):
		self.setA(a)

	def getGain(self):
		return self.getA()

	def setGain(self, gain):
		self.setA(gain)

	@property
	def gain(self):
		return self.getGain()

	@gain.setter
	def gain(self, g):
		self.setGain(g)

	def set(self, w=1.0, xc=0.0, a=1.0):
		self.setW(w)
		self.setXc(xc)
		self.setA(a)

	def get(self, x, w=None, xc=None, a=None):
		if (w is None):
			w = self.getW()
		if (xc is None):
			xc = self.getXc()
		if (a is None):
			a = self.getA()
		return extreme_func(x, w, xc, a)

	def val(self, x, w=None, xc=None, a=None):
		return self.get(x, w, mu, a)

	def fit(self, x, y, xc=None):
		ldprint(["--> extreme.fit(,, xc:{})".format(xc)])
		w, xc, a = extreme_fit(x, y, xc)
		self.set(w, xc, a)
		ldprint(["<-- extreme.fit(): w:{0:.6f}, xc:{1:.6f}, a:{2:.6f}".format(w, xc, a)])
		return w, xc, a

#-- main

if (__name__ == '__main__'):
	import numpy as np
	import matplotlib.pyplot as plt

	lib_debuglevel(2)

	if (True): # Gauss
		print("gauss_classname: \"{}\"".format(gauss.classname))

		gsigma = 1.0
		gmu = 0.0
		ga = 1.0

		print("sigma: {}".format(gsigma))
		print("mu:    {}".format(gmu))
		print("A:     {}".format(ga))

		x = np.arange(-5, 5, 0.1)
		y = gauss_func(x, gsigma, gmu, ga)
		plt.plot(x, y)

		if (True):
			gau = gauss()
			sigma, mu, a = gau.fit(x, y)
			print("sigma: {}".format(sigma))
			print("mu:    {}".format(mu))
			print("A:     {}".format(a))
			y2 = gau.get(x)
			plt.plot(x, y2, 'x')

		plt.show()

		if (False):
			gauss = gauss(2.0 * gsigma, gmu, 0.5 * ga)
			y = gauss.get(x)
			plt.plot(x, y)
			plt.show()

	if (True): # Sigmoid
		print("sigmoid_classname: \"{}\"".format(sigmoid.classname))

		tau = 1.0
		x0 = 0.0
		b = 0.0
		a = 1.0

		print("tau:  {}".format(tau))
		print("x0:   {}".format(x0))
		print("b:    {}".format(b))
		print("A:    {}".format(a))

		x = np.arange(-5, 5, 0.1)
		y = sigmoid_func(x, tau, x0, b, a)
		plt.plot(x, y)

		if (True):
			sig = sigmoid()
			tau, x0, b, a = sig.fit(x, y)
			print("tau:  {}".format(tau))
			print("x0:   {}".format(x0))
			print("b:    {}".format(b))
			print("A:    {}".format(a))
			y2 = sig.get(x)
			plt.plot(x, y2, 'x')

		plt.show()

		if (False):
			sig = sigmoid(2.0 * tau, x0, b, 0.5 * a)
			y = sig.get(x)
			plt.plot(x, y)
			plt.show()

	if (True): # Extreme
		print("extreme_classname: \"{}\"".format(extreme.classname))

		w = 1.0
		xc = 0.0
		a = 1.0

		print("w:  {}".format(w))
		print("xc: {}".format(xc))
		print("A:  {}".format(a))

		x = np.arange(-5, 5, 0.1)
		y = extreme_func(x, w, xc, a)
		plt.plot(x, y)

		if (True):
			ext = extreme()
			w, xc, a = ext.fit(x, y)
			y2 = ext.get(x)
			plt.plot(x, y2, 'x')

		plt.show()

		if (False):
			ext = extreme(2.0 * w, xc, 0.5 * a)
			y = ext.get(x)
			plt.plot(x, y)
			plt.show()
