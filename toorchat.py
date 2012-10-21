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
			toor_message = ToorChatProtocol.parse_message(msg)
			if toor_message != None:
				visual.message_queue.append(toor_message)
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
		self.user = None
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
			self.last_message_index = 0
			while True:
				self.screen_max_y, self.screen_max_x = self.screen.getmaxyx()
				self.screen.addstr(0, 1, "[S] Send Message [U] Set User Name")
				self.__add_message_to_screen__()
				entry = self.screen.getch()
				if entry == curses.KEY_RESIZE:
					self.__draw_frame__(False)
				if entry == ord('s'):
					self.screen.nodelay(0)
					user_input = self.screen.getstr(1, 1, 60)
					old_message = self.protocol.send_message(user_input, self.user)
					self.message_queue.append(old_message)
					self.screen.nodelay(1)
					self.screen.addstr(1,1," "*(self.screen_max_x-3))
				if entry == ord('u'):
					self.screen.nodelay(0)
					user_input = self.screen.getstr(1, 1, 60)
					self.user = user_input[:USER_NAME_SIZE]
					self.screen.nodelay(1)
					self.screen.addstr(1,1," "*(self.screen_max_x-3))

		except KeyboardInterrupt:
			self.exit = True
			self.stop()

	def __add_message_to_screen__(self):
		if len(self.message_queue) > 0:
			message = self.message_queue[len(self.message_queue)-1]
			message_string = str(message.user)+":"+ str(message.data)
			self.screen.addstr(self.last_message_index+3,1, message_string + " "*(self.screen_max_x-(2+len(message_string))))
			self.last_message_index +=1
			self.message_queue.pop()
			if self.last_message_index > self.screen_max_y-5:
				self.last_message_index = 0
				self.__draw_frame__()

	def __draw_frame__(self, clear = True):
		if clear:
			self.screen.clear()
		self.screen.border(0)
		self.screen.addstr(2,1,"_"*(self.screen_max_x-2))

	def stop(self):
		curses.endwin()

if __name__ == '__main__':
	visual = Visualizer()
	visual.start()