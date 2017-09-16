# coding:utf-8

"""
出力した多項式に愚直に代入して計算する
"- 2p^2 + 4p^3 + 13p^4 - 38p^5 - 8p^6"
こんな感じの多項式を想定
"""

def retVal(poly):
	poly = poly.split(" ")
	ans = 0
	p = 0.5
	print poly
	if poly[0] != '-' and 'p' not in poly[0]:
		ans = int(poly[0])
		poly = poly[1:]

	flag = True # True　の時は足し算で、Falseなら引き算にする
	for i in poly:
		if i == '-':
			flag = False
			continue
		elif i == '+':
			flag = True
		else:
			# i = Cp^x のような形になっている
			c,x = map(int,i.split("p^"))
			if flag == True:
				ans += c * p ** x
			else:
				ans -= c * p ** x
	return ans


