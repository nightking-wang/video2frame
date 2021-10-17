# video2frame
## crop images from videos
# 你还在为看视频截PPT而烦恼吗
 # 你还在为手动裁剪和转换挠头吗
# 他来了他来了  自动化的乞丐脚本他来了
# 操作简单，极易上手
# 不要告诉老师 他会打我！！！！！

# requirements
- python 3
- cv2  opencv-python
- skimage
- shutil

# 创建环境
## 安装依赖包
pip install -r requirements.txt


# 运行
## demo 
python video2frame.py --input [videopath] output [imagesavepath] --time_init 截取开始的时间点 默认0  --time_end 截取结束的时间点 --inter 截取的时间间隔 每隔多久截一次 默认2 --box 裁剪的区域[y0,y1,x0,x1] [左上点的在y方向的坐标，右下点在y方向的坐标，左上点在x方向的坐标，右下点在x方向的坐标]  不要搞反了

0————————————————————————————————————>x
|
|
|
|
|
|
|
|
y

python videoframe.py --input G:/Desktop/test.mp4 --output G:/Desktop/images2 --time_init 0 --time_end 500 --inter 2 --box [95,588, 285,1160]
