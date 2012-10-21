#!/usr/bin/env python

import sys
from rflib import *
import rflib.chipcon_nic as rfnic
import atexit
from libtoorchat import *
from os import system
import curses
import time
from threading import Thread

def thread_run(visual):
	''' This is our function for the thread '''
	#Thread should run until exit
	while not visual.exit:
		try:
			msg, timestamp = visual.badge.RFrecv()
			visual.message_queue.append(msg)
		except ChipconUsbTimeoutException:
			pass

class Visualizer():

	def __init__(self):
		self.screen = curses.initscr()
		# curses.noecho()
		# curses.cbreak()
		self.screen.nodelay(1)
		self.badge = RfCat(idx=0)
		self.badge.setModeRX()
		self.protocol = ToorChatProtocol(self.badge)
		self.message_queue = []
		#This when set to True will kill the thread
		self.exit = False

	def start(self):
		self.__start_recv_thread__()
		self.__run__()

	def __start_recv_thread__(self):
		'''This spins off a thread to deal with recving information from the rf device '''
		self.thread = Thread(target=thread_run, args=(self,))
		self.thread.start()

	def __run__(self):
		try:
			self.screen_max_y, self.screen_max_x = self.screen.getmaxyx()
			self.__draw_frame__()
			self.screen.refresh()
			while True:
				self.screen_max_y, self.screen_max_x = self.screen.getmaxyx()
				self.screen.addstr(0, 1, "[S] Send Message ")
				self.screen.addstr(3,1,"Count:" + str(len(self.message_queue)))
				entry = self.screen.getch()
				if entry == curses.KEY_RESIZE:
					self.__draw_frame__()
				if entry == ord('s'):
					self.screen.nodelay(0)
					user_input = self.screen.getstr(1, 1, 60)
					self.protocol.send_message(user_input)
					self.screen.nodelay(1)
					self.__draw_frame__()
					self.screen.refresh()

		except KeyboardInterrupt:
			self.exit = True
			self.stop()

	def __draw_frame__(self):
		self.screen.clear()
		self.screen.border(0)
		self.screen.addstr(2,1,"_"*(self.screen_max_x-2))

	def stop(self):
		curses.endwin()

if __name__ == '__main__':
	visual = Visualizer()
	visual.start()