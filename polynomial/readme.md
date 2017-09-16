# numpyで多項式計算

- 一次元多項式を生成
係数のリストから多項式オブジェクトを生成
次数の大きい順になる

```bash:python
>>> f1 = np.poly1d([1])
>>> f2 = np.poly1d([1,2,3])
>>> print f1

1
>>> print f2
   2
1 x + 2 x + 3
```

- 多項式の四則演算
基本的にはpythonの演算子をそのまま使える
割り算は商と余りの配列になるので注意

```bash:python
>>> print f1 + f2
   2
1 x + 2 x + 4
>>> print f1 - f2
    2
-1 x - 2 x - 2
>>> print f1 * f2
   2
1 x + 2 x + 3
>>> print f1/f2
(poly1d([ 0.]), poly1d([ 1.]))
```

