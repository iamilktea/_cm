# 運算數學與程式設計 (Computational Mathematics) - 課程作業集

本專案匯集了「運算數學」課程的所有平時作業、期中作業與期末總結。內容涵蓋微積分、代數結構、線性代數、訊號處理、機率統計等數學領域的 Python 實作。

## 📝 關於本專案 (About)

* **作者**：[陳建瑋]
* **課程**：運算數學

## 📚 作業目錄 (Table of Contents)

|週次/習題| 主題 (Topic) | 程式碼 (Code) | 說明文件 (Docs) | 完成方法 |
|:---:|:---|:---:|:---:|:---|
| HW1 | **微積分基本定理** (Calculus) | [Code](./calculusTheorem1.py) | [Read](./README_HW1.md) | AI 協助 + 原創測試 |
| HW2 | **二次多項式的根** (Quadratic Roots) | [Code](./root2.py) | [Read](./README_HW2.md) | AI 協助 (`cmath`應用) |
| HW3 | **三次多項式的根** (Cubic Roots) | [Code](./root3.py) | [Read](./README_HW3.md) | 參考公式 + AI 實作 |
| HW4 | **N 次多項式 (牛頓法)** (Newton's Method) | [Code](./rootN.py) | [Read](./README_HW4.md) | AI 協助演算法邏輯 |
| HW6 | **有限體與群** (Finite Fields) | [Code](./finite_field.py) | [Read](./README_HW6.md) | AI 協助物件導向架構 |
| Midterm| **曼德博集合** (Mandelbrot Set) | [Code](./fractal.py) | [Read](./README_Midterm.md) | AI 生成繪圖核心 + 自行調整 |
| HW9 | **幾何系統建構** (Geometry System) | [Code](./geometry.py) | [Read](./README_HW9.md) | AI 協助向量運算 |
| HW10| **機率統計檢定** (Hypothesis Testing) | [Code](./statistics_test.py) | [Read](./README_HW10.md) | AI 解說原理 + 自行實作 |
| HW11| **資訊理論與漢明碼** (Info Theory) | [Code](./info_theory.py) | [Read](./README_HW11.md) | AI 協助編碼邏輯 |
| HW12| **線性代數演算法** (Linear Algebra) | [Code](./linear_algebra.py) | [Read](./README_HW12.md) | AI 協助矩陣分解實作 |
| HW13| **常微分方程求解** (ODE Solver) | [Code](./ode1.py) | [Read](./README_HW13.md) | AI 協助字串處理與誤差修正 |
| HW14| **傅立葉轉換** (DFT/IDFT) | [Code](./fourier.py) | [Read](./README_HW14.md) | 參考公式 + 原創實作 |

---

## 🛠️ 作業詳細說明 (Detailed Descriptions)

### [HW1] 微積分基本定理驗證
* **目標**：使用數值積分 (黎曼和) 與數值微分 (差分商) 驗證 $\frac{d}{dx}\int_a^x f(t)dt = f(x)$。
* **重點**：處理浮點數誤差，使用 `assert abs(diff) < epsilon` 進行驗證。

### [HW2] 二次多項式的根
* **目標**：實作 $ax^2+bx+c=0$ 的公式解。
* **重點**：使用 Python 的 `cmath` 模組處理判別式小於 0 (複數根) 的情況。

### [HW3] 三次多項式的根 (加分題)
* **目標**：實作卡爾丹諾公式 (Cardano's formula) 求解三次方程式。
* **重點**：處理複數開立方根的主值問題，確保能找出所有三個根。

### [HW4] N 次多項式的根 (牛頓法)
* **目標**：針對 $n \ge 5$ 無公式解的情況，實作數值解法。
* **重點**：結合 **牛頓法 (Newton-Raphson)** 尋找單根，以及 **綜合除法 (Synthetic Division)** 進行降次 (Deflation)，找出所有複數根。

### [HW6] 有限體 (Finite Field)
* **目標**：實作 $GF(p)$ 類別並驗證群公理 (Group Axioms)。
* **重點**：實作運算子重載 (`+`, `-`, `*`, `/`)，並利用費馬小定理計算乘法反元素 (除法)。

### [Midterm] 期中作業：曼德博集合
* **目標**：數學視覺化程式。
* **重點**：利用複數迭代 $z_{n+1} = z_n^2 + c$ 繪製碎形圖形，使用 `matplotlib` 與 `numpy` 加速運算。

### [HW9] 幾何物件導向系統
* **目標**：定義點、線、圓、三角形類別。
* **重點**：實作幾何演算法，包括「兩線交點」、「線圓交點」、「點到直線垂足」及「畢氏定理驗證」。

### [HW10] 機率統計：檢定原理
* **目標**：不使用套件，手刻 Z-test 與 T-test (單樣本、獨立、配對) 的計算公式。
* **重點**：理解中央極限定理與 t 分佈的差異，並透過程式驗證公式正確性。

### [HW11] 資訊理論
* **目標**：處理機率下溢問題，計算熵 (Entropy)、KL 散度。
* **重點**：實作 (7,4) 漢明碼 (Hamming Code) 的編碼與錯誤更正 (Syndrome Decoding)。

### [HW12] 線性代數觀念與實作
* **目標**：回答線性代數核心觀念，並實作數值演算法。
* **重點**：手刻遞迴行列式、LU 分解、使用特徵值分解 (Eigendecomposition) 實作 SVD，以及 PCA 主成份分析。

### [HW13] 常微分方程 (ODE) 求解器
* **目標**：輸入常係數陣列，輸出 ODE 的通解字串。
* **重點**：使用 `numpy.roots` 求特徵根，並處理「浮點數誤差」以正確判斷「重根」與「共軛複數根」，輸出正確的 $x$ 修正項與三角函數項。

### [HW14] 傅立葉轉換 (DFT)
* **目標**：不使用 `numpy.fft`，根據定義實作離散傅立葉轉換。
* **重點**：實作 $O(N^2)$ 的 DFT 與 IDFT 雙重迴圈，驗證訊號經轉換後可無損還原。

---

## 🏁 期末總結

透過本學期的課程，我從基礎的微積分數值驗證開始，一路深入到代數結構、線性代數的底層演算法，最後結合訊號處理與微分方程。這不僅讓我學會了如何「寫程式算數學」，更重要的是理解了現成套件 (如 NumPy, SciPy) 背後的數學原理與實作細節。

---
*Last Updated: 2025/01*
