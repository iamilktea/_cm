# 習題 1 : 用 Python 驗證微積分基本定理 (Fundamental Theorem of Calculus)

本專案是一個數值分析的練習程式，旨在透過 Python 程式碼，以數值方法驗證**微積分基本定理的第一部分 (FTC Part 1)**。

## 📖 題目說明

微積分基本定理的第一部分指出：如果我們定義一個積分函數 $G(x)$ 為：

$$G(x) = \int_0^x f(t) \, dt$$

那麼 $G(x)$ 的導數即為原函數 $f(x)$：

$$G'(x) = \frac{d}{dx} \left( \int_0^x f(t) \, dt \right) = f(x)$$

本程式的目標是實作積分與微分的數值算法，並驗證上述等式在容許誤差範圍內是否成立。

## 🛠️ 實作方法 (Implementation)

由於電腦無法直接處理連續的無限小概念，我們使用離散的數值方法來近似：

### 1. 數值積分 (`integral`)
使用 **黎曼和 (Riemann Sum)** 的概念，將區間 $[a, b]$ 切割成無數個寬度為 $h$ 的小矩形，並將面積加總。
* **公式**：$\text{Area} \approx \sum_{x=a}^{b} f(x) \cdot h$
* 在本程式中，$h$ 設定為 `0.0001`。

### 2. 數值微分 (`df`)
使用 **差分商 (Difference Quotient)** 的定義來近似導數。
* **公式**：$f'(x) \approx \frac{f(x+h) - f(x)}{h}$

### 3. 驗證邏輯 (`theorem1`)
由於浮點數運算 (Floating-point arithmetic) 存在微小誤差，我們不能直接使用 `==` 來比較結果。程式改為檢查兩者的差值絕對值是否小於一個極小值 (Epsilon, 例如 `0.01`)：
```python
assert abs(derivative_of_integral - original_function_value) < 0.01
