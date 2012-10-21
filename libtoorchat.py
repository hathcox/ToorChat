
class ToorChatProtocol():
	''' This is a class to allow for easy of use with anything to do with messaging '''
	def __init__(self, device):
		self.PACKET_START = "\xFF\xDE\xAD\xFF"
		self.PACKET_END = "\xFF\xBE\xEF\xFF"
		self.device = device

	def send_message(self, message = "", user = None):
		''' This is used to send a simple message over the toorchat protocol '''
		msg = ToorChatMessage(message, user)
		self.device.RFxmit(msg.to_string())

	@classmethod
	def parse_message(cls, raw_message):
		message = ToorChatMessage()
		message.raw = raw_message
		start_index = raw_message.find(ToorChatProtocol.get_packet_start())
		end_index = raw_message.find(ToorChatProtocol.get_packet_end())
		if start_index == -1 or end_index == -1:
			return None
		message.start = raw_message[start_index:start_index + 4]
		message.xid = raw_message[start_index + 4: start_index + 12]
		message.user = raw_message[start_index + 12: start_index + 44]
		message.data = raw_message[start_index + 44: end_index]
		message.end = raw_message[end_index: end_index+4]
		return message

	@classmethod
	def get_packet_start(cls):
		return "\xFF\xDE\xAD\xFF"
	
	@classmethod
	def get_packet_end(cls):
		return "\xFF\xBE\xEF\xFF"

class ToorChatMessage():
	''' This is a simple Message object wrapper to make things cleaner '''

	def __init__(self, message = "", user = None):
		self.raw = None
		self.start = ToorChatProtocol.get_packet_start()
		self.xid = self.get_random_xid()
		if user != None:
			self.user = user
		else:
			self.user = "\xAA"*32
		self.data = message
		self.end = ToorChatProtocol.get_packet_end()

	def get_random_xid(self):
		return "44444444"

	def __str__(self):
		return self.start + self.xid + self.user + self.data + self.end

	def to_string(self):
		return self.__str__()