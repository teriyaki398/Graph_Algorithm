# -*- coding: utf-8 -*-

import time
from Queue import Queue
import itertools
import copy
"""
グラフを無向グラフとして扱った時の漏洩確率を計算する
つまり[1,4]という辺がある時、[4,1]も入れる
"""

p = 0.5
n = input("n : ")
#次数nの完全グラフを作る
G = []
G.append([])
for i in range(1,n+1):
	temp = range(1,n+1)
	temp.remove(i)
	G.append(temp)


#辺のリストを作る
edge_list = []
for i in range(len(G)):
	for j in range(len(G[i])):
		if([G[i][j],i] not in edge_list):
			edge_list.append([i,G[i][j]])

tnum = len(G) - 1


#道判定関数
def judge_path(G):	#グラフを引数にする
	que = Queue()
	que.put(1)	#スタートはsから
	reachnode = set() #到達したノードをメモしておく
	while(True):
		if(que.empty()): break

		temp = que.get()

		for node in G[temp]:
			if(node == tnum):
				return True
			if(node not in reachnode):
				que.put(node)
				reachnode.add(node)
	return False



def main():
	ans = 0
	# print G

	for comb in range(1,len(edge_list)+1):
		cnt = 0
		for element in itertools.combinations(edge_list, comb):
			"""
			指定した数の組み合わせを取得する
			コピーしたグラフからその辺を取り除き、道を判定する
			"""
			#if(([1,2*n] in element) == False): continue		#s-tの辺がカットされていない場合はcontinue

			tG = copy.deepcopy(G)
			for i in range(comb):
				tG[element[i][0]].remove(element[i][1])
				tG[element[i][1]].remove(element[i][0])
			if(judge_path(tG) == False):
				cnt += 1
				# print element
		# print "(comb,cnt)=",comb,cnt

		anstemp= cnt*p**(comb)*(1-p)**(len(edge_list)-comb)
		# print anstemp
		ans += anstemp
	print ans
	return


if __name__ == "__main__":
	start = time.time()
	main()
	print time.time() - start





