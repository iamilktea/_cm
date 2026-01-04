# 習題 2 : 解二次多項式的根 (Solving Quadratic Roots)

本專案旨在透過 Python 實作一元二次方程式的公式解，並能夠正確處理**實數根**與**複數根**的情況。

## 📖 題目說明

給定一個二次多項式：

$$f(x) = ax^2 + bx + c$$

我們需要編寫一個函數 `root2(a, b, c)` 來求出使 $f(x) = 0$ 的 $x$ 解。

### 數學公式
根據公式解（Quadratic Formula）：

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

* 當 $b^2 - 4ac \geq 0$ 時，有實數解。
* 當 $b^2 - 4ac < 0$ 時，有共軛複數解。

## 🛠️ 實作重點

為了符合題目對於**複數根**以及**精確驗證**的要求，本程式使用了 Python 的 `cmath` (Complex Math) 模組。

### 1. 處理複數 (`cmath.sqrt`)
標準的 `math.sqrt` 在遇到負數時會報錯。我們使用 `cmath.sqrt`，它會自動將負數開根號轉換為虛數單位 `j`。

```python
import cmath
# 即使 b^2 - 4ac 為負，這行程式也能正常運作並回傳複數
sqrt_val = cmath.sqrt(b**2 - 4*a*c)
