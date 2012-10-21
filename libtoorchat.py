import os
import httplib
from threading import Thread

USER_NAME_SIZE = 9


def get_web_site(visual, site):
	''' This is a threaded message to query a website and create message to pass back '''
	try:
		connection = httplib.HTTPConnection(site)
		connection.request("GET", "/")
		result = connection.getresponse().read()
		visual.message_quque.append(result)
	except Exception:
		pass 


class ToorChatProtocol():
	''' This is a class to allow for easy of use with anything to do with messaging '''
	def __init__(self, device):
		self.PACKET_START = "\xFF\xDE\xAD\xFF"
		self.PACKET_END = "\xFF\xBE\xEF\xFF"
		self.device = device

	def send_chat_message(self, message = "", user = None):
		''' This is used to send a simple message over the toorchat protocol '''
		msg = ToorMessage(message, user)
		self.device.RFxmit(msg.to_string())
		return msg

	def change_channel(self, channel):
		''' This is used to change the channel that the user operates in '''
		if isinstance(channel, int):
			self.device.setChannel(int(channel))


	def change_frequency(self, frequency):
		''' This is used to change the frequency that the user operates in '''
		if isinstance(frequency, int):
			self.device.setFreq(int(frequency))

	def send_web_request(self, site = ""):
		'''This is used to attempt to get anyone who is registered as a server to load a website on your behalf '''
		if site != "":
			request = ToorMessage(site, None, ToorChatProtocol.get_web_request_type())
			self.device.RFxmit(request.to_string())

	@classmethod
	def parse_message(cls, raw_message):
		message = ToorMessage()
		message.raw = raw_message
		start_index = raw_message.find(ToorChatProtocol.get_packet_start())
		end_index = raw_message.find(ToorChatProtocol.get_packet_end())
		if start_index == -1 or end_index == -1:
			return None
		message.start = raw_message[start_index:start_index + 4]
		message.type = raw_message[start_index + 4: start_index + 5]
		message.xid = raw_message[start_index + 5: start_index + 13]
		message.user = raw_message[start_index + 13: start_index + 22]
		message.data = raw_message[start_index + 22: end_index]
		message.end = raw_message[end_index: end_index+4]
		return message

	@classmethod
	def get_web_messages(cls, site, visual):
		'''This is query the webpage and make thoose messages '''
		thread = Thread(target=get_web_site, args=(visual, site))
		thread.start()

	@classmethod
	def get_packet_start(cls):
		return "\xFF\xDE\xAD\xFF"
	
	@classmethod
	def get_packet_end(cls):
		return "\xFF\xBE\xEF\xFF"

	@classmethod
	def get_chat_type(cls):
		return "1"

	@classmethod
	def get_web_request_type(cls):
		return "2"

class ToorMessage():
	''' This is a simple Message object wrapper to make things cleaner '''

	def __init__(self, message = "", user = None, type=ToorChatProtocol.get_chat_type()):
		self.raw = None
		self.start = ToorChatProtocol.get_packet_start()
		self.xid = self.get_random_xid()
		self.type = type
		if user != None:
			self.user = user
			if len(self.user) < USER_NAME_SIZE:
				self.user = self.user + " "* (USER_NAME_SIZE-len(self.user))
		else:
			self.user = "anonymous"
		self.data = message
		self.end = ToorChatProtocol.get_packet_end()

	def get_random_xid(self):
		return os.urandom(8)

	def __str__(self):
		return self.start +self.type+ self.xid + self.user + self.data + self.end

	def to_string(self):
		return self.__str__()
