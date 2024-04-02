import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, get_body_barycentric, get_body, Observer

# 设置观测者的位置（地球观测者）
obs = Observer(location=[0, 0], unit=(u.deg, u.deg), name="Earth")

# 设置观测时间范围
start_time = Time('2024-01-01')
end_time = Time('2024-12-31')
times = start_time + (end_time - start_time) * np.linspace(0, 1, 365)

# 计算木星和土星的位置
with solar_system_ephemeris.set('builtin'):
    jupiter = get_body('jupiter', times, location=obs)
    saturn = get_body('saturn', times, location=obs)

# 绘制木星和土星的轨道
plt.figure(figsize=(10, 6))
plt.plot(times.datetime, jupiter.distance, label='Jupiter')
plt.plot(times.datetime, saturn.distance, label='Saturn')
plt.xlabel('Date')
plt.ylabel('Distance (AU)')
plt.title('Distance from Earth to Jupiter and Saturn')
plt.legend()
plt.grid(True)
plt.show()