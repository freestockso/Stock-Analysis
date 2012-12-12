import os,sys
__dir__ = os.path.realpath(os.path.dirname(__file__))
APP_HOME=os.path.join(__dir__,"..")
SYS_HOME=os.path.join(APP_HOME,"..")
SYS_LIB_HOME=os.path.join(SYS_HOME,"lib")
conf = {"SYS_HOME":SYS_HOME}
sys.path.insert(0,SYS_LIB_HOME)

from stk.statistics.Wave import wave
print wave(conf = conf)
