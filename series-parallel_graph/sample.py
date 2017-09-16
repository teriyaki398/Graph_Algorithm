# coding:utf-8

"""
ランダムな単純直並列グラフを生成し、
信頼度を計算、漏えい確率を算出する
多項式でやってみる
分母と分子を分けて保存する
edge : sorce sink weight(分母) weight(分子)
"""

import random
import numpy as np
import pygraphviz as pgv
from PIL import Image
from numpy.polynomial.polynomial import polyval
from numpy.polynomial.polynomial import polypow

# local function
import reduce_function as rf
import drawGraph_function as df
import calc_polynomial as calc

piccnt = 0

# reliability probability
def main():
	Factor = []

	# 任意のグラフにして見る
	G = [[1,2],[0,2,3],[0,1,3],[1,2]]
	Elis = []
	for i in range(len(G)):
		for j in range(len(G[i])):
			if([G[i][j],i] not in Elis):
				Elis.append([i,G[i][j]])
	for i in range(len(Elis)):
		Elis[i].append(np.poly1d([1,0]))
		Elis[i].append(np.poly1d([1]))
	s = 0
	t = 3
	drawGraph_polynomial(G, Elis, s, t)

	while True:
		drawGraph_polynomial(G, Elis, s, t)
		flag = False
		G, Elis, flag = rem_deg1(G, Elis, s, t)
		if flag == True: continue
		G, Elis, flag = rem_loop(G, Elis, s, t)
		if flag == True: continue
		G, Elis, flag = parallel_reduction_polynomial(G, Elis, s, t)
		if flag == True: continue
		G, Elis, flag = series_reduction_polynomial(G, Elis, s, t)
		if flag == True: continue
		G, Elis, flag, Omega = polychain_reduction_polynomial(G, Elis, s, t)
		if flag == True:
			Factor.append(["Omega",Omega])
			continue
		break

	# この時点で、Elisにはs-t間の辺が一つのみの状態になってるはず
	# Factor にはOmegaのリストが入ってる
	# PI Omega * Elis[0] をしたあと、 p -> 1 - p にして 1 - R(1-p)を求める

	print "Factor ->", Factor
	nume = Elis[0][2]
	deno = Elis[0][3]
	On, Od = calc_Omega(Factor)
	nume = On * nume
	deno = Od * deno
	# この時点で nune/deno が信頼度になっている
	print "rel",[nume,deno]
	print "pst",Elis[0][2:]
	print "Reliability -> \n"
	print retPoly(nume)
	print "_" *min(max(len(retPoly(nume)),len(retPoly(deno))),190)
	print retPoly(deno) + "\n"

	# 先に1引いてから、1-pに変換する
	nume = deno - nume
	# f(p) -> f(1-p)
	nume = retLeakCoef(nume)
	deno = retLeakCoef(deno)
	print "Leak Probability -> \n"
	print retPoly(nume)
	print "_" *min(max(len(retPoly(nume)),len(retPoly(deno))),190)
	print retPoly(deno) + "\n"


	# 漏えい確率を計算する
	# s_nume = retPoly(retLeakCoef(deno) - retLeakCoef(nume))
	# s_deno = retPoly(retLeakCoef(deno))
	# print "Leak Probability -> \n"
	# print s_nume
	# print "_" * min(max(len(s_nume), len(s_deno)),190)
	# print s_deno + "\n"
	
	return



def calc_Omega(factor):
	nume = np.poly1d([1])
	deno = np.poly1d([1])
	for i in factor:
		nume *= i[1][0]
		deno *= i[1][1]
	return [nume,deno]

def g_sort(G):
	return [sorted(i) for i in G]

def e_sort(Elis):
	return sorted([sorted([i[0],i[1]]) + [i[2],i[3]] for i in Elis])

def parallel_polynomial_operation(G, Elis):
	# 辺を並列にする操作
	cEdge = random.choice(Elis)
	Elis.append(cEdge)
	G[cEdge[0]].append(cEdge[1])
	G[cEdge[1]].append(cEdge[0])
	# ソートして返す
	return [g_sort(G), e_sort(Elis)]

def series_polynomial_operation(G, Elis):
	# 点を挿入する操作
	# 辺リストからランダムに選ぶ
	cEdge = random.choice(Elis)
	# 選ばれた辺がループなら選び直す
	while cEdge[0] == cEdge[1]:
		cEdge = random.choice(Elis)
	G.append([])
	nV = len(G)-1

	# 選んだ辺をグラフから除く
	Elis.remove(cEdge)
	# グラフから接続する点の情報を除く
	G[cEdge[0]].remove(cEdge[1])
	G[cEdge[1]].remove(cEdge[0])

	# 新しい辺と点を追加する
	G[cEdge[0]].append(nV)
	G[cEdge[1]].append(nV)
	G[nV].append(cEdge[0])
	G[nV].append(cEdge[1])
	Elis.append([cEdge[0],nV,np.poly1d([1,0]),np.poly1d([1])])
	Elis.append([cEdge[1],nV,np.poly1d([1,0]),np.poly1d([1])])

	# ソートして返す
	return [g_sort(G), e_sort(Elis)]


# 並列縮退　多項式版
# G:無向グラフ, Elis:辺のリスト, s,t:2端子nodeの番号
# return グラフ,辺リスト,端子nodeの番号,縮退したかどうかのflag
def parallel_reduction_polynomial(G, Elis, s, t):
	# 辺の数を数えて、2以上のものが存在するなら、1本にする
	flag = False

	for e in Elis:
		# 平行な辺が存在するなら、indexを記録しておく
		cnt = 0
		index = -1
		for i in range(len(Elis)):
			if sorted([e[0],e[1]]) == sorted([Elis[i][0], Elis[i][1]]):
				cnt += 1
				if cnt == 2:
					index = i
					break

		# indexにどこかの場所が格納されているなら、それとeを並列縮退する
		if index != -1:
			flag = True
			rem_edge = Elis[index]

			# 分母を考慮して (x - y)/x のように計算する
			nume1 = e[2]
			deno1 = e[3]
			nume2 = rem_edge[2]
			deno2 = rem_edge[3]

			# まず (1 - nume1/deno1)*(1 - nume2/deno2)を計算する
			nume = (deno1 - nume1) * (deno2 - nume2)
			deno = deno1 * deno2
			nume = deno - nume

			Elis[Elis.index(e)][2] = nume
			Elis[Elis.index(e)][3] = deno
			Elis.remove(rem_edge)
			G[e[0]].remove(e[1])
			G[e[1]].remove(e[0])
			# これを入れないとエラーになるよ
			return [g_sort(G), e_sort(Elis),flag]

	# ソートして返す
	return [g_sort(G), e_sort(Elis),flag]

# 直列縮退 多項式版
# G:無向グラフ, Elis:存在する辺のリスト, s,t; 端子nodeの番号
# return グラフ,辺リスト,縮退したかどうかのflag
def series_reduction_polynomial(G, Elis, s, t):
	flag = False
	for w in range(len(G)):
		if w == s or w == t: continue
		if len(G[w]) == 2:
			flag = True
			# 隣接する2点をu,v とする
			u,v = [G[w][0], G[w][1]]

			# e_uw, e_wv を探す
			e_uw = []
			e_wv = []
			for v1,v2,pol,pol2 in Elis:
				if [v1, v2] == [u,w] or [v1, v2] == [w, u]:
					e_uw = [v1, v2, pol, pol2]
					Elis.remove([v1,v2,pol,pol2])
					break
			for v1,v2,pol,pol2 in Elis:
				if [v1, v2] == [w, v] or [v1, v2] == [v, w]:
					e_wv = [v1, v2, pol, pol2]
					Elis.remove([v1,v2,pol,pol2])
					break

			# 2辺を取り除き、uvを短絡する
			G[u].remove(w)
			G[v].remove(w)
			G[w].remove(u)
			G[w].remove(v)

			# 信頼度を計算し辺を張る
			var = np.polymul(e_uw[2],e_wv[2])
			var2 = np.polymul(e_uw[3],e_wv[3])
			Elis.append(sorted([u,v]) + [var,var2])
			G[u].append(v)
			G[v].append(u)

	# ソートして返す
	return [g_sort(G), e_sort(Elis), flag]

# ループを除く
def rem_loop(G, Elis, s, t):
	flag = False
	for e in Elis:
		if e[0] == e[1]:
			Elis.remove(e)
			G[e[0]].remove(e[0])
			G[e[0]].remove(e[0])
	return [G, Elis, flag]


# 次数1の点を除く
def rem_deg1(G, Elis, s, t):
	# s,tは除かない
	flag = False
	for vnum in range(len(G)):
		if vnum == s or vnum == t:
			continue
		if len(G[vnum]) == 1:
			flag = True
			u = G[vnum][0]
			G[u].remove(vnum)
			G[vnum].remove(u)

			# Elisから[u,vnum]の辺を探す
			for edge in Elis:
				if sorted([edge[0], edge[1]]) == sorted([u, vnum]):
					Elis.remove(edge)
					break

			Elis = e_sort(Elis)
			G = g_sort(G)

	return [G, Elis, flag]


# 本命のPolygon-to-Chain reductionを行う
# OMGをFactorに格納する
def polychain_reduction_polynomial(G, Elis, s, t):
	flag = False
	# 実行可能かについては次数をみればok
	if len(G[s]) == 2:
		flag = True
		u = G[s][0]
		v = G[s][1]
		# u-v間の辺を除去して、su,svを更新する
		# 各辺を探す
		e_us = []
		e_sv = []
		e_uv = []
		for e in Elis:
			if sorted([u,s]) == sorted([e[0],e[1]]):
				e_us = e
			if sorted([s,v]) == sorted([e[0],e[1]]):
				e_sv = e
			if sorted([u,v]) == sorted([e[0],e[1]]):
				e_uv = e
			if e_us != [] and e_sv != [] and e_uv != []: break
		if e_us == [] or e_sv == [] or e_uv == []:
			print "Error"
			sys.exit()

		pa, da = [e_us[2], e_us[3]]
		pb, db = [e_sv[2], e_sv[3]]
		pc, dc = [e_uv[2], e_uv[3]]

		palp = (da - pa) * pb * (dc - pc)
		dalp = da * db * dc

		pbet = pa * (db - pb) * (dc - pc)
		dbet = da * db * dc

		pdlt = pa*pb*pc + (da - pa)*pb*pc + pa*(db - pb)*pc + pa*pb*(dc - pc)
		ddlt = da * db * dc

		Elis[Elis.index(e_us)][2] = pdlt
		Elis[Elis.index(e_us)][3] = palp + pdlt
		Elis[Elis.index(e_sv)][2] = pdlt
		Elis[Elis.index(e_sv)][3] = pbet + pdlt
		Omega = [(palp*ddlt + pdlt*dalp)*(pbet*ddlt + pdlt*dbet), pdlt*dalp*dbet*ddlt]

		# 除去処理
		Elis.remove(e_uv)
		G[u].remove(v)
		G[v].remove(u)

		return [g_sort(G), e_sort(Elis), flag, Omega]

	# もしかしたらtについては縮退しなくても良いかも
	return [g_sort(G), e_sort(Elis), flag, 1]

	Elis = sorted([sorted([i[0],i[1]])+[i[2]] for i in Elis])
	G = [sorted(i) for i in G]
	return [G, Elis, flag, 1]	


def drawGraph_polynomial(G, Elis, s, t):
	global piccnt
	print "Graph", G
	print "Elis", Elis
	print "s,t", s, t
	print "----------------------------"
	Graph = pgv.AGraph(strict = False)

	for i in Elis:
		nume = retLeakCoef(i[2])
		deno = retLeakCoef(i[3])
		nume = deno - nume

		label = ""
		if deno == np.poly1d([1]):
			label = retPoly(nume)
		else:
			label = retPoly(nume) + "\n"
			label += "_" * max(len(retPoly(nume)), len(retPoly(deno))) + "\n"
			label += retPoly(deno)

		Graph.add_edge(str(i[0]), str(i[1]), label = label)

	# グラフレイアウト
	Graph.node_attr['shape'] = 'circle'
	Graph.node_attr['style'] = 'filled'
	Graph.node_attr['label'] = ' '

	# sとtを指定する
	n = Graph.get_node(s)
	n.attr['fillcolor'] = '#F781D8'
	n.attr['label'] = 's'
	n = Graph.get_node(t)
	n.attr['fillcolor'] = '#81BEF7'
	n.attr['label'] = 't'

	Graph.layout()
	# ローカルに保存しておく
	# Graph.draw("graph%04s.png" % piccnt, prog = "neato")
	# piccnt += 1
	Graph.draw("graph.png", prog="neato")

	im = Image.open("./graph.png")
	im.show()
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
			ans += "p^%d" % i

	if ans[1] == "+":
		return ans[2:]
	else:
		return ans


# 信頼度のやつを漏えい確率に変換する
# f(p) -> f(1-p)にする
def retLeakCoef(poly):
	coef = poly.c[::-1]
	eps = np.poly1d([0])
	for i in range(len(coef)):
		eps += coef[i] * np.poly1d(polypow(np.poly1d([-1,1]), i))
	return eps



if __name__ == "__main__":
	main()