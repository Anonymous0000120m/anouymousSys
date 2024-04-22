import matplotlib.pyplot as plt
import pandas as pd

# 读取CSV文件
df = pd.read_csv('missile_trajectory.csv')

# 提取数据
t = df['Time']
x = df['X Position']
y = df['Y Position']

# 绘制导弹轨迹
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Missile Trajectory')
plt.grid(True)
plt.show()
