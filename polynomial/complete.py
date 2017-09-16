# coding:utf-8

"""
完全グラフにおける漏えい確率を
信頼度の漸化式から求めてみる
"""

import math
import numpy as np
from numpy.polynomial.polynomial import polyval
from numpy.polynomial.polynomial import polypow


#combination
def xCy(x,y):
	return math.factorial(x)/(math.factorial(x-y) * math.factorial(y))

# p^kを返す
def retpow(k):
	x = np.poly1d([1])
	for i in range(k):
		x *= np.poly1d([1,0])
	return x

# 完全グラフKnにおける全端子信頼度Anを返す
def retAn(n):
	ans = np.poly1d([0])
	for j in range(1,n):	#j=1 -- n-1
		ans += np.poly1d([xCy(n-1,j-1)]) * retAn(j) * retpow(j*(n-j))
	return 1 - ans

def retEps(n):
	ans = np.poly1d([0])
	for j in range(1,n): 	#j=1 -- n-1
		ans += np.poly1d([xCy(n-2,j-1)]) * retAn(j) * retpow(j*(n-j))
	return ans

def main():
	n = input("n : ")
	print retPoly(retEps(n))
	return


# numpyオブジェクトを多項式の文字列に直して返す
def retPoly(polyobj):
	# 次数で昇順にする

	coef = polyobj.c[::-1]
	ans = ""

	if coef[0] > 0:
		ans += " + %d" % coef[0]
	elif coef[0] < 0:
		ans += " - %d" % abs(coef[0])

	for i in range(1,len(coef)):
		if coef[i] != 0:
			if coef[i] == 1:
				ans += " + "
			elif coef[i] > 1:
				ans += " + %d" % coef[i]
			elif coef[i] < 0:
				ans += " - %d" % abs(coef[i])
			ans += "p^{%d}" % i

	if ans[1] == "+":
		return ans[2:]
	else:
		return ans


if __name__ == "__main__":
	main()