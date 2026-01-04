"""
習題 10 (第 12 週) : 線性代數 - 觀念與實作
目標：
1. 遞迴計算行列式
2. LU 分解與行列式計算
3. 驗證 LU, Eigen, SVD 分解
4. 使用 Eigendecomposition 實作 SVD
5. 實作 PCA
"""

import numpy as np

# --- 1. 遞迴方式計算行列式 (Recursive Determinant) ---
def get_minor(matrix, i, j):
    """ 取得刪除第 i 列與第 j 行後的子矩陣 """
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

def det_recursive(matrix):
    """ 使用拉普拉斯展開 (Laplace Expansion) 計算行列式 """
    # Base case: 2x2 矩陣
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

    determinant = 0
    # 沿著第一列 (row 0) 展開
    for c in range(len(matrix)):
        determinant += ((-1)**c) * matrix[0][c] * det_recursive(get_minor(matrix, 0, c))
    return determinant

# --- 2. LU 分解 (Doolittle Algorithm) ---
def lu_decomposition_manual(A):
    """ 
    手動實作 LU 分解 (假設矩陣可逆且不需要 Pivot 交換)
    A = L * U
    L: 下三角 (對角線為 1)
    U: 上三角
    """
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    for i in range(n):
        # Upper Triangular
        for k in range(i, n):
            sum_val = sum((L[i][j] * U[j][k]) for j in range(i))
            U[i][k] = A[i][k] - sum_val

        # Lower Triangular
        for k in range(i, n):
            if i == k:
                L[i][i] = 1 # 對角線設為 1
            else:
                sum_val = sum((L[k][j] * U[j][i]) for j in range(i))
                L[k][i] = (A[k][i] - sum_val) / U[i][i]
    return L, U

def det_via_lu(U):
    """ 行列式等於上三角矩陣 U 的對角線乘積 """
    det = 1.0
    for i in range(len(U)):
        det *= U[i][i]
    return det

# --- 3. 驗證各種分解 (Verification) ---
def verify_decompositions(A):
    print("\n--- 3. 驗證分解 (使用 Numpy) ---")
    
    # (1) LU 分解驗證
    # 注意: numpy 預設會做 PLU (包含列交換 P)
    from scipy.linalg import lu
    P, L, U = lu(A)
    reconstructed_A = P @ L @ U
    print(f"[LU] A == P*L*U? {np.allclose(A, reconstructed_A)}")
    
    # (2) 特徵值分解驗證 (Eigendecomposition)
    # A = V * D * V^-1
    evals, evecs = np.linalg.eig(A)
    D = np.diag(evals)
    # A * V = V * D
    left = A @ evecs
    right = evecs @ D
    print(f"[Eigen] A*V == V*D? {np.allclose(left, right)}")

    # (3) SVD 分解驗證
    # A = U * S * Vh
    U_svd, S, Vh = np.linalg.svd(A)
    S_mat = np.zeros_like(A, dtype=float)
    np.fill_diagonal(S_mat, S)
    reconstructed_A_svd = U_svd @ S_mat @ Vh
    print(f"[SVD] A == U*S*Vh? {np.allclose(A, reconstructed_A_svd)}")

# --- 4. 用特徵值分解來做 SVD (SVD via Eigen) ---
def svd_via_eigen(A):
    """
    SVD 原理:
    1. A^T A 的特徵向量是 V
    2. A^T A 的特徵值開根號是 Singular Values (S)
    3. A A^T 的特徵向量是 U (或者用 U = A * V / S 計算)
    """
    print("\n--- 4. 使用 Eigen 實作 SVD ---")
    ATA = A.T @ A
    
    # 1. 求 eigenvalues (lambda) 和 eigenvectors (V)
    evals, V = np.linalg.eig(ATA)
    
    # 排序 (SVD 要求奇異值從大到小)
    idx = evals.argsort()[::-1]
    evals = evals[idx]
    V = V[:, idx]
    
    # 2. 計算 Singular Values (sigma = sqrt(lambda))
    # 處理極小的負值誤差
    evals = np.maximum(evals, 0)
    S = np.sqrt(evals)
    
    # 3. 計算 U: u_i = (1/sigma_i) * A * v_i
    # 過濾掉 sigma 為 0 的部分
    rank = np.sum(S > 1e-10)
    U = np.zeros((A.shape[0], rank))
    
    for i in range(rank):
        U[:, i] = (A @ V[:, i]) / S[i]
        
    print("手算 SVD Singular Values:", S)
    return U, S, V.T

# --- 5. PCA 主成份分析 ---
def pca_implementation(data, n_components=2):
    print(f"\n--- 5. PCA 實作 (降至 {n_components} 維) ---")
    # 1. 中心化 (Center the data)
    mean = np.mean(data, axis=0)
    centered_data = data - mean
    
    # 2. 計算共變異數矩陣 (Covariance Matrix)
    # rowvar=False 代表每一行是一個 feature
    cov_matrix = np.cov(centered_data, rowvar=False)
    
    #
