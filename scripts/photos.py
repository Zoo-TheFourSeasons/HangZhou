import os
import time
from multiprocessing import Process

from PIL import Image
from PIL.ExifTags import TAGS


class Photo(object):
    formats = ('jpg', 'JPG')

    def __init__(self):
        pass

    @staticmethod
    def create_thumbnail(file, thumbnail_folder):
        """
        创建略缩图
        :param file: 图片路径
        :param thumbnail_folder: 略缩图保存目录
        :return: None
        """
        print('创建略缩图', file)
        im = Image.open(file)

        im_width = im.size[0]
        im_high = im.size[1]

        if im_high > im_width:
            # 高>宽
            ####
            #  #
            #  #
            #  #
            ####
            width = im_width
            spare = (im_high - width) / 2
            left = 0
            upper = spare
            right = width
            lower = spare + width
        else:
            #########
            #       #
            #########
            width = im_high
            spare = (im_width - width) / 2
            left = spare
            upper = 0
            right = spare + width
            lower = width
        im_crop = im.crop((left, upper, right, lower))
        for size in (120, 240, 640, ):
            im_resize = im_crop.resize((size, size))
            _, file_name = os.path.split(file)
            file_name = file_name[:-4] + 'x' + str(size) + file_name[-4:]
            path = os.path.join(thumbnail_folder, file_name)
            im_resize.save(path, "JPEG")

    @staticmethod
    def __create_folder(folder):
        """
        创建目录
        :param folder: 需创建的目录完整路径
        :return: None
        """
        if os.path.exists(folder):
            return
        os.mkdir(folder)

    @staticmethod
    def create_thumbnail_from_path(path):
        """
        从路径中创建略缩图
        :param path: 路径
        :return: None
        """
        # 链接
        if os.path.islink(path):
            print('路径错误: %s' % path)
            return

        # 进程列表
        processes = []
        # 创建略缩图目录
        folder = path
        if os.path.isfile(path):
            folder = os.path.dirname(path)

        thumbnail, thumbnail_name = os.path.split(folder)

        thumbnail_folder = os.path.join(thumbnail, thumbnail_name + '_thumbnail')
        Photo.__create_folder(thumbnail_folder)

        # 文件
        if os.path.isfile(path):
            # 非图
            if path[-3:] not in Photo.formats:
                print('文件格式错误: %s' % path)
                return
            file = path
            p = Process(target=Photo.create_thumbnail, args=(os.path.join(folder, file), thumbnail_folder))
            processes.append(p)

        # 文件夹
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                if file[-3:] not in Photo.formats:
                    continue
                p = Process(target=Photo.create_thumbnail, args=(os.path.join(folder, file), thumbnail_folder))
                processes.append(p)

        Photo.control_processes(processes)

    @staticmethod
    def reduce_size(file, reduce_folder):
        """

        :param file: 图片路径
        :param reduce_folder: 缩小图保存目录
        :return: None
        """
        print('创建缩小图', file)
        im = Image.open(file)

        im_width = im.size[0]
        im_high = im.size[1]

        try:
            exif = {}
            for tag, value in im._getexif().items():
                exif[TAGS.get(tag, tag)] = value
        except Exception as e:
            pass
        else:
            print(im_width, im_high, exif['YResolution'], exif['XResolution'])

    @staticmethod
    def reduce_size_from_path(path):
        """
        从路径中缩小图片大小
        :param path: 路径
        :return: None
        """
        # 链接
        if os.path.islink(path):
            print('路径错误: %s' % path)
            return
        pass
        # 进程列表
        processes = []
        # 创建缩小图目录
        folder = path
        if os.path.isfile(path):
            folder = os.path.dirname(path)

        reduce, reduce_name = os.path.split(folder)

        reduce_folder = os.path.join(reduce, reduce_name + '_reduce')
        Photo.__create_folder(reduce_folder)

        # 文件
        if os.path.isfile(path):
            # 非图
            if path[-3:] not in Photo.formats:
                print('文件格式错误: %s' % path)
                return
            file = path
            p = Process(target=Photo.reduce_size, args=(os.path.join(folder, file), reduce_folder))
            processes.append(p)

        # 文件夹
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                if file[-3:] not in Photo.formats:
                    continue
                p = Process(target=Photo.reduce_size, args=(os.path.join(folder, file), reduce_folder))
                processes.append(p)

        Photo.control_processes(processes)

    @staticmethod
    def control_processes(processes, max_alive=15):
        """
        控制并发进程数
        :param processes: 进程列表
        :param max_alive: 最大并发进程数
        :return: None
        """
        for process in processes:
            while len([p for p in processes if p.is_alive()]) > max_alive:
                time.sleep(0.5)
            process.start()

        for p in processes:
            p.join()

    @staticmethod
    def convert_to_html(path):
        """<img src="/static/images/06BeginningOfSummer_thumbnail/DSCF0633x120.JPG" class="thumbnail">"""
        files = os.listdir(path)
        _, folder = os.path.split(path)
        for file in files:
            if 'x240' not in file:
                continue

            html = """<img src="/static/images/%s/%s" class="thumbnail">""" % (folder, file)
            print(html)


if __name__ == '__main__':
    # 夏至
    # Photo.create_thumbnail_from_path(r'C:\-C\HangZhou\static\images\06BeginningOfSummer')
    # Photo.convert_to_html(r'C:\-C\HangZhou\static\images\06BeginningOfSummer_thumbnail')
    # Photo.reduce_size_from_path(r'C:\Users\0x7E4\Desktop\媒体\panda\200518红山动物园\pictures')
    # 小满
    Photo.create_thumbnail_from_path(r'C:\-C\HangZhou\static\images\07GrainFull')
    Photo.convert_to_html(r'C:\-C\HangZhou\static\images\07GrainFull_thumbnail')
