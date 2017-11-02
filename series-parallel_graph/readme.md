# 直並列グラフにおける漏えい確率の計算
線形時間で求める
CSS2017の内容

calc_polynomial.py
多項式に値を代入する？

create_function.py
直並列グラフを生成する関数を定義している
クラスではなく関数

drawGraph_function.py
グラフを描画する関数を定義している
クラスではなく関数

enhanced_polychain_reduction.py
ランダムな直並列グラフを生成し、信頼度を計算
そこから漏えい確率を求める
Polygon-to-Chain reductionを実装しており、最後まで計算できる

polychain_polynomial.py
単純な縮退手法のみで計算を行うやつ

reduce_function.py
直列縮退、並列縮退、polychain縮退、次数１縮退を行う関数を定義


