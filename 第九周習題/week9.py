"""
第九週習題 : 資訊理論 - 熵、互資訊與漢明碼
目標：
1. 解決機率下溢問題 (Underflow)
2. 計算 Entropy, Cross Entropy, KL Divergence, Mutual Information
3. 驗證 Gibbs Inequality (修正題目敘述)
4. 實作 (7,4) 漢明碼的編碼與解碼 (包含錯誤更正)
"""

import math
import random

# --- 1. & 2. 基礎機率與對數 ---

def prob_underflow_demo():
    print("--- 1. & 2. 機率下溢與對數運算 ---")
    p = 0.5
    n = 10000
    
    # 直接計算 p^n
    # 在 Python 中，0.5**10000 會因為數值太小直接變成 0.0
    prob_direct = p ** n
    print(f"直接計算 0.5^{n}: {prob_direct} (發生下溢 Underflow)")
    
    # 使用對數計算 log(p^n) = n * log(p)
    # 資訊理論中通常使用底數為 2 (單位: bit)
    log_prob = n * math.log2(p)
    print(f"對數計算 log2(0.5^{n}): {log_prob:.4f} bits")
    print("說明: 這代表發生該事件的資訊量極大，或者機率極小 (2^-10000)\n")

# --- 3. 資訊量度量 ---

def entropy(p):
    """ H(P) = - sum(p(x) log2 p(x)) """
    return -sum(pi * math.log2(pi) for pi in p if pi > 0)

def cross_entropy(p, q):
    """ H(P, Q) = - sum(p(x) log2 q(x)) """
    # 避免 log(0)
    return -sum(pi * math.log2(qi) for pi, qi in zip(p, q) if qi > 0)

def kl_divergence(p, q):
    """ D_KL(P||Q) = sum(p(x) log2 (p(x)/q(x))) = H(P, Q) - H(P) """
    return sum(pi * math.log2(pi / qi) for pi, qi in zip(p, q) if pi > 0 and qi > 0)

def mutual_information(pxy, px, py):
    """ 
    I(X;Y) = sum(p(x,y) * log2( p(x,y) / (p(x)p(y)) )) 
    這裡簡化輸入，假設 pxy 是聯合機率矩陣，px, py 是邊緣機率
    """
    mi = 0.0
    for i in range(len(px)):
        for j in range(len(py)):
            if pxy[i][j] > 0:
                mi += pxy[i][j] * math.log2(pxy[i][j] / (px[i] * py[j]))
    return mi

def measure_demo():
    print("--- 3. & 4. 熵、交叉熵、KL 散度 ---")
    # 定義兩個機率分佈 P (真實) 和 Q (預測)
    P = [0.8, 0.2] # 例如：銅板主要正面
    Q = [0.5, 0.5] # 猜測是公平銅板
    
    h_p = entropy(P)
    ce_pq = cross_entropy(P, Q)
    ce_pp = cross_entropy(P, P)
    kl = kl_divergence(P, Q)
    
    print(f"真實分佈 P: {P}, 預測分佈 Q: {Q}")
    print(f"熵 H(P): {h_p:.4f}")
    print(f"交叉熵 H(P, Q): {ce_pq:.4f}")
    print(f"交叉熵 H(P, P): {ce_pp:.4f} (即 H(P))")
    print(f"KL 散度 D_KL(P||Q): {kl:.4f}")
    
    # 驗證題目 4: cross_entropy(p,p) 與 cross_entropy(p,q) 的關係
    # 根據吉布斯不等式 (Gibbs' Inequality): H(P, Q) >= H(P)
    # 所以 H(P, P) 應該小於或等於 H(P, Q)
    print(f"\n驗證 H(P, P) < H(P, Q) (當 P!=Q):")
    print(f"{ce_pp:.4f} < {ce_pq:.4f} ? {ce_pp < ce_pq}")
    print("注意：題目圖片可能筆誤寫成 >，但數學上交叉熵在分佈相同時最小。")

# --- 5. 漢明碼 (7,4) Hamming Code ---

class Hamming74:
    """
    使用矩陣運算實作 (7,4) 漢明碼
    G: 生成矩陣 (4x7)
    H: 奇偶校驗矩陣 (3x7)
    """
    def __init__(self):
        # 系統碼形式: G = [I | P]
        # 資料位元 d1 d2 d3 d4 -> 碼字 d1 d2 d3 d4 p1 p2 p3
        self.G = [
            [1, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ]
        # H = [P^T | I]
        self.H = [
            [1, 1, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 0, 1]
        ]
        # 用於將校驗子 (Syndrome) 映射到錯誤位置索引 (0-6)
        # H 的行向量 (轉置後) 對應二進位數值
        # Col 0: 110 (6) -> 實際上我們的 H 定義不同，需動態查表
        self.syndrome_map = {}
        for col in range(7):
            syn_tuple = tuple(self.H[row][col] for row in range(3))
            self.syndrome_map[syn_tuple] = col

    def encode(self, data_bits):
        """ 輸入 4 bits (list), 輸出 7 bits """
        if len(data_bits) != 4: raise ValueError("Input must be 4 bits")
        # 向量乘法 c = d * G (mod 2)
        codeword = [0] * 7
        for col in range(7):
            val = sum(data_bits[row] * self.G[row][col] for row in range(4))
            codeword[col] = val % 2
        return codeword

    def decode(self, received_bits):
        """ 輸入 7 bits, 輸出修正後的 4 bits """
        if len(received_bits) != 7: raise ValueError("Input must be 7 bits")
        # 計算校驗子 s = r * H^T (mod 2)
        syndrome = []
        for row in range(3):
            val = sum(received_bits[col] * self.H[row][col] for col in range(7))
            syndrome.append(val % 2)
        
        s_tuple = tuple(syndrome)
        
        # 複製一份以免修改原始數據
        corrected = list(received_bits)
        
        if sum(syndrome) == 0:
            status = "No Error"
        else:
            if s_tuple in self.syndrome_map:
                error_pos = self.syndrome_map[s_tuple]
                status = f"Error at index {error_pos}"
                # 翻轉錯誤位元
                corrected[error_pos] = 1 - corrected[error_pos]
            else:
                status = "Uncorrectable Error"

        # 回傳前 4 位 (系統碼特性)
        return corrected[:4], status

def hamming_demo():
    print("\n--- 5. 漢明碼 (7,4) 編碼與解碼 ---")
    hamming = Hamming74()
    
    # 測試資料
    data = [1, 0, 1, 1]
    print(f"原始資料 (4 bits): {data}")
    
    # 編碼
    encoded = hamming.encode(data)
    print(f"編碼結果 (7 bits): {encoded}")
    
    # 模擬傳輸錯誤 (翻轉第 2 個 bit, index 1)
    received = list(encoded)
    error_idx = 1
    received[error_idx] = 1 - received[error_idx]
    print(f"接收資料 (有雜訊): {received} (翻轉 index {error_idx})")
    
    # 解碼與更正
    decoded, status = hamming.decode(received)
    print(f"解碼結果: {decoded}")
    print(f"狀態報告: {status}")
    print(f"是否還原成功? {decoded == data}")

if __name__ == "__main__":
    prob_underflow_demo()
    measure_demo()
    hamming_demo()
