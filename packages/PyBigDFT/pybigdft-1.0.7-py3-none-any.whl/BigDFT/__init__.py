import os

import BigDFT.LogUtils as LogUtils

# useful attributes
filepath = os.path.abspath(__file__)
pythonpath = os.path.abspath(os.path.join(filepath, '../..'))
sourcepath = os.path.abspath(os.path.join(pythonpath, '..'))

Logger = LogUtils.LogHandler()
