'''
Description: 
Author: F.O.X
Date: 2021-03-23 19:24:12
LastEditor: F.O.X
LastEditTime: 2022-10-01 00:46:02
'''

import os  # noqa: E402
os.environ['PATH'] = os.path.dirname(os.path.realpath(
    __file__)) + os.pathsep + os.environ['PATH']  # noqa: E402
from .Andor3Cam import Camera
