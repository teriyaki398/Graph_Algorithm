# coding:utf-8

"""
ランダムな単純直並列グラフを生成し、
単純な縮退のみで
信頼度を計算、漏えい確率を算出する
多項式でやってみる
"""

import random
import numpy as np

# local function
import reduce_function as rf
import create_function as cf
import drawGraph_function as df

# reliability probability
OpeCount = input("Operation times : ")

def main():
	G = [[1],[0]]
	# 信頼度 1-p をweightにする
	Elis = [[0,1,np.poly1d([1,0])]]
	Factor = []

	# ランダムなグラフを生成
	for _ in range(OpeCount):
		switch = random.randint(0,1)
		if switch == 0:
			G, Elis = cf.parallel_polynomial_operation(G, Elis)
		else:
			G, Elis = cf.series_polynomial_operation(G, Elis, np.poly1d([1,0]))

	# 単純グラフになるまで直す
	while True:
		flag = False
		G, Elis, flag = rf.parallel_reduction_polynomial(G, Elis, -1, -1)
		if flag == True: continue
		G, Elis, flag = rf.rem_deg1(G, Elis, -1, -1)
		if flag == True: continue
		G, Elis, flag = rf.rem_loop(G, Elis, -1, -1)
		if flag == True: continue
		break
	for i in range(len(Elis)):
		Elis[i][2] = np.poly1d([1,0])

	# プレイヤーの集合を計算
	# 重複がないようにs,tを選ぶ
	player_lis = set([])
	for element in G:
		player_lis = player_lis | set(element)
	
	s = random.choice(list(player_lis))
	t = random.choice(list(player_lis))
	while s == t:
		t = random.choice(list(player_lis))

	df.drawGraph_polynomial(G, Elis, s, t)
	switch = input("switch : ")
	if switch == 0:
		return

	counter = [0,0,0,0]	# rem_deg1, rem_loop, parallel_reductionm series_reduction
	while True:
		df.drawGraph_polynomial(G, Elis, s, t)
		flag = False
		G, Elis, flag = rf.rem_deg1(G, Elis, s, t)
		if flag == True:
			counter[0] += 1
			continue
		G, Elis, flag = rf.rem_loop(G, Elis, s, t)
		if flag == True:
			counter[1] += 1
			continue
		G, Elis, flag = rf.parallel_reduction_polynomial(G, Elis, s, t)
		if flag == True:
			counter[2] += 1
			continue
		G, Elis, flag = rf.series_reduction_polynomial(G, Elis, s, t)
		if flag == True:
			counter[3] += 1
			continue
		break

	print df.retPoly(df.retLeakCoef(Elis[0][2]))
	print "counter :",counter

	return

def calc_Omega(factor):
	x = 1
	for i in factor:
		x *= i[1]
	return x

if __name__ == "__main__":
	main()