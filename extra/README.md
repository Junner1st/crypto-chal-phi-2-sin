# Phi2Sin (Φ to Signature)

## 檔案

- `field.py`：有限域輔助函式
- `curve.py`：橢圓曲線群與 public automorphism
- `relation.py`：constraint-friendly 的 map-to-curve relation
- `scheme.py`：基於 relation 的玩具簽章系統
- `service.py`：指令分派器

## 題目設計

這個 relation 不是真正的 hash-to-curve map。

在 $j = 0$ 曲線

$$
y^2 = x^3 - 17
$$

有映射

$$
\phi(x, y) = (\omega x, y)
$$

這是一個曲線自同態。因為純量乘法會和這個映射交換：

$$
\phi(sk \cdot P) = sk \cdot \phi(P)
$$

所以某個 relation point 上的簽章可被搬到另一個 relation point 上。

簽章 oracle 會拒絕直接簽 reserved account，但公開自同態讓我們可以找到另一個合法的 relation point，使它經過映射後落到 reserved account 的 relation point。

## 攻擊流程

1. 呼叫 `params` 取得 `p`、`b`、`window`、`item_limit`、`account_id` 和自同態係數 `a`。
2. 枚舉 reserved account 的候選 index `k2`，並設定 `x2 = account_id * window + k2`。
3. 檢查 `x2` 是否對應到合法曲線點，且 witness `z` 是否滿足 relation constraints。
4. 用反向自同態把點拉回去，計算 `x1 = a^-1 * x2`。
5. 將 `x1` 轉成 `(m1, k1)`，並確認 `m1` 不是 reserved account。
6. 請 oracle 對非 reserved 的 relation point `(x1, y)` 簽章。
7. 對回傳 token 套用自同態，得到 `(a*sx, sy)`。
8. 把搬運後的 token 送去驗證 reserved account 的點 `(x2, y)`，取得 flag。

[solver script is here](/extra/solve.py)

## FLAG

`CCCTF{Ya_wen2__faahhh___}`
