import numpy as np
from collections import Counter

def solve_ode_general(coefficients):
    """
    求解常係數齊次常微分方程
    輸入: coefficients (list) - 從最高階到最低階的係數
    輸出: 通解字串 y(x) = ...
    """
    # 1. 使用 numpy 求解特徵方程式的根
    # np.roots 接受的輸入順序正是 [an, an-1, ..., a0]
    raw_roots = np.roots(coefficients)
    
    # 2. 清洗數據 (處理浮點數誤差)
    # 我們將根四捨五入到小數點後 5 位，以便正確判定重根
    # 同時將極小的虛部視為 0 (處理實數根卻帶有 1e-15j 的情況)
    cleaned_roots = []
    for r in raw_roots:
        real_part = round(r.real, 5)
        imag_part = round(r.imag, 5)
        
        # 如果虛部極小，視為實數
        if abs(imag_part) == 0:
            cleaned_roots.append((real_part, 0.0))
        # 為了方便統計共軛複數，我們將複數根統一存為 (實部, 絕對值(虛部))
        # 這樣 a+bi 和 a-bi 會被視為同一組特徵
        else:
            cleaned_roots.append((real_part, abs(imag_part)))

    # 3. 統計每個根的重數 (Multiplicity)
    # Counter 會回傳如 {(2.0, 0.0): 2} 代表根為 2, 重數為 2
    root_counts = Counter(cleaned_roots)
    
    # 對根進行排序，讓輸出順序穩定 (先排實部，再排虛部)
    sorted_unique_roots = sorted(root_counts.keys(), key=lambda x: (x[0], x[1]))

    terms = []
    c_idx = 1 # 常數項編號 C_1, C_2...

    # 4. 根據根的類型建構解的字串
    for r_real, r_imag in sorted_unique_roots:
        count = root_counts[(r_real, r_imag)]
        
        # --- Case A: 實數根 (虛部為 0) ---
        if r_imag == 0:
            # 重根處理: 乘上 x^0, x^1, x^2...
            for power in range(count):
                term_str = f"C_{c_idx}"
                c_idx += 1
                
                # 處理 x 的次方 (重根修正項)
                if power == 1:
                    term_str += "x"
                elif power > 1:
                    term_str += f"x^{power}"
                
                # 處理指數項 e^(rx)
                if r_real != 0: # e^0x = 1，不顯示
                    # 格式化去掉不必要的 .0 (讓 2.0 顯示為 2)
                    r_str = f"{int(r_real)}" if r_real.is_integer() else f"{r_real}"
                    term_str += f"e^({r_str}x)"
                
                terms.append(term_str)
        
        # --- Case B: 複數根 (共軛複數) ---
        else:
            # 複數根成對出現，numpy 算出的 count 會包含共軛的兩個
            # 例如三重根會有 6 個解，實際上 m=3
            m = count // 2 
            
            for power in range(m):
                # 準備 x 的次方字串
                x_str = ""
                if power == 1: x_str = "x"
                elif power > 1: x_str = f"x^{power}"
                
                # 準備指數項字串 e^(alpha*x)
                exp_str = ""
                if r_real != 0:
                    r_str = f"{int(r_real)}" if r_real.is_integer() else f"{r_real}"
                    exp_str = f"e^({r_str}x)"
                
                # 準備 beta 字串
                beta_str = f"{int(r_imag)}" if r_imag.is_integer() else f"{r_imag}"

                # 建構 C_n * x * e * cos 和 C_m * x * e * sin
                # 習慣上先寫 cos 再寫 sin
                terms.append(f"C_{c_idx}{x_str}{exp_str}cos({beta_str}x)")
                c_idx += 1
                terms.append(f"C_{c_idx}{x_str}{exp_str}sin({beta_str}x)")
                c_idx += 1

    # 5. 組合最終字串
    if not terms:
        return "y(x) = 0"
    return "y(x) = " + " + ".join(terms)


# --- 測試主程式 ---

if __name__ == "__main__":
    # 範例測試 (1): 實數單根: y'' - 3y' + 2y = 0  (根: 1, 2)
    print("--- 實數單根範例 ---")
    coeffs1 = [1, -3, 2]
    print(f"方程係數: {coeffs1}")
    print(solve_ode_general(coeffs1))

    # 範例測試 (2): 實數重根: y'' - 4y' + 4y = 0  (根: 2, 2)
    print("\n--- 實數重根範例 ---")
    coeffs2 = [1, -4, 4]
    print(f"方程係數: {coeffs2}")
    print(solve_ode_general(coeffs2))

    # 範例測試 (3): 複數共軛根: y'' + 4y = 0  (根: 2i, -2i)
    print("\n--- 複數共軛根範例 ---")
    coeffs3 = [1, 0, 4]
    print(f"方程係數: {coeffs3}")
    print(solve_ode_general(coeffs3))

    # 範例測試 (4): 複數重根: (D^2 + 1)^2 y = 0 (根: i, i, -i, -i)
    print("\n--- 複數重根範例 ---")
    coeffs4 = [1, 0, 2, 0, 1]
    print(f"方程係數: {coeffs4}")
    print(solve_ode_general(coeffs4))

    # 範例測試 (5): 高階重根: (r-2)^3 = 0 -> r=2, 2, 2
    print("\n--- 高階重根範例 ---")
    coeffs5 = [1, -6, 12, -8]
    print(f"方程係數: {coeffs5}")
    print(solve_ode_general(coeffs5))
