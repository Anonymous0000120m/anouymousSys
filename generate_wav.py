from moviepy.editor import ImageSequenceClip  
  
# 图像文件名列表  
image_files = ['frame1.png', 'frame2.png', 'frame3.png', ...]  # 这里填入你的图像文件名  
duration_per_image = 1  # 每张图像的显示时长（秒）  
  
# 使用ImageSequenceClip从图像序列创建视频剪辑  
clip = ImageSequenceClip(image_files, durations=[duration_per_image] * len(image_files))  
  
# 写入视频文件  
clip.write_videofile('output.mp4')