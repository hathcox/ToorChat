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
			# msg, timestamp =  badge.RFrecv()
			# print "enter a message"
			send = raw_input("Enter a message\n")
			protocol.send_message(send)
		except ChipconUsbTimeoutException:
			pass
	


if __name__ == '__main__':
	main()