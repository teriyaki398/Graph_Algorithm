# coding:utf-8

"""
直並列グラフを生成する関数を定義
"""
import sys
import random
import numpy as np


# 多項式用
# def e_sort(Elis):
# 	return sorted([sorted([i[0], i[1]]) + [i[2],i[3]] for i in Elis])
def e_sort(Elis):
	return sorted([sorted([i[0],i[1]]) + [i[2]] for i in Elis])
def g_sort(G):
	return [sorted(i) for i in G]

# 並列な辺を追加
def parallel_operation(G, Elis):
	# 辺を並列にする操作
	cEdge = random.choice(Elis)
	Elis.append(cEdge)
	G[cEdge[0]].append(cEdge[1])
	G[cEdge[1]].append(cEdge[0])
	# ソートして返す
	return [[sorted(i) for i in G], sorted([sorted([i[0],i[1]]) + [i[2]] for i in Elis])]

# 直列な辺を追加
def series_operation(G, Elis, p):
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
	Elis.append([cEdge[0],nV,p])
	Elis.append([cEdge[1],nV,p])

	# ソートして返す
	return [[sorted(i) for i in G], sorted([sorted([i[0],i[1]]) + [i[2]] for i in Elis])]

def parallel_polynomial_operation(G, Elis):
	# 辺を並列にする操作
	cEdge = random.choice(Elis)
	Elis.append(cEdge)
	G[cEdge[0]].append(cEdge[1])
	G[cEdge[1]].append(cEdge[0])
	# ソートして返す
	return [g_sort(G), e_sort(Elis)]

def series_polynomial_operation(G, Elis, p):
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











