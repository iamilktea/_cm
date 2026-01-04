"""
習題 3 (加分題) : 請寫程式求解三次多項式的根
目標：使用公式解求 ax^3 + bx^2 + cx + d = 0 的根，包含複數根。
"""

import cmath

def root3(a, b, c, d):
    """
    輸入係數 a, b, c, d，回傳三次多項式的三個根。
    使用通用的三次方程式公式 (General Cubic Formula)。
    """
    if a == 0:
        raise ValueError("這不是三次方程式 (a 不能為 0)")

    # 為了簡化公式，我們使用 Wolfram MathWorld 的標準形式參數
    # 定義 delta0 和 delta1
    delta0 = b**2 - 3*a*c
    delta1 = 2*b**3 - 9*a*b*c + 27*a**2*d

    # 計算 C 值
    # C = cube_root( (delta1 +/- sqrt(delta1^2 - 4*delta0^3)) / 2 )
    # 注意：這裡的平方根和立方根都可能產生複數
    inner_sqrt = cmath.sqrt(delta1**2 - 4*delta0**3)
    
    # 計算 C (C 有兩個可能值，我們選其中一個非零的即可，這裡選 + )
    # Python 的 **(1/3) 對於複數會回傳主值
    C = ((delta1 + inner_sqrt) / 2) ** (1/3)
    
    # 如果 C 為 0 (極端情況，例如三重根)，嘗試減號
    if cmath.isclose(C, 0):
        C = ((delta1 - inner_sqrt) / 2) ** (1/3)

    # 如果 C 還是 0，代表 delta0 也是 0，這是一個三重根的情況
    if cmath.isclose(C, 0):
        root = -b / (3*a)
        return root, root, root

    # 定義 1 的三次單位根 (primitive cube root of unity)
    # omega = (-1 + sqrt(3)i) / 2
    omega = complex(-0.5, cmath.sqrt(3).real / 2)
    
    # 根據公式計算三個根
    # x_k = -1/(3a) * (b + omega^k * C + delta0 / (omega^k * C))
    # k = 0, 1, 2
    
    x1 = -1/(3*a) * (b + C + delta0/C)
    x2 = -1/(3*a) * (b + omega*C + delta0/(omega*C))
    x3 = -1/(3*a) * (b + omega**2*C + delta0/(omega**2*C))

    return x1, x2, x3

def verify_root(a, b, c, d, x):
    """
    驗證根代入方程式後是否為 0
    """
    val = a * x**3 + b * x**2 + c * x + d
    # 檢查是否趨近於 0
    is_correct = cmath.isclose(val, 0, abs_tol=1e-8)
    return val, is_correct

if __name__ == "__main__":
    # 測試案例 1: 簡單整數根
    # (x-1)(x-2)(x-3) = x^3 - 6x^2 + 11x - 6 = 0
    print("--- 測試案例 1: 實數根 (1, -6, 11, -6) ---")
    print("預期答案: 1, 2, 3")
    a, b, c, d = 1, -6, 11, -6
    roots = root3(a, b, c, d)
    
    for i, r in enumerate(roots):
        val, correct = verify_root(a, b, c, d, r)
        print(f"根 {i+1}: {r:.4f}")
        print(f"  -> 代回 f(x) = {val:.2e}, 正確? {correct}")

    print("\n")

    # 測試案例 2: 包含複數根
    # x^3 - 1 = 0 (根為 1, 以及兩個複數根)
    print("--- 測試案例 2: x^3 - 1 = 0 (1, 0, 0, -1) ---")
    a, b, c, d = 1, 0, 0, -1
    roots = root3(a, b, c, d)
    
    for i, r in enumerate(roots):
        val, correct = verify_root(a, b, c, d, r)
        print(f"根 {i+1}: {r:.4f}")
        print(f"  -> 代回 f(x) = {val:.2e}, 正確? {correct}")
