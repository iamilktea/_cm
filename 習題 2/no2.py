"""
習題 2 : 請寫程式求解二次多項式的根 #2
目標：使用公式解求 ax^2 + bx + c = 0 的根，包含複數根。
"""

import cmath

def root2(a, b, c):
    """
    輸入係數 a, b, c，回傳二次多項式的兩個根 (x1, x2)。
    使用 cmath.sqrt 處理判別式小於 0 的情況 (複數根)。
    """
    # 計算判別式 (discriminant) 的平方根
    # cmath.sqrt 可以處理負數，會自動產生複數結果 (例如 1j)
    sqrt_discriminant = cmath.sqrt(b**2 - 4*a*c)
    
    # 應用公式解
    x1 = (-b + sqrt_discriminant) / (2 * a)
    x2 = (-b - sqrt_discriminant) / (2 * a)
    
    return x1, x2

def verify_root(a, b, c, x):
    """
    驗證根代入方程式後是否為 0 (或極接近 0)
    """
    val = a * x**2 + b * x + c
    # 使用 cmath.isclose 來比較浮點數/複數是否趨近於 0
    # abs_tol 是絕對誤差容許值
    is_correct = cmath.isclose(val, 0, abs_tol=1e-9)
    return val, is_correct

if __name__ == "__main__":
    # 測試案例 1: 實數根 (x^2 - 3x + 2 = 0 => 根為 1, 2)
    print("--- 測試案例 1: 實數根 (1, -3, 2) ---")
    a, b, c = 1, -3, 2
    roots = root2(a, b, c)
    print(f"方程式: {a}x^2 + {b}x + {c} = 0")
    print(f"計算出的根: {roots[0]}, {roots[1]}")
    
    # 驗證
    for r in roots:
        val, correct = verify_root(a, b, c, r)
        print(f"代回驗證 f({r}) = {val:.2e}, 結果正確? {correct}")

    print("\n")

    # 測試案例 2: 複數根 (x^2 + 1 = 0 => 根為 i, -i)
    # 判別式 b^2 - 4ac = 0 - 4 = -4 < 0
    print("--- 測試案例 2: 複數根 (1, 0, 1) ---")
    a, b, c = 1, 0, 1
    roots = root2(a, b, c)
    print(f"方程式: {a}x^2 + {b}x + {c} = 0")
    print(f"計算出的根: {roots[0]}, {roots[1]}")
    
    # 驗證
    for r in roots:
        val, correct = verify_root(a, b, c, r)
        print(f"代回驗證 f({r}) = {val:.2e}, 結果正確? {correct}")
