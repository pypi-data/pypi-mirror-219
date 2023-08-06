from __future__ import absolute_import
#from . import mkmain

import sys
import os
 
# 把当前文件所在文件夹的父文件夹路径加入到PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("init:",os.path.dirname(os.path.abspath(__file__)))
__version__ = '1.0.0'
__license__ = ''
