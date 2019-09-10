import serial
class Arduino():
    def __init__(self):
        self.ser=serial.Serial(
        	port="/dev/ttyACM0", 
        	baudrate=115200,
        	timeout=0.1,
        	write_timeout=0.1,
        )

    def send(self, Value):
        str_sum=""
        for i in Value:
            str_sum+=str(i)+","
        
        self.ser.flushInput()
        self.ser.flushOutput()
        
        self.ser.write((str(str_sum)+"A").encode(encoding='utf-8', errors=''))
        #self.ser.write(bytes(b'str(str_sum)+"A"'))
