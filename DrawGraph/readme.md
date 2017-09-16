# pygraphvizでグラフ描画
Graphvizというグラフ描画ツールを使って描画してみる
レイアウトは以下が参考になる
[Graphvizレイアウトサンプル](http://melborne.github.io/2013/04/02/graphviz-layouts/)

```python
def drawGraph(G, Elis, s, t)
# グラフ, 辺リスト, Sourceノード, Sinkノードを引数にとる
# グラフを生成し, ローカルに"graph番号.png"で保存する
# 辺のラベルは漏えい確率を表す
```

def drawGraph_polynomial(G, Elis, s, t)
# drawGraph()とほぼ同じ
# 漏えい確率の多項式を辺のラベルにする
```

