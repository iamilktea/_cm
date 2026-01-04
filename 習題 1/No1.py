
"""
習題 1 : 請用程式驗證微積分基本定理 #1
目標：驗證 d/dx (∫ f(t) dt) = f(x)
"""

# 設定一個微小的步長，用於近似計算
h = 0.0001 

def integral(f, a, b):
    """
    使用黎曼和 (Riemann Sum) 來計算定積分
    f: 函數
    a: 下限
    b: 上限
    """
    area = 0.0
    x = a
    while x < b:
        area += f(x) * h
        x += h
    return area

def df(f, x):
    """
    使用差分商 (Difference Quotient) 來計算導數
    f: 函數
    x: 位置
    定義：(f(x+h) - f(x)) / h
    """
    return (f(x + h) - f(x)) / h

def f(x):
    """
    測試用的函數，例如 f(x) = x^2
    """
    return x**2

def theorem1(f, x):
    """
    驗證微積分基本定理第一部分
    注意：因為是數值近似，不能用 == (完全相等)，
    必須檢查誤差是否在容許範圍內 (epsilon)。
    """
    # G(x) = 積分 f(t) 從 0 到 x
    def G(x):
        return integral(f, 0, x)
    
    # 計算 G(x) 的導數
    derivative_of_integral = df(G, x)
    original_function_value = f(x)
    
    print(f"位置 x={x}:")
    print(f"  G'(x) (積分後微分) = {derivative_of_integral:.5f}")
    print(f"  f(x)  (原函數值)   = {original_function_value:.5f}")
    
    # 驗證兩者是否非常接近 (誤差小於 0.01)
    diff = abs(derivative_of_integral - original_function_value)
    assert diff < 0.01, f"驗證失敗，誤差過大: {diff}"
    print("✅ 驗證成功 (誤差在容許範圍內)")
    print("-" * 30)

if __name__ == "__main__":
    # 測試幾個不同的 x 值
    theorem1(f, 1.0)
    theorem1(f, 2.0)
    theorem1(f, 3.0)
