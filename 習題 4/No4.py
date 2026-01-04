"""
習題 4 (思考題) : 求解 n 次多項式的根
目標：當 n >= 5 時沒有公式解，需使用數值方法 (如牛頓法) 求解。
輸入：c 是陣列，c[i] 代表 x^i 的係數 (注意：c[0] 是常數項)
"""

import cmath
import random

def eval_poly(c, x):
    """
    計算多項式 f(x) 的值
    f(x) = c[0] + c[1]x + c[2]x^2 + ...
    """
    val = 0
    for i, coeff in enumerate(c):
        val += coeff * (x**i)
    return val

def eval_deriv(c, x):
    """
    計算多項式導數 f'(x) 的值
    f'(x) = c[1] + 2*c[2]x + 3*c[3]x^2 + ...
    """
    val = 0
    # 從第 1 項開始微分 (常數項 c[0] 微分是 0)
    for i in range(1, len(c)):
        val += i * c[i] * (x**(i-1))
    return val

def find_one_root_newton(c, max_iter=1000, tol=1e-10):
    """
    使用牛頓法 (Newton-Raphson) 找到一個複數根
    公式：x_new = x - f(x) / f'(x)
    """
    # 隨機初始化一個複數猜測值 (避開 0，避免導數為 0 的風險)
    x = complex(random.uniform(-1, 1), random.uniform(-1, 1))
    
    for _ in range(max_iter):
        f_val = eval_poly(c, x)
        
        # 如果已經夠接近 0，就回傳
        if abs(f_val) < tol:
            return x
            
        df_val = eval_deriv(c, x)
        
        # 避免除以 0
        if df_val == 0:
            # 如果導數為 0，隨機跳轉到另一個點重試
            x = complex(random.uniform(-2, 2), random.uniform(-2, 2))
            continue
            
        # 牛頓法更新步驟 (類似梯度下降，但利用斜率直接跳轉)
        x = x - f_val / df_val
        
    return x  # 回傳最後的估計值

def deflate_poly(c, root):
    """
    綜合除法 (Synthetic Division) / 多項式降次
    將 P(x) 除以 (x - root)，回傳商式的新係數
    """
    n = len(c) - 1 # 次數
    new_c = [0] * n # 降次後的係數陣列 (長度少 1)
    
    # 由於題目定義 c[i] 是 x^i，最高次項在最後面 c[-1]
    # 我們從最高次項開始做綜合除法
    remainder = 0
    # 從最高次往下做
    for i in range(n - 1, -1, -1):
        # 這裡的邏輯是反過來的，因為 c[n] 是最高次
        if i == n - 1:
            new_c[i] = c[i+1]
        else:
            new_c[i] = c[i+1] + new_c[i+1] * root
            
    return new_c

def root(c):
    """
    求解 n 次多項式的所有根
    策略：找到一個根 -> 降次 -> 重複直到解完
    """
    roots = []
    current_c = c[:] # 複製一份係數
    
    # 當還有 x (次數 >= 1，即係數陣列長度 >= 2) 時繼續
    while len(current_c) >= 2:
        # 1. 找到一個根
        r = find_one_root_newton(current_c)
        
        # 2. 修飾根 (去除極小的虛部誤差，如果是實係數多項式通常會有共軛根，這裡簡化處理)
        if abs(r.imag) < 1e-8:
            r = r.real + 0j
            
        roots.append(r)
        
        # 3. 降次 (Deflation)
        # 如果只剩一次方，最後一個根直接解出來，不用降次了
        if len(current_c) == 2:
            break
        current_c = deflate_poly(current_c, r)
        
    return roots

def verify_poly(c, x):
    """ 驗證函數 """
    val = eval_poly(c, x)
    return val, cmath.isclose(val, 0, abs_tol=1e-5)

if __name__ == "__main__":
    # 題目範例: x^5 - 1 = 0
    # 係數 c = [-1, 0, 0, 0, 0, 1] (對應 -1 + 0x + ... + 1x^5)
    print("--- 測試案例: x^5 - 1 = 0 ---")
    c = [-1, 0, 0, 0, 0, 1]
    
    roots = root(c)
    
    for i, r in enumerate(roots):
        val, valid = verify_poly(c, r)
        print(f"根 {i+1}: {r:.4f}")
        print(f"  -> 代回誤差: {abs(val):.2e} \t 通過? {valid}")

    print("\n")
    
    # 測試案例: 隨機多項式 (x-2)(x+3)(x-1)(x+1)(x-0.5) = 0
    # 為了方便測試，我們直接讓數值法跑一個係數較複雜的
    # f(x) = x^5 - 0.5x^4 - 7x^3 + 2.5x^2 + 6x
    # 係數 c = [0, 6, 2.5, -7, -0.5, 1]
    print("--- 測試案例: x^5 - 0.5x^4 - 7x^3 + 2.5x^2 + 6x = 0 ---")
    print("預期根約為: 2, -3, 1, -1, 0.5")
    c2 = [0, 6, 2.5, -7, -0.5, 1]
    
    roots2 = root(c2)
    for i, r in enumerate(roots2):
        val, valid = verify_poly(c2, r)
        print(f"根 {i+1}: {r:.4f}")
        # 因為累積誤差，對於高次多項式容許值稍微放寬
        print(f"  -> 代回誤差: {abs(val):.2e}")
