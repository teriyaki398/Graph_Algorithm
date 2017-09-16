# coding:utf-8

import pygraphviz as pgv
from PIL import Image
import numpy as np

# グラフを描画する関数を定義
piccnt = 0

def drawGraph(G, Elis, s, t):
	global piccnt
	print "Graph", G
	print "Elis", Elis
	print "s,t", s, t
	print "----------------------------"
	Graph = pgv.AGraph(strict = False)

	for i in Elis:
		# 信頼度を漏えい確率に直して表示する
		Graph.add_edge(str(i[0]), str(i[1]), label = str(1-i[2]))

	# グラフレイアウト
	Graph.node_attr['shape'] = 'circle'
	Graph.node_attr['style'] = 'filled'

	# sとtを指定する
	n = Graph.get_node(s)
	n.attr['fillcolor'] = '#F781D8'
	n = Graph.get_node(t)
	n.attr['fillcolor'] = '#81BEF7'

	Graph.layout()
	# ローカルに保存しておく
	Graph.draw("graph%04s.png" % piccnt, prog = "neato")
	piccnt += 1
	Graph.draw("graph.png", prog="neato")

	im = Image.open("./graph.png")
	im.show()
	return

def drawGraph_polynomial(G, Elis, s, t):
	global piccnt
	print "Graph", G
	print "Elis", Elis
	print "s,t", s, t
	print "----------------------------"
	Graph = pgv.AGraph(strict = False)

	for i in Elis:
		# 信頼度を漏えい確率に直して表示する
		# if i[2] == np.poly1d([1]):
		# 	leakProb = retLeakCoef(i[2])
		# 	Graph.add_edge(str(i[0]), str(i[1]), label = retPoly(leakProb))
		# else:
		# 	Graph.add_edge(str(i[0]), str(i[1]), label = retPoly("a"))
		leakProb = retLeakCoef(i[2])
		Graph.add_edge(str(i[0]), str(i[1]), label = retPoly(leakProb))

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
	Graph.draw("graph%04s.png" % piccnt, prog = "neato")
	piccnt += 1
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


# 信頼度のやつを漏えい確率に変換して、係数リストを求める
def retLeakCoef(poly):
	coef = poly.c[::-1]
	eps = np.poly1d([0])
	for i in range(len(coef)):
		eps += coef[i] * np.poly1d(polypow(np.poly1d(-1,1), i))
	return eps










