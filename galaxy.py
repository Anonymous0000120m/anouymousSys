import numpy as np
import matplotlib.pyplot as plt

# 定义常量
light_year = 9.461e15  # 光年到米的转换因子
distance = 10 * light_year  # 10光年的距离

# 定义行星的初始位置和速度（示例数据，实际应根据具体行星数据调整）
initial_positions = np.array([0, 0, 0])  # 初始位置为原点
initial_velocities = np.array([10000, 0, 0])  # 初始速度为x轴正向10000m/s

# 计算10光年前、现在和10光年后的位置
delta_time = np.linspace(-1, 1, 1000)  # 时间范围为[-1, 1]，单位为年
positions = initial_positions[:, np.newaxis] + initial_velocities[:, np.newaxis] * delta_time

# 绘制轨迹图
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(positions[0], positions[1], positions[2], label='Planet Orbit')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('Planet Orbit at 10 Light Years Away')
plt.legend()
plt.show()