# -*- coding: utf-8 -*-

"""
漏洩確率一様
完全二部グラフにおける漏洩確率を求める多項式を計算する
"""

import itertools
import math
import time

m,n = map(int, raw_input("m,n : ").split())


#Gに完全二部グラフを入れる
G = []
G.append([])
for i in range(m):
	temp = range(m+1,m+n+1)
	G.append(temp)
for i in range(n):
	temp = range(1,m+1)
	G.append(temp)

#辺のリストを作る
edge = []
for i in range(len(G)):
	for j in range(len(G[i])):
		if([G[i][j],i] not in edge):
			edge.append([i,G[i][j]])



SIZE = len(edge) + 1
tnum = len(G) - 1	#tの値

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


def polyA(i,j,k):

	temp = range(SIZE)
	for x in range(SIZE):
		temp[x] = 0
	temp[j*k] = 1

	for el in range(1,j):
		X = xCy(j-1,el)
		Y = nikou(k,el)
		XY = mulk(X,Y)

		Z = range(SIZE)
		for x in range(SIZE):
			Z[x] = 0
		Z[(j-el)*k] = 1
		XYZ = mul(XY,Z)

		W = mul(XYZ, polyB(j,i-k,el))
		temp = plus(temp,W)

	return temp

def polyB(i,j,k):
	temp = range(SIZE)
	for x in range(SIZE):
		temp[x] = 0
	temp[j*k] = 1

	for el in range(1,j+1):
		X = xCy(j,el)
		Y = nikou(k,el)
		XY = mulk(X,Y)

		Z = range(SIZE)
		for x in range(SIZE):
			Z[x] = 0
		Z[(j-el)*k] = 1
		XYZ = mul(XY,Z)

		W = mul(XYZ, polyA(j,i-k,el))
		temp = plus(temp ,W)

	return temp



def main():
	start = time.time()
	temp = polyA(m,n,1)
	ans = ""
	for i in range(SIZE):
		if(temp[i] != 0):
			ans += str(temp[i])+"p^"+str(i)+"  "
	print ans
	print time.time() - start



if __name__ == "__main__":
	main()

