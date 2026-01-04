"""
期中作業 : 數學相關程式 - 曼德博集合 (Mandelbrot Set) 視覺化
目標：利用複數迭代函數 f(z) = z^2 + c，繪製出數學上著名的碎形圖案。
"""

import numpy as np
import matplotlib.pyplot as plt
import time

def mandelbrot(c, max_iter):
    """
    計算複數 c 是否屬於曼德博集合。
    核心公式：z(n+1) = z(n)^2 + c, z(0) = 0
    如果 |z| 超過 2，則認定為發散 (不屬於集合)。
    回傳：發散時的迭代次數 (用於著色)。
    """
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def generate_fractal(xmin, xmax, ymin, ymax, width, height, max_iter):
    """
    生成指定範圍內的曼德博集合影像數據。
    使用 Vectorization (向量化) 加速運算，避免雙重迴圈過慢。
    """
    # 建立座標網格
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    
    # 這裡為了簡單展示，我們先用簡單的迴圈邏輯 (雖然慢一點，但比較好理解數學原理)
    # 若要高效能，通常會使用 numpy 的廣播運算
    print(f"正在計算 {width}x{height} 的像素點，請稍候...")
    start_time = time.time()
    
    for i in range(width):
        for j in range(height):
            # 將像素座標轉換為複數平面座標
            real = r1[i]
            imag = r2[j]
            c = complex(real, imag)
            
            # 計算該點的逃逸時間
            n3[i, j] = mandelbrot(c, max_iter)
            
    end_time = time.time()
    print(f"計算完成！耗時: {end_time - start_time:.2f} 秒")
    return (r1, r2, n3)

def plot_mandelbrot(xmin, xmax, ymin, ymax, width=400, height=400, max_iter=256):
    """
    繪製並顯示曼德博集合
    """
    x, y, z = generate_fractal(xmin, xmax, ymin, ymax, width, height, max_iter)
    
    # 繪圖設定
    plt.figure(figsize=(10, 10))
    # 使用 'hot', 'magma', 'inferno' 等色票可以得到很酷的效果
    plt.imshow(z.T, extent=[xmin, xmax, ymin, ymax], cmap='magma', origin='lower')
    plt.colorbar(label='Iterations to Escape')
    plt.title(f"Mandelbrot Set\nRange: Real[{xmin}, {xmax}], Imag[{ymin}, {ymax}]")
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")
    plt.show()

if __name__ == "__main__":
    # 設定探索範圍 (標準曼德博集合全景)
    # 您可以嘗試修改這裡的數值來「放大」特定區域
    # 例如：放大頭部區域 xmin=-0.74877, xmax=-0.74872, ...
    x_min, x_max = -2.0, 0.5
    y_min, y_max = -1.25, 1.25
    
    # 解析度設定 (越高越清晰，但計算越久)
    img_width, img_height = 800, 800
    iterations = 100
    
    plot_mandelbrot(x_min, x_max, y_min, y_max, img_width, img_height, iterations)
