import numpy as np

def rls_adaptive_filter(input_signal, desired_signal, filter_length, forgetting_factor):
    # 初始化权重向量和协方差矩阵
    w = np.zeros(filter_length)
    P = np.eye(filter_length) / 0.01
    
    # RLS 算法迭代更新
    for i in range(len(input_signal)):
        x = input_signal[i:i+filter_length]
        d = desired_signal[i]
        
        # 计算增益向量
        k = P @ x / (forgetting_factor + x.T @ P @ x)
        
        # 更新权重向量和协方差矩阵
        w = w + k * (d - x.T @ w)
        P = (1/forgetting_factor) * (P - k @ x.T @ P)
    
    return w

# 示例使用
# 输入信号和期望信号
input_signal = np.random.randn(1000)  # 示例随机生成输入信号
desired_signal = np.convolve(input_signal, np.array([1, 0.5, 0.2]), mode='same')  # 示例期望信号

# RLS 参数
filter_length = 3  # 滤波器长度
forgetting_factor = 0.99  # 遗忘因子

# 应用 RLS 算法
estimated_weights = rls_adaptive_filter(input_signal, desired_signal, filter_length, forgetting_factor)

print("Estimated weights:", estimated_weights)
