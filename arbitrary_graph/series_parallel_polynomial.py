# -*- coding: utf-8 -*-


"""
直並列グラフの多項式を求める
グラフと、s,tの値を入れよう
"""


import itertools
import copy


#Gにグラフを入れる
G = [[], [2, 7], [1, 4, 7, 8, 12, 16, 17, 20, 24], [], [2, 6, 13, 14, 17, 22, 23, 24], [6, 13], [4, 5], [1, 2, 18], [2, 10], [], [8, 15], [], [2, 20, 21], [4, 5, 23], [4, 21], [10, 22], [2, 19], [2, 4], [7, 19], [16, 18], [2, 12], [12, 14], [4, 15], [4, 13], [2, 4]]
tnum = 19
snum = 22

#辺のリストを作る
edge = []
for i in range(len(G)):
	for j in range(len(G[i])):
		if([G[i][j],i] not in edge):
			edge.append([i,G[i][j]])

SIZE = len(edge) + 1

# 綺麗に多項式を表示
def retPoly(coef):
	# 次数で昇順にする
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
			ans += "p^%d" % i

	if ans[1] == "+":
		return ans[2:]
	else:
		return ans

#足し算
def plus(a,b):
	temp = range(SIZE)
	for i in range(SIZE):
		temp[i] = a[i] + b[i]
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


#poly(始点集合、現在のグラフ)
def poly(S,tG):

	#係数のリスト
	coef = range(SIZE)
	for i in range(SIZE):
		coef[i] = 0

	#始点集合から繋がる変の本数を数える
	edgecnt = 0
	for i in S:
		for j in tG[i]:
			if(j not in S): edgecnt += 1
	coef[edgecnt] = 1

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
			#p^leakEdgeCnt の多項式を生成
			X = range(SIZE)
			for i in range(SIZE):
				X[i] = 0
			##漏洩する辺の本数を数え、多項式を更新
			leakEdgeCnt = 0
			for i in S:
				for j in tG[i]:
					if((j not in S) and (j not in element)):
						leakEdgeCnt += 1
			X[leakEdgeCnt] = 1

			#Yを求める
			Y = range(SIZE)
			for i in range(SIZE):
				Y[i] = 0
			Y[0] = 1
			for i in element:
				temp = range(SIZE)
				for j in range(SIZE):
					temp[j] = 0
				#element内のiに接続する辺の本数を記録
				conEdgeCnt = 0
				for j in S:
					if(i in tG[j]):
						conEdgeCnt += 1
				temp[0] = 1
				temp[conEdgeCnt] = -1

				Y = mul(Y,temp)

			XY = mul(X,Y)

			#Wにこのl点の選び方における多項式を記録
			#nGに次に見るグラフを入れる
			nG = copy.deepcopy(tG)
			for i in S:
				nG[i] = []
			for i in range(len(nG)):
				for j in S:
					if(j in nG[i]):
						nG[i].remove(j)
			W = mul(XY, poly(element, nG))

			coef = plus(coef, W)

	return coef


def main():
	tG= copy.deepcopy(G)
	ans = poly([snum],tG)
	print retPoly(ans)
	return

if __name__ == "__main__":
	main()