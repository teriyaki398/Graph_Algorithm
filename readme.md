# グラフ関連のpythonコード
###### arbitrary_graph
任意のグラフについてできるだけ効率的に総当りする

###### complete, bipartite
完全グラフと完全二部グラフについて、自前実装の漸化式と多項式計算で解く

###### polynomial
numpyを使った多項式計算

###### series-parallel_graph
直並列グラフについて、線形時間で漏えい確率を求める
CSS2017

###### DrawGraph
pygraphvizを用いてグラフを描画する


## GitHubにデータをプッシュするまでの流れw
- ファイルをローカルリポジトリに登録する
```bash
$ git add FILE
$ git commit -a -m "COMMENT"
```

- GitHubにプッシュする
```bash
$ git remote add origin https://github.com/teriyaki398/Graph_Algorithm.git
$ git push origin master
```

- その他のコマンド
``` bash
$ git rm --cached	//addしたファイルを取り消す
$ git commit --amend 	//直前のコミットを取り消す
$ git commit -v 	//変更点を表示してコミット
$ git branch -a		//リモートとローカルのブランチ一覧 -rでリモートのみ
$ git diff		//差分を確認する
$ git log		//ログの表示 git reflog で色々見れる
```
