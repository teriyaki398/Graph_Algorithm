# -*- coding: utf-8 -*-

import math
SIZE = input("SIZE:")


#combination
def xCy(x,y):
	return math.factorial(x)/(math.factorial(x-y) * math.factorial(y))


#足し算
def plus(a,b):
	temp = range(SIZE)
	for i in range(SIZE):
		temp[i] = a[i] + b[i]
	return temp


#整数との掛け算
def mulk(k,a):
	temp = range(SIZE)
	for i in range(SIZE):
		temp[i] = a[i] * k
	return temp


#掛け算
def mul(a,b):
	temp = range(SIZE)
	#安全な初期化　[0]*SIZEでいいかもしれない
	for i in range(SIZE):
		temp[i] = 0

	for i in range(len(a)):
		for j in range(len(b)):
			if(i+j < SIZE):
				temp[i+j] += a[i] * b[j]
	return temp


#(1-p^k)^l　の多項式を求める
def nikou(k,el):
	temp = range(SIZE)
	for i in range(SIZE):
		temp[i] = 0
	for i in range(el+1):
		temp[k*i] = xCy(el,i) * (-1)**i
	return temp


def poly(i,k):
	temp = range(SIZE)
	for j in range(SIZE):
		temp[j] = 0
	temp[(i-k)*k] = 1

	for el in range(1,i-k):
		X = xCy(i-k-1,el)
		Y = nikou(k,el)
		XY = mulk(X,Y)

		Z = range(SIZE)
		for j in range(SIZE):
			Z[j] = 0
		Z[(i-k-el)*k] = 1
		XYZ = mul(XY,Z)

		W = mul(XYZ,poly(i-k,el))

		temp = plus(temp, W)

	return temp




def main():
	n = input("N:")
	temp = poly(n,1)
	ans = ""
	for i in range(SIZE):
		if(temp[i] != 0):
			ans += str(temp[i])+"p^"+str(i)+"  "
	print ans



if __name__ == "__main__":
	main()