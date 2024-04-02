import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_planet_orbit(initial_position, initial_velocity, distance, num_points=1000):
    # 计算时间范围
    time_range = np.linspace(-distance / np.linalg.norm(initial_velocity), distance / np.linalg.norm(initial_velocity), num_points)

    # 计算行星位置
    positions = initial_position[:, np.newaxis] + initial_velocity[:, np.newaxis] * time_range

    return positions

def plot_orbit(positions, planet_name):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(positions[0], positions[1], positions[2], label=f'{planet_name} Orbit')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(f'{planet_name} Orbit at 10 Light Years Away')
    plt.legend()
    plt.savefig(f'{planet_name}_orbit.png')  # 保存图片
    plt.close(fig)  # 关闭图形窗口

# 定义常量
light_year = 9.461e15  # 光年到米的转换因子
distance = 10 * light_year  # 10光年的距离

# 定义行星初始位置和速度（示例数据，实际应根据具体行星数据调整）
initial_positions = np.array([[0, 0, 0], [0, 1e8, 0]])  # 初始位置，可以是多个行星
initial_velocities = np.array([[1e4, 0, 0], [0, 1e4, 0]])  # 初始速度，对应初始位置的行星

# 计算行星轨道并绘制轨迹图
for i in range(len(initial_positions)):
    positions = calculate_planet_orbit(initial_positions[i], initial_velocities[i], distance)
    plot_orbit(positions, f'Planet_{i + 1}')

#https://astroquery.readthedocs.io/en/latest/ipac/nexsci/nasa_exoplanet_archive.html