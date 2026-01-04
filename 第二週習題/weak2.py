"""
習題 6 : 有限體 (Finite Field)
目標：
1. 實作有限體類別 (Galois Field, GF(p))
2. 驗證加法構成群 (Group)
3. 驗證乘法(排除0)構成群
4. 驗證分配律
5. 實作運算子重載 (+, -, *, /)
"""

class GF:
    """
    有限體元素類別 (Galois Field Element)
    代表 GF(p) 中的一個數字
    """
    def __init__(self, val, p):
        self.val = val % p
        self.p = p

    def __repr__(self):
        return f"{self.val}"

    # --- 運算子重載 (Operator Overloading) ---
    
    def __add__(self, other):
        # (a + b) mod p
        self._check_p(other)
        return GF(self.val + other.val, self.p)

    def __sub__(self, other):
        # (a - b) mod p
        self._check_p(other)
        return GF(self.val - other.val, self.p)

    def __mul__(self, other):
        # (a * b) mod p
        self._check_p(other)
        return GF(self.val * other.val, self.p)

    def __truediv__(self, other):
        # (a / b) mod p => a * b^(-1) mod p
        self._check_p(other)
        if other.val == 0:
            raise ZeroDivisionError("Cannot divide by zero in Finite Field")
        
        # 使用費馬小定理求乘法反元素: b^(p-2) mod p
        inverse = pow(other.val, self.p - 2, self.p)
        return GF(self.val * inverse, self.p)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.val == (other % self.p)
        return self.val == other.val and self.p == other.p

    def _check_p(self, other):
        if self.p != other.p:
            raise ValueError("Cannot operate on elements from different fields")

# --- 驗證邏輯 (Axiom Verification) ---

def check_group_axioms(elements, operation_name, op_func, identity_val):
    """
    驗證是否符合群 (Group) 的定義：
    1. 封閉性 (Closure) - 由類別定義保證
    2. 結合律 (Associativity): (a op b) op c == a op (b op c)
    3. 單位元素 (Identity): a op e == a
    4. 反元素 (Inverse): a op a' == e
    """
    print(f"--- 驗證 {operation_name} 群性質 ---")
    
    # 1. 檢查結合律
    for a in elements:
        for b in elements:
            for c in elements:
                res1 = op_func(op_func(a, b), c)
                res2 = op_func(a, op_func(b, c))
                if res1 != res2:
                    print(f"❌ 結合律失敗: ({a}{operation_name}{b}){operation_name}{c} != {a}{operation_name}({b}{operation_name}{c})")
                    return False
    print("✅ 結合律 (Associativity) 通過")

    # 2. 檢查單位元素
    identity_element = None
    for e in elements:
        is_identity = True
        for a in elements:
            if op_func(a, e) != a or op_func(e, a) != a:
                is_identity = False
                break
        if is_identity:
            identity_element = e
            break
            
    if identity_element is None or identity_element.val != identity_val:
        print(f"❌ 找不到正確的單位元素 (預期 {identity_val})")
        return False
    print(f"✅ 單位元素 (Identity) 存在且正確: {identity_element}")

    # 3. 檢查反元素
    for a in elements:
        has_inverse = False
        for b in elements:
            if op_func(a, b) == identity_element and op_func(b, a) == identity_element:
                has_inverse = True
                break
        if not has_inverse:
            print(f"❌ 元素 {a} 沒有反元素")
            return False
    print("✅ 反元素 (Inverse) 對所有元素皆存在")
    
    print(f"🎉 {operation_name} 構成一個群 (Group)！\n")
    return True

def check_distributivity(elements):
    """
    驗證分配律: a * (b + c) == a * b + a * c
    """
    print("--- 驗證 分配律 (Distributivity) ---")
    for a in elements:
        for b in elements:
            for c in elements:
                # 左式: a * (b + c)
                left = a * (b + c)
                # 右式: a * b + a * c
                right = (a * b) + (a * c)
                
                if left != right:
                    print(f"❌ 分配律失敗: {a} * ({b} + {c}) != {a}*{b} + {a}*{c}")
                    return False
    print("✅ 分配律 (Distributivity) 通過！\n")
    return True

# --- 主程式 ---

if __name__ == "__main__":
    # 設定質數 p，例如 p = 5
    P = 5
    print(f"正在建立 GF({P}) 的所有元素...\n")
    
    # 產生 GF(5) 的所有元素: {0, 1, 2, 3, 4}
    all_elements = [GF(i, P) for i in range(P)]
    
    # 產生乘法群元素 (排除
