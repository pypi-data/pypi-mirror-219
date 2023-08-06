from distutils.core import setup
from setuptools import find_packages
 
setup(name = 'sdbsxwf',     # 包名
      version = '20230713',  # 版本号
      description = '个人工具箱',
      long_description = '试着改变世界', 
      author = 'xwf',
      author_email = '453211170@qq.com',
      url = '',
      license = '',
      install_requires=[
        'six>=1.5.2',
        'parsel>=1.1',
    ], #申明依赖包
      classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
      ],
      keywords = '',
      packages = find_packages('src'),  # 必填，就是包的代码主目录
      package_dir = {'':'src'},         # 必填
      include_package_data = True,
)
