# -*- coding: utf-8 -*-

import math

p = 0.5

#combination
def xCy(x,y):
	return math.factorial(x)/(math.factorial(x-y) * math.factorial(y))

def alpha(i,k):
	ans = p**((i-k)*k)

	for el in range(1,i-k):
		temp = xCy(i-k-1,el)
		temp *= (1-p**k)**el
		temp *= p**((i-k-el)*k)
		temp *= alpha(i-k,el)

		ans += temp

	return ans


def main():
	n = input("n:")
	print alpha(n,1)

if __name__ == "__main__":
	main()