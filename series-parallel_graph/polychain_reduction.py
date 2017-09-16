# coding:utf-8

"""
ランダムな単純直並列グラフを生成し、
信頼度を計算、漏えい確率を算出する
"""

import random

# local function
import reduce_function as rf
import create_function as cf
import drawGraph_function as df

# reliability probability
p = 0.5
OpeCount = input("Operation times : ")

def main():
	G = [[1],[0]]
	Elis = [[0,1,p]]
	Factor = []

	for _ in range(OpeCount):
		switch = random.randint(0,1)
		if switch == 0:
			G, Elis = cf.parallel_operation(G, Elis)
		else:
			G, Elis = cf.series_operation(G, Elis, p)

	# 生成したグラフを単純グラフに直す
	s = -1
	t = -1
	while True:
		G, Elis, flag = rf.parallel_reduction(G, Elis, s, t)
		if flag == True: continue
		G, Elis, flag = rf.rem_deg1(G, Elis, s, t)
		if flag == True: continue
		G, Elis, flag = rf.rem_loop(G, Elis, s, t)
		if flag == True: continue
		break
	for i in range(len(Elis)):
		Elis[i][2] = p

	# プレイヤーの集合を計算
	player_lis = set([])
	for element in G:
		player_lis = player_lis | set(element)
	
	s = random.choice(list(player_lis))
	t = random.choice(list(player_lis))
	while s == t:
		t = random.choice(list(player_lis))

	print "G",G
	print "Elis",Elis
	df.drawGraph(G, Elis, s, t)

	while True:
		# flagを初期化しておく
		flag1,flag2,flag3,flag4,flag5 = [False]*5
		df.drawGraph(G, Elis, s, t)
		G, Elis, flag1 = rf.rem_deg1(G, Elis, s, t)
		if flag1 == True: continue
		G, Elis, flag2 = rf.rem_loop(G, Elis, s, t)
		if flag2 == True: continue
		G, Elis, flag3 = rf.series_reduction(G, Elis, s, t)
		if flag3 == True: continue
		G, Elis, flag4 = rf.parallel_reduction(G, Elis, s, t)
		if flag4 == True: continue

		G, Elis, flag5, Omega = rf.polychain_reduction(G, Elis, s, t)
		if flag5 == True: 
			Factor.append(['Omega', Omega])
			continue
		break

	print "Factor", Factor
	if len(Elis) == 0:
		print "Leak Probability",Elis[0][2]
	else:
		print "Leak Probability",1-calc_Omega(Factor)*Elis[0][2]

	return

def calc_Omega(factor):
	x = 1
	for i in factor:
		x *= i[1]
	return x

if __name__ == "__main__":
	main()