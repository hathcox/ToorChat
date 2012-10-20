#!/usr/bin/env python

import sys
from rflib import *
import rflib.chipcon_nic as rfnic
import atexit
from libtoorchat import *

def banner():
	print "******** ToorChat [v 0.1] ********"

def main():
	banner()
	badge = RfCat(idx=0)
	badge.setModeRX()
	protocol = ToorChatProtocol(badge)
	while True:
		try:
			print badge.RFrecv()
			# print msg
		except ChipconUsbTimeoutException:
			pass
	


if __name__ == '__main__':
	main()