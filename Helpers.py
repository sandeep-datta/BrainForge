import sys

def funcname():
	return sys._getframe(2).f_code.co_name