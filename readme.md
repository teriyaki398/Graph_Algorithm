# グラフ関連のpythonコード

## GitHubにデータをプッシュするまでの流れw
- ファイルをローカルリポジトリに登録する
"""bash
$ git add FILE
$ git commit -a -m "COMMENT"
"""

- GitHubにプッシュする
"""bash
$ git remote add origin https://github.com/teriyaki398/Graph_Algorithm.git
$ git push origin master
"""

- その他のコマンド
""" bash
$ git rm --cached	//addしたファイルを取り消す
$ git commit --amend 	//直前のコミットを取り消す
$ git commit -v 	//変更点を表示してコミット
$ git branch -a		//リモートとローカルのブランチ一覧 -rでリモートのみ
$ git diff		//差分を確認する
$ git log		//ログの表示 git reflog で色々見れる
"""
