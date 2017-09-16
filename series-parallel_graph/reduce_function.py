# coding:utf-8

"""
直列縮退、並列縮退、polychain縮退、次数1の縮退
を行う関数を定義
"""
import sys
import random
import numpy as np

# 直列縮退
# G:無向グラフ, Elis:存在する辺のリスト, s,t; 端子nodeの番号
# return グラフ,辺リスト,縮退したかどうかのflag
def series_reduction(G, Elis, s, t):
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
			for v1,v2,pol in Elis:
				if [v1, v2] == [u,w] or [v1, v2] == [w, u]:
					e_uw = [v1, v2, pol]
					Elis.remove([v1,v2,pol])
					break
			for v1,v2,pol in Elis:
				if [v1, v2] == [w, v] or [v1, v2] == [v, w]:
					e_wv = [v1, v2, pol]
					Elis.remove([v1,v2,pol])
					break

			# 2辺を取り除き、uvを短絡する
			G[u].remove(w)
			G[v].remove(w)
			G[w].remove(u)
			G[w].remove(v)

			# 信頼度を計算し辺を張る
			var = e_uw[2] * e_wv[2]
			Elis.append(sorted([u,v]) + [var])
			G[u].append(v)
			G[v].append(u)

	# ソートして返す
	return [[sorted(i) for i in G], [sorted([i[0],i[1]])+[i[2]] for i in Elis], flag]


# 並列縮退
# G:無向グラフ, Elis:辺のリスト, s,t:2端子nodeの番号
# return グラフ,辺リスト,端子nodeの番号,縮退したかどうかのflag
def parallel_reduction(G, Elis, s, t):
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
		if index == -1:
			continue

		# indexにどこかの場所が格納されているなら、それとeを並列縮退する
		if index != -1:
			flag = True
			rem_edge = Elis[index]
			var = 1 - (1 - e[2]) * (1 - rem_edge[2])
			Elis[Elis.index(e)][2] = var
			Elis.remove(rem_edge)
			G[e[0]].remove(e[1])
			G[e[1]].remove(e[0])
			return [[sorted(i) for i in G], sorted([sorted([i[0],i[1]])+[i[2]] for i in Elis]), flag]

	# ソートして返す
	return [[sorted(i) for i in G], sorted([sorted([i[0],i[1]])+[i[2]] for i in Elis]), flag]


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

			Elis = sorted([sorted([i[0],i[1]])+[i[2]] for i in Elis])
			G = [sorted(i) for i in G]

	return [G, Elis, flag]


# ループを除く
def rem_loop(G, Elis, s, t):
	flag = False
	for e in Elis:
		if e[0] == e[1]:
			Elis.remove(e)
			G[e[0]].remove(e[0])
			G[e[0]].remove(e[0])
	return [G, Elis, flag]


# 本命のPolygon-to-Chain reductionを行う
# OMGをFactorに格納する
def polychain_reduction(G, Elis, s, t):
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

		p_us = e_us[2]
		p_sv = e_sv[2]
		p_uv = e_uv[2]
		alp = (1 - p_us) * p_sv * (1 - p_uv)
		bet = p_us * (1 - p_sv) * (1 - p_uv)
		dlt = p_us * p_sv * p_uv * (1 + (1-p_us)/p_us + (1 - p_sv)/p_sv + (1-p_uv)/p_uv)

		# 新しい値とOMGを与える
		Elis[Elis.index(e_us)][2] = dlt / (alp + dlt)
		Elis[Elis.index(e_sv)][2] = dlt / (bet + dlt)
		Omega = (alp + dlt)*(bet + dlt)/dlt
		# Factor.append(['Omega',(alp + dlt)*(bet + dlt)/dlt])

		# 除去処理
		Elis.remove(e_uv)
		G[u].remove(v)
		G[v].remove(u)

		Elis = sorted([sorted([i[0],i[1]])+[i[2]] for i in Elis])
		G = [sorted(i) for i in G]

		return [G, Elis, flag, Omega]

	if len(G[t]) == 2:
		flag = True
		u = G[t][0]
		v = G[t][1]
		# u-v間の辺を除去して、tu,tvを更新する
		# 各辺を探す
		e_ut = []
		e_tv = []
		e_uv = []
		for e in Elis:
			if sorted([u,t]) == sorted([e[0],e[1]]):
				e_ut = e
			if sorted([t,v]) == sorted([e[0],e[1]]):
				e_tv = e
			if sorted([u,v]) == sorted([e[0],e[1]]):
				e_uv = e
			if e_ut != [] and e_tv != [] and e_uv != []: break
		if e_ut == [] or e_tv == [] or e_uv == []:
			print "Error"
			sys.exit()

		p_us = e_ut[2]
		p_sv = e_tv[2]
		p_uv = e_uv[2]
		alp = (1 - p_ut) * p_tv * (1 - p_uv)
		bet = p_ut * (1 - p_tv) * (1 - p_uv)
		dlt = p_ut * p_tv * p_uv * (1 + (1-p_ut)/p_ut + (1 - p_tv)/p_tv + (1-p_uv)/p_uv)

		# 新しい値とOMGを与える
		Elis[Elis.index(e_ut)][2] = dlt / (alp + dlt)
		Elis[Elis.index(e_tv)][2] = dlt / (bet + dlt)
		Omega = (alp + dlt)*(bet + dlt)/dlt
		# Factor.append(['Omega',(alp + dlt)*(bet + dlt)/dlt])

		# 除去処理
		Elis.remove(e_uv)
		G[u].remove(v)
		G[v].remove(u)

		Elis = sorted([sorted([i[0],i[1]])+[i[2]] for i in Elis])
		G = [sorted(i) for i in G]
		return [G, Elis, flag, Omega]

	Elis = sorted([sorted([i[0],i[1]])+[i[2]] for i in Elis])
	G = [sorted(i) for i in G]
	return [G, Elis, flag, 1]	


# 多項式用
# def e_sort(Elis):
# 	return sorted([sorted([i[0], i[1]]) + [i[2],i[3]] for i in Elis])
def e_sort(Elis):
	return sorted([sorted([i[0], i[1]]) + [i[2]] for i in Elis])
def g_sort(G):
	return [sorted(i) for i in G]


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
			for v1,v2,pol in Elis:
				if [v1, v2] == [u,w] or [v1, v2] == [w, u]:
					e_uw = [v1, v2, pol]
					Elis.remove([v1,v2,pol])
					break
			for v1,v2,pol in Elis:
				if [v1, v2] == [w, v] or [v1, v2] == [v, w]:
					e_wv = [v1, v2, pol]
					Elis.remove([v1,v2,pol])
					break

			# 2辺を取り除き、uvを短絡する
			G[u].remove(w)
			G[v].remove(w)
			G[w].remove(u)
			G[w].remove(v)

			# 信頼度を計算し辺を張る
			var = np.polymul(e_uw[2],e_wv[2])
			# var2 = np.polymul1(e_uw[3],e_wv[3])
			# Elis.append(sorted([u,v]) + [var,var2])
			Elis.append(sorted([u,v]) + [var])
			G[u].append(v)
			G[v].append(u)

	# ソートして返す
	return [g_sort(G), e_sort(Elis), flag]



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
			px = e[2]
			# pd1 = e[3]
			py = rem_edge[2]
			# pd2 = rem_edge[3]

			# Elis(Elis.index(e))[2] = pd1*py + pd2*px - px*py
			# Elis(Elis.index(e))[3] = pd1 * pd2
			Elis[Elis.index(e)][2] = 1 - (1 - px)*(1 - py)
			Elis.remove(rem_edge)
			G[e[0]].remove(e[1])
			G[e[1]].remove(e[0])
			# これを入れないとエラーになるよ
			return [g_sort(G), e_sort(Elis),flag]

	# ソートして返す
	return [g_sort(G), e_sort(Elis),flag]



# 本命のPolygon-to-Chain reductionを行う
# OMGをFactorに格納する
# ret G, Elis, flag, Omega[p,d]
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
