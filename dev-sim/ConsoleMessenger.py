class ConsoleMessenger:
	def send_data(self, lectura, timestamp, uuid):
		print("sensor {} midió {} en {}".format(uuid, lectura, timestamp))