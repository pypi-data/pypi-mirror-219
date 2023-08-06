from distutils.core import  setup
import setuptools
packages = ['yolov5-6','yolov5-6/data','yolov5-6/utils','yolov5-6/models']# 唯一的包名，自己取名
setup(name='yolov5-6',
	version='1.0',
	author='shenhui',
    packages=packages,
    package_dir={'yolov5-6': 'yolov5-6'},)
