def handle(data):
	return handle

class CameraInterface():

	def __init__(self):
		self.address = 'tcp://localhost:5555'

	def init_camera(self):
		context = zmq.Context()
		self.footage_socket = context.socket(zmq.PUB)
		self.footage_socket.connect(self.address)
		self.video_data = cv2.VideoCapture(0)  # init the camera

	def start_stream(self):	
		context = zmq.Context()
		self.footage_socket = context.socket(zmq.PUB)
		self.footage_socket.connect(self.address)
		self.video_data = cv2.VideoCapture(0)  # init the camera	
		while True:
		    try:
		        grabbed, frame = self.video_data.read()  # grab the current frame
		        #frame = cv2.resize(frame, (640, 480))  # resize the frame
		        #frame = cv2.resize(frame, (320, 240))  # resize the frame
		        encoded, buffer = cv2.imencode('.jpg', frame)
		        jpg_as_text = base64.b64encode(buffer)

		        print(len(jpg_as_text))
		        #jpg_as_text = zlib.compress(jpg_as_text)
		        print(type(jpg_as_text))
		        self.footage_socket.send(jpg_as_text)
		    except KeyboardInterrupt:
		        self.video_data.release()
		        cv2.destroyAllWindows()
		        break

	def fetch_frame(self,handle):
		context = zmq.Context()
		footage_socket = context.socket(zmq.SUB)
		footage_socket.bind('tcp://*:5555')
		footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

		while True:
		    try:
		        frame = footage_socket.recv_string()
		        frame = frame.encode()
		        #frame = zlib.decompress(frame)
		        print(len(frame))
		        print(type(frame))

		        img = base64.b64decode(frame)

		        npimg = np.fromstring(img, dtype=np.uint8)
		        source = cv2.imdecode(npimg, 1)

		        handle(source)

		    except KeyboardInterrupt:
		        cv2.destroyAllWindows()
		        break

def main():
	ci = CameraInterface()

	if sys.argv[1] == 's':
		ci.start_stream()

	else:
		ci.fetch_frame(handle)

if __name__ == "__main__":
	main()	        

