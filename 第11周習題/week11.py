"""
第 11 週習題 : 傅立葉轉換 (Fourier Transform)
目標：
1. 不使用套件，實作離散傅立葉轉換 (DFT)
2. 不使用套件，實作逆離散傅立葉轉換 (IDFT)
3. 驗證轉換後再轉回，是否等於原訊號
"""

import math
import cmath

def dft(x):
    """
    離散傅立葉轉換 (Discrete Fourier Transform)
    將時域訊號 x[n] 轉換為頻域訊號 X[k]
    公式: X[k] = sum_{n=0}^{N-1} x[n] * e^(-i * 2*pi * k * n / N)
    """
    N = len(x)
    X = []
    
    # 對每一個頻率分量 k 進行計算
    for k in range(N):
        sum_val = 0 + 0j
        for n in range(N):
            # 歐拉公式: e^(-ix) = cos(x) - i*sin(x)
            # 這裡是利用 cmath.exp 直接處理複數指數
            theta = 2 * math.pi * k * n / N
            w = cmath.exp(-1j * theta) 
            sum_val += x[n] * w
        X.append(sum_val)
        
    return X

def idft(X):
    """
    逆離散傅立葉轉換 (Inverse Discrete Fourier Transform)
    將頻域訊號 X[k] 還原為時域訊號 x[n]
    公式: x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * e^(i * 2*pi * k * n / N)
    """
    N = len(X)
    x_recon = []
    
    # 對每一個時間點 n 進行還原
    for n in range(N):
        sum_val = 0 + 0j
        for k in range(N):
            # 正轉換是指數負次方，逆轉換是指數正次方
            theta = 2 * math.pi * k * n / N
            w = cmath.exp(1j * theta)
            sum_val += X[k] * w
            
        # 逆轉換通常需要除以 N (正規化)
        x_recon.append(sum_val / N)
        
    return x_recon

def verify_signal(original, reconstructed):
    """
    驗證兩個訊號是否極度相似
    """
    N = len(original)
    error = 0.0
    for i in range(N):
        # 比較實部 (因為原始訊號通常是實數，虛部應該要是 0 或極小)
        diff = abs(original[i] - reconstructed[i])
        error += diff
    
    print(f"總誤差 (Total Error): {error:.2e}")
    # 允許極小的浮點數運算誤差
    return error < 1e-9

if __name__ == "__main__":
    # 1. 準備一個簡單的測試訊號 (例如: [1, 0, 1, 0])
    # 或是模擬一個簡單的波形
    f = [1.0, 2.0, 4.0, 2.0, 1.0, 0.0, 0.0, 0.0]
    print(f"原始訊號 f(x): {f}")

    # 2. 執行 DFT (正轉換)
    F = dft(f)
    print("\nDFT 結果 F(w) (頻域):")
    for i, val in enumerate(F):
        # 格式化輸出複數，方便閱讀
        print(f"  Freq {i}: {val.real:.4f} + {val.imag:.4f}j")

    # 3. 執行 IDFT (逆轉換)
    f_recon = idft(F)
    # 取實部 (因為原始訊號是實數，理論上虛部應為 0)
    f_recon_real = [val.real for val in f_recon]
    
    print(f"\nIDFT 還原訊號 f'(x):")
    print([round(v, 4) for v in f_recon_real])

    # 4. 驗證
    if verify_signal(f, f_recon):
        print("\n✅ 驗證成功：正轉換再逆轉換後還原為原函數！")
    else:
        print("\n❌ 驗證失敗：誤差過大")
