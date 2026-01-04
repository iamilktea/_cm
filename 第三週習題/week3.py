"""
習題 9 : 幾何學 - (點, 線, 圓) 世界的建構
目標：
1. 定義幾何物件類別。
2. 實作交點計算 (線線、線圓、圓圓)。
3. 實作垂線與畢氏定理驗證。
4. 實作幾何變換 (平移、縮放、旋轉)。
"""

import math

class Point:
    """ 定義「點」及其基本運算 """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def __add__(self, other): # 向量加法
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other): # 向量減法
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar): # 純量乘法
        return Point(self.x * scalar, self.y * scalar)
    
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    # --- 幾何變換 ---
    def translate(self, dx, dy):
        return Point(self.x + dx, self.y + dy)

    def scale(self, factor):
        return Point(self.x * factor, self.y * factor)

    def rotate(self, angle_deg, center=None):
        """ 繞著 center 旋轉 (預設繞原點) """
        if center is None: center = Point(0, 0)
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # 平移到相對原點
        dx = self.x - center.x
        dy = self.y - center.y
        
        # 旋轉矩陣應用
        new_x = dx * cos_a - dy * sin_a
        new_y = dx * sin_a + dy * cos_a
        
        # 平移回去
        return Point(new_x + center.x, new_y + center.y)


class Line:
    """ 定義「線」(由兩點決定) """
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        # 一般式 ax + by = c
        self.a = p1.y - p2.y
        self.b = p2.x - p1.x
        self.c = self.a * p1.x + self.b * p1.y

    def __repr__(self):
        return f"Line[{self.p1} -> {self.p2}]"

    def intersect_line(self, other):
        """ 計算兩直線交點 (使用克拉瑪公式) """
        det = self.a * other.b - other.a * self.b
        if abs(det) < 1e-9:
            return None # 平行無交點
        x = (other.b * self.c - self.b * other.c) / det
        y = (self.a * other.c - other.a * self.c) / det
        return Point(x, y)

    def get_projection(self, p):
        """ 計算點 p 在此直線上的投影點 (垂足) """
        # 使用向量投影公式
        # 向量 AB
        ab = self.p2 - self.p1
        # 向量 AP
        ap = p - self.p1
        
        # AP 在 AB 上的投影長度比例 t = (AP dot AB) / |AB|^2
        t = (ap.x * ab.x + ap.y * ab.y) / (ab.x**2 + ab.y**2)
        
        # 投影點 = A + t * AB
        return self.p1 + (ab * t)

    def transform(self, func, *args):
        """ 通用變換函數 """
        return Line(func(self.p1, *args), func(self.p2, *args))


class Circle:
    """ 定義「圓」 """
    def __init__(self, center, r):
        self.center = center
        self.r = r

    def __repr__(self):
        return f"Circle(Center={self.center}, R={self.r:.2f})"

    def intersect_line(self, line):
        """ 直線與圓的交點 """
        # 幾何法：先找圓心到直線的投影點(垂足) P
        projection = line.get_projection(self.center)
        dist = projection.distance(self.center)
        
        if dist > self.r:
            return [] # 不相交
        
        # 計算弦長的一半
        h = math.sqrt(abs(self.r**2 - dist**2))
        
        # 單位方向向量
        dx = line.p2.x - line.p1.x
        dy = line.p2.y - line.p1.y
        length = math.sqrt(dx**2 + dy**2)
        ux, uy = dx/length, dy/length
        
        # 交點 = 投影點 +/- h * 方向向量
        p1 = Point(projection.x + ux * h, projection.y + uy * h)
        p2 = Point(projection.x - ux * h, projection.y - uy * h)
        
        if dist == self.r: return [p1] # 切點
        return [p1, p2]

    def intersect_circle(self, other):
        """ 圓與圓的交點 """
        d = self.center.distance(other.center)
        
        if d > self.r + other.r or d < abs(self.r - other.r) or d == 0:
            return [] # 外離、內含或同心圓
            
        # 餘弦定理求出交點相對於連心線的角度與距離
        a = (self.r**2 - other.r**2 + d**2) / (2 * d)
        h = math.sqrt(abs(self.r**2 - a**2))
        
        # 連心線單位向量 (P2 - P1) / d
        x2 = other.center.x - self.center.x
        y2 = other.center.y - self.center.y
        x3 = self.center.x + a * (x2 / d)
        y3 = self.center.y + a * (y2 / d)
        
        # 旋轉 90 度得到交點偏移量
        x4_1 = x3 + h * (y2 / d) * -1
        y4_1 = y3 + h * (x2 / d)
        x4_2 = x3 - h * (y2 / d) * -1
        y4_2 = y3 - h * (x2 / d)
        
        return [Point(x4_1, y4_1), Point(x4_2, y4_2)]

    def transform(self, func, *args):
        # 圓的縮放比較特別，半徑也要變，這裡假設均勻縮放
        new_center = func(self.center, *args)
        # 如果是 scale 操作，args[0] 通常是 factor
        new_r = self.r
        if func.__name__ == 'scale':
             new_r *= args[0]
        return Circle(new_center, new_r)


class Triangle:
    """ 定義「三角形」 """
    def __init__(self, p1, p2, p3):
        self.points = [p1, p2, p3]

    def __repr__(self):
        return f"Triangle{self.points}"

    def transform(self, func, *args):
        new_pts = [func(p, *args) for p in self.points]
        return Triangle(*new_pts)


# --- 測試與驗證邏輯 ---

def verify_pythagoras(line, point_outside):
    print("\n--- 驗證畢氏定理 ---")
    print(f"直線: {line}")
    print(f"線外一點 P: {point_outside}")
    
    # 1. 找垂足 (F)
    foot = line.get_projection(point_outside)
    print(f"垂足 F: {foot}")
    
    # 2. 在線上隨便找另一點 A (這裡直接用線的起點 p1)
    p_on_line = line.p1
    print(f"線上另一點 A: {p_on_line}")
    
    # 3. 計算三邊長
    a = point_outside.distance(foot)      # PF (股)
    b = foot.distance(p_on_line)          # FA (股)
    c = point_outside.distance(p_on_line) # PA (斜邊)
    
    print(f"PF = {a:.4f}, FA = {b:.4f}, PA = {c:.4f}")
    
    # 4. 驗證 a^2 + b^2 = c^2
    left = a**2 + b**2
    right = c**2
    print(f"{a:.4f}^2 + {b:.4f}^2 = {left:.4f}")
    print(f"{c:.4f}^2 = {right:.4f}")
    
    if math.isclose(left, right, rel_tol=1e-9):
        print("✅ 畢氏定理驗證成功！")
    else:
        print("❌ 驗證失敗")

def main():
    # 1. 初始化物件
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(0, 3)
    line1 = Line(p1, p2) # y=0
    line2 = Line(Point(2, -1), Point(2, 5)) # x=2
    circle1 = Circle(Point(0, 0), 5)
    circle2 = Circle(Point(3, 0), 4) # (x-3)^2 + y^2 = 16
    tri = Triangle(p1, p2, p3)

    print(f"幾何物件:\n L1:{line1}\n L2:{line2}\n C1:{circle1}\n C2:{circle2}\n T1:{tri}")

    # 2. 交點計算
    print("\n--- 交點計算 ---")
    print(f"L1 與 L2 交點: {line1.intersect_line(line2)}")
    
    inter_lc = circle1.intersect_line(Line(Point(-10, 3), Point(10, 3))) # y=3 與 x^2+y^2=25 => x=+-4
    print(f"C1 與 y=3 交點: {inter_lc}")
    
    inter_cc = circle1.intersect_circle(circle2)
    print(f"C1 與 C2 交點: {inter_cc}")

    # 3. 畢氏定理驗證
    # 建立一條線 y = x 和一個點 (0, 2)
    l_ver = Line(Point(0, 0), Point(5, 5))
    p_ver = Point(0, 2)
    verify_pythagoras(l_ver, p_ver)

    # 4. 幾何變換
    print("\n--- 幾何變換 (三角形) ---")
    print(f"原始: {tri}")
    
    # 平移 (10, 10)
    tri_trans = tri.transform(Point.translate, 10, 10)
    print(f"平移後: {tri_trans}")
    
    # 旋轉 90度 (繞原點)
    tri_rot = tri.transform(Point.rotate, 90, Point(0,0))
    print(f"旋轉後: {tri_rot}")

if __name__ == "__main__":
    main()
