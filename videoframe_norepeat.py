# -*- coding: utf-8 -*-

"""
输入视频
输出相似度低于标准的图片
自动裁剪ppt区域
"""

import os
import cv2    ##加载OpenCV模块
import shutil
# from skimage.measure import compare_ssim
# from skimage.metrics import _structural_similarity
from skimage.metrics import structural_similarity as ssim




def video2frames(pathIn='', 
                 pathOut='', 
                 only_output_video_info = False, 
                 extract_time_points = None, 
                 initial_extract_time = 0,
                 end_extract_time = None,
                 extract_time_interval = -1, 
                 output_prefix = 'frame',
                 jpg_quality = 100,
                 isColor = True):
    '''
    pathIn：视频的路径，比如：F:\python_tutorials\test.mp4
    pathOut：设定提取的图片保存在哪个文件夹下，比如：F:\python_tutorials\frames1\。如果该文件夹不存在，函数将自动创建它
    only_output_video_info：如果为True，只输出视频信息（长度、帧数和帧率），不提取图片
    extract_time_points：提取的时间点，单位为秒，为元组数据，比如，(2, 3, 5)表示只提取视频第2秒， 第3秒，第5秒图片
    initial_extract_time：提取的起始时刻，单位为秒，默认为0（即从视频最开始提取）
    end_extract_time：提取的终止时刻，单位为秒，默认为None（即视频终点）
    extract_time_interval：提取的时间间隔，单位为秒，默认为-1（即输出时间范围内的所有帧）
    output_prefix：图片的前缀名，默认为frame，图片的名称将为frame_000001.jpg、frame_000002.jpg、frame_000003.jpg......
    jpg_quality：设置图片质量，范围为0到100，默认为100（质量最佳）
    isColor：如果为False，输出的将是黑白图片
    '''

    cap = cv2.VideoCapture(pathIn)  ##打开视频文件
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  ##视频的帧数
    fps = cap.get(cv2.CAP_PROP_FPS)  ##视频的帧率
    dur = n_frames/fps  ##视频的时间
    
    ##如果only_output_video_info=True, 只输出视频信息，不提取图片
    if only_output_video_info:
        print('only output the video information (without extract frames)::::::')
        print("Duration of the video: {} seconds".format(dur))
        print("Number of frames: {}".format(n_frames))
        print("Frames per second (FPS): {}".format(fps))
    
    ##提取特定时间点图片
    elif extract_time_points is not None:
        if max(extract_time_points) > dur:   ##判断时间点是否符合要求
            raise NameError('the max time point is larger than the video duration....')
        try:
            os.mkdir(pathOut)
        except OSError:
            pass
        success = True
        count = 0
        while success and count < len(extract_time_points):
            cap.set(cv2.CAP_PROP_POS_MSEC, (1000*extract_time_points[count])) 
            success,image = cap.read()
            if success:
                if not isColor:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  ##转化为黑白图片
                print('Write a new frame: {}, {}th'.format(success, count+1))
                cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                count = count + 1

    else:
        ##判断起始时间、终止时间参数是否符合要求
        if initial_extract_time > dur:
            raise NameError('initial extract time is larger than the video duration....')
        if end_extract_time is not None:
            if end_extract_time > dur:
                raise NameError('end extract time is larger than the video duration....')
            if initial_extract_time > end_extract_time:
                raise NameError('end extract time is less than the initial extract time....')
        
        ##时间范围内的每帧图片都输出
        if extract_time_interval == -1:
            if initial_extract_time > 0:
                cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time)) 
            try:
                os.mkdir(pathOut)
            except OSError:
                pass
            print('Converting a video into frames......')
            if end_extract_time is not None:
                N = (end_extract_time - initial_extract_time)*fps + 1
                success = True
                count = 0
                while success and count < N:
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}/{}'.format(success, count+1, n_frames))
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count =  count + 1
            else:
                success = True
                count = 0
                while success:
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}/{}'.format(success, count+1, n_frames))
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count =  count + 1

        ##判断提取时间间隔设置是否符合要求    
        elif extract_time_interval > 0 and extract_time_interval < 1/fps:
            raise NameError('extract_time_interval is less than the frame time interval....')
        elif extract_time_interval > (n_frames/fps):
            raise NameError('extract_time_interval is larger than the duration of the video....')
        
        ##时间范围内每隔一段时间输出一张图片
        else:
            try:
                os.mkdir(pathOut)
            except OSError:
                pass
            print('Converting a video into frames......')
            if end_extract_time is not None:
                N = (end_extract_time - initial_extract_time)/extract_time_interval + 1
                success = True
                count = 0
                while success and count < N:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time+count*1000*extract_time_interval)) 
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}th'.format(success, count+1))
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1
            else:
                success = True
                count = 0
                while success:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time+count*1000*extract_time_interval)) 
                    success,image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        print('Write a new frame: {}, {}th'.format(success, count+1))
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1


def delete(filename1):
    os.remove(filename1)



def list_all_files(root):
    files = []
    list = os.listdir(root)
    # os.listdir()方法：返回指定文件夹包含的文件或子文件夹名字的列表。该列表顺序以字母排序
    for i in range(len(list)):
        element = os.path.join(root, list[i])
        # 需要先使用python路径拼接os.path.join()函数，将os.listdir()返回的名称拼接成文件或目录的绝对路径再传入os.path.isdir()和os.path.isfile().
        if os.path.isdir(element):  # os.path.isdir()用于判断某一对象(需提供绝对路径)是否为目录
            # temp_dir = os.path.split(element)[-1]
            # os.path.split分割文件名与路径,分割为data_dir和此路径下的文件名，[-1]表示只取data_dir下的文件名
            files.append(list_all_files(element))

        elif os.path.isfile(element):
            files.append(element)
    # print('2',files)
    return files


def ssim_compare(img_files):
    count = 0
    imgs_n = []
    for currIndex, filename in enumerate(img_files):
        if not os.path.exists(img_files[currIndex]):
            print('not exist', img_files[currIndex])
            break
        img = cv2.imread(img_files[currIndex])

        img1 = cv2.imread(img_files[currIndex + 1])

        #进行结构性相似度判断
        # ssim_value = _structural_similarity.structural_similarity(img,img1,multichannel=True)
        ssim_value = ssim(img,img1,multichannel=True)
        if ssim_value > 0.9:
            #基数
            count += 1
            imgs_n.append(img_files[currIndex + 1])
            print('big_ssim:',img_files[currIndex], img_files[currIndex + 1], ssim_value)
        # 避免数组越界
        if currIndex+1 >= len(img_files)-1:
            break
    return count , imgs_n






import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='parameters for this script')
    parser.add_argument('--input', type=str, default=None, help='path of the video end by .mp4')
    parser.add_argument('--output', type=str, default=None, help='path of the images you get')
    parser.add_argument('--time_init', type=int, default=0, help='the initial time you want to start in the video')
    parser.add_argument('--time_end', type=int, default=50, help='the end time you want to end in  this video')
    parser.add_argument('--inter', type=int, default=2, help='the extract_time_interval you want')
    parser.add_argument('--box', type=int, default=[95,588, 285,1160], help='the area you want to crop in the images [y0,y1,x0,x1]')
    args = parser.parse_args()
    print('the video you want to deal with is:', args.input)
    print('the images you get in the file:', args.output)
    print('the length of the video in second counting:', args.time_init)
    print('the extract_time_interval you want', args.inter)
    print('the area you want to crop in the images', args.box)

    # ##### 测试
    # # os.chdir(os.path.split(os.path.realpath(__file__))[0])
    # # print(os.getcwd())
    #
    # # dirs_path = 'G:\\Desktop\\test'  # 设置路径
    # # print(dirs_path)
    # # dirs = os.listdir(dirs_path)  # 获取指定路径下的文件
    # # for pathIn in dirs:  # 循环读取路径下的文件并筛选输出
    # #     #print("1")
    # #     if os.path.splitext(pathIn)[1] == ".mp4":  # 筛选mp4文件
    # #         print(pathIn)  # 输出所有的mp4文件
    # #         print("1")
    # #         continue
    #
    #
    #
    #
    # # videoFPS=cap.get(cv2.CAP_PROP_FPS)
    # # print (videoFPS)
    #
    # 输入视频路径读取
    # pathIn = 'G:/Desktop/test.mp4'  # 视频路径
    pathIn = args.input  # 视频路径
    print("start")
    #
    # # def getFilePathList(path, filetype):
    # #     pathList = []
    # #     for root, dirs, files in os.walk(path):
    # #         for file in files:
    # #             if file.endswith(filetype):
    # #                 pathList.append(os.path.join(root, file))
    # #     return pathList
    #
    #
    #
    #
    """ ##### 视频截取为图片 ####### """
    video2frames(pathIn, only_output_video_info = True)
    #
    # # pathOut = './frames1/'
    # # video2frames(pathIn, pathOut)
    # #
    # # pathOut = './frames2'
    # # video2frames(pathIn, pathOut, extract_time_points=(1, 2, 5))
    #
    # pathOut = 'G:\\Desktop\\images'  # 图片保存路径
    pathOut = args.output  # 图片保存路径
    video2frames(pathIn, pathOut,
                 initial_extract_time=args.time_init,
                 end_extract_time=args.time_end,  ### 视频总时长
                 extract_time_interval =args.inter)  ### 截取间隔
    # #
    # pathOut = './frames4/'
    # video2frames(pathIn, pathOut, extract_time_points=(0.3, 2), isColor = False)
    #
    #
    # pathOut = './frames5/'
    # video2frames(pathIn, pathOut, extract_time_points=(0.3, 2), jpg_quality=50)


    """" 删除重复的图片 """
    # path = 'G:/Desktop/images2'
    path = args.output
    img_path = path
    imgs_n = []

    all_files = list_all_files(path)  # 返回包含完整路径的所有图片名的列表
    print('1', len(all_files))

    # for files in all_files:
    #     # 根据文件名排序，x.rfind('/')是从右边寻找第一个‘/'出现的位置，也就是最后出现的位置
    #     # 注意sort和sorted的区别，sort作用于原列表，sorted生成新的列表，且sorted可以作用于所有可迭代对象
    #     files.sort(key=lambda x: int(x[x.rfind('/') + 1:-4]))  # 路径中包含“/”
    #     # print(files)
    img_files = []
    for img in all_files:
        if img.endswith('.jpg'):
            # 将所有图片名都放入列表中
            img_files.append(img)
    count, imgs_n = ssim_compare(all_files)
    print(img[:img.rfind('/')], "路径下删除的图片数量为：", count)
    cnt = 1
    for image in imgs_n:
        delete(image)


    """ $$$$$$$$$$$ 裁剪图片 $$$$$$$$$$"""
    # coding: utf-8
    from PIL import Image
    import os
    import os.path
    import numpy as np
    import cv2

    # 指明被遍历的文件夹
    # rootdir = 'G:/Desktop/images2'
    rootdir = args.output
    for parent, dirnames, filenames in os.walk(rootdir):  # 遍历每一张图片
        for filename in filenames:
            print('parent is :' + parent)
            print('filename is :' + filename)
            currentPath = os.path.join(parent, filename)
            print('the fulll name of the file is :' + currentPath)

            img = cv2.imread(currentPath)
            # print(img.format, img.size, img.mode)
            # img.show()
            # box1 = (17, 16, 158, 189)  # 设置左、上、右、下的像素
            image1 = img[args.box[0]:args.box[1], args.box[2]:args.box[3]]  # 图像裁剪
            cv2.imwrite(args.output + '/' + filename,image1)  # 存储裁剪得到的图像