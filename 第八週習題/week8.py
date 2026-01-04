"""
第八週習題 : 機率統計 - 檢定背後的數學原理
目標：
1. 實作 Z-test 公式 (單一樣本)
2. 實作 T-test 公式 (單一樣本、雙樣本獨立、雙樣本配對)
3. 驗證數學原理與公式推導
"""

import math
# 我們只用 scipy 來查找 P-value (因為積分計算繁瑣)，但統計量(t-score, z-score)全部手算
from scipy import stats

def calculate_mean(data):
    return sum(data) / len(data)

def calculate_std(data, ddof=1):
    """ 計算標準差，ddof=1 代表樣本標準差 (除以 n-1) """
    n = len(data)
    if n <= ddof: return 0.0
    mean_val = calculate_mean(data)
    variance = sum((x - mean_val) ** 2 for x in data) / (n - ddof)
    return math.sqrt(variance)

def z_test_one_sample(data, pop_mean, pop_std):
    """
    1. Z-test (單樣本)
    適用情境: 母體標準差(pop_std)已知，樣本數通常較大 (n > 30)
    公式: z = (x_bar - mu) / (sigma / sqrt(n))
    """
    n = len(data)
    sample_mean = calculate_mean(data)
    
    # 標準誤 (Standard Error)
    se = pop_std / math.sqrt(n)
    
    # Z 分數
    z_score = (sample_mean - pop_mean) / se
    
    # 雙尾 P-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    return z_score, p_value

def t_test_one_sample(data, pop_mean):
    """
    2-1. T-test (單樣本)
    適用情境: 母體標準差未知，用樣本標準差(s)取代
    公式: t = (x_bar - mu) / (s / sqrt(n))
    """
    n = len(data)
    sample_mean = calculate_mean(data)
    sample_std = calculate_std(data, ddof=1) # 樣本標準差
    
    # 標準誤 (Standard Error)
    se = sample_std / math.sqrt(n)
    
    # T 分數
    t_score = (sample_mean - pop_mean) / se
    
    # 雙尾 P-value (自由度 df = n - 1)
    df = n - 1
    p_value = 2 * (1 - stats.t.cdf(abs(t_score), df))
    
    return t_score, p_value

def t_test_independent(data1, data2):
    """
    2-2. T-test (雙樣本獨立)
    適用情境: 兩組獨立樣本，比較平均值是否相同
    假設: 變異數相等 (Pooled Variance)
    公式: t = (x1_bar - x2_bar) / sp * sqrt(1/n1 + 1/n2)
    """
    n1, n2 = len(data1), len(data2)
    m1, m2 = calculate_mean(data1), calculate_mean(data2)
    v1 = calculate_std(data1)**2
    v2 = calculate_std(data2)**2
    
    # 計算合併變異數 (Pooled Variance)
    # sp^2 = ((n1-1)s1^2 + (n2-1)s2^2) / (n1 + n2 - 2)
    pooled_var = ((n1 - 1)*v1 + (n2 - 1)*v2) / (n1 + n2 - 2)
    sp = math.sqrt(pooled_var)
    
    # 標準誤
    se = sp * math.sqrt(1/n1 + 1/n2)
    
    t_score = (m1 - m2) / se
    
    df = n1 + n2 - 2
    p_value = 2 * (1 - stats.t.cdf(abs(t_score), df))
    
    return t_score, p_value

def t_test_paired(data_before, data_after):
    """
    2-3. T-test (雙樣本配對)
    適用情境: 同一個體不同時間的測量 (例如: 服藥前 vs 服藥后)
    原理: 轉化為「差值」的單樣本 T 檢定
    公式: d = x_after - x_before, 檢定 d_bar 是否為 0
    """
    if len(data_before) != len(data_after):
        raise ValueError("配對樣本數量必須相同")
        
    # 計算差值 d
    diffs = [a - b for a, b in zip(data_after, data_before)]
    
    # 轉化為單樣本 T 檢定 (檢定差值平均是否為 0)
    return t_test_one_sample(diffs, pop_mean=0)

if __name__ == "__main__":
    print("=== 1. Z-test (單樣本) 驗證 ===")
    # 假設某班級數學成績，已知母體標準差為 10，檢定平均是否為 70
    data_z = [72, 75, 68, 70, 74, 78, 66, 71, 73, 69] # 平均 71.6
    pop_std_known = 10
    mu_0 = 70
    z, p = z_test_one_sample(data_z, mu_0, pop_std_known)
    print(f"樣本平均: {calculate_mean(data_z)}")
    print(f"Z-score: {z:.4f} (公式計算)")
    print(f"P-value: {p:.4f}\n")

    print("=== 2-1. T-test (單樣本) 驗證 ===")
    # 母體標準差未知，檢定平均是否為 70
    t, p = t_test_one_sample(data_z, mu_0)
    print(f"T-score: {t:.4f} (公式計算)")
    print(f"P-value: {p:.4f}\n")

    print("=== 2-2. T-test (雙樣本獨立) 驗證 ===")
    # A班 vs B班
    class_A = [80, 85, 88, 78, 82]
    class_B = [70, 75, 72, 68, 74]
    t, p = t_test_independent(class_A, class_B)
    print(f"A班平均: {calculate_mean(class_A)}, B班平均: {calculate_mean(class_B)}")
    print(f"T-score: {t:.4f} (公式計算)")
    print(f"P-value: {p:.4f}\n")

    print("=== 2-3. T-test (雙樣本配對) 驗證 ===")
    # 減肥前 vs 減肥後
    weight_pre = [80, 82, 78, 90, 75]
    weight_post = [78, 80, 75, 85, 74]
    t, p = t_test_paired(weight_pre, weight_post)
    diffs = [post - pre for pre, post in zip(weight_pre, weight_post)]
    print(f"體重變化平均: {calculate_mean(diffs)}")
    print(f"T-score: {t:.4f} (公式計算)")
    print(f"P-value: {p:.4f}")
