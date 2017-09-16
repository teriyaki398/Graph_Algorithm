# -*- coding: utf-8 -*-


"""
漏洩確率が一様で、グラフの形は任意とする。
その時にstーフロープロトコルを用いた際の漏洩確率を計算する
多項式ではなく値を用いている
"""

import time
import itertools
import copy


p = 0.5
n = input("n : ")

#Gにグラフを入れる
#以下は次数nの完全グラフを入れている
G = []
G.append([])
for i in range(1,n+1):
	temp = range(1,n+1)
	temp.remove(i)
	G.append(temp)

#辺のリストを作る
edge = []
for i in range(len(G)):
	for j in range(len(G[i])):
		if([G[i][j],i] not in edge):
			edge.append([i,G[i][j]])



SIZE = len(edge) + 1
tnum = len(G) - 1	#tの値


#poly(始点集合、現在のグラフ)
def poly(S,tG):

	#eps 漏洩確率
	eps = 0

	#始点集合から繋がる変の本数を数える
	edgecnt = 0
	for i in S:
		for j in tG[i]:
			if(j not in S): edgecnt += 1
	eps += p**edgecnt

	#Sから接続可能な点のリストを作る
	ellist = []
	for i in S:
		for j in tG[i]:
			if (j not in S) and (j not in ellist):
				ellist.append(j)
	if (tnum in ellist): ellist.remove(tnum)

	for el in range(1,len(ellist)+1):	#elの個数を1~ellist.sizeまでループ
		for element in itertools.combinations(ellist, el):	#接続する点の組み合わせループ

			#Xを求める
			#p^leakEdgeCntを求める
			leakEdgeCnt = 0
			for i in S:
				for j in tG[i]:
					if((j not in S) and (j not in element)):
						leakEdgeCnt += 1
			X = p**leakEdgeCnt

			#Yを求める
			Y = 1
			for i in element:
				temp = 0
				#element内のiに接続する辺の本数を記録
				conEdgeCnt = 0
				for j in S:
					if(i in tG[j]):
						conEdgeCnt += 1
				temp = 1 - p**conEdgeCnt

				Y *= temp

			XY = X*Y

			#Wにこのl点の選び方における多項式を記録
			#nGに次に見るグラフを入れる
			nG = [i[:] for i in tG]
			for i in S:
				nG[i] = []
			for i in range(len(nG)):
				for j in S:
					if(j in nG[i]):
						nG[i].remove(j)
			W = XY * poly(element,nG)

			eps += W

	return eps


def main():
	tG = [i[:] for i in G]
	start = time.time()
	print poly([1],tG)
	print time.time() - start
	return

if __name__ == "__main__":
	main()