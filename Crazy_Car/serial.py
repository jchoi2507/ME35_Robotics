from machine import UART

class serial_comm():
    def __init__(self, baud, timeout = 50):
        self.uart = UART(0, baud, timeout = timeout)  #tx=Pin(0), rx=Pin(1)
        self.Ctrl = {'C':'\x03','D':'\x04','E':'\x05'}
        
    def send_raw(self, text):
        self.uart.write(text.encode())
        
    def send(self, text):
        self.send_raw(text+'\r\n')
        return self.read()
        
    def send_code(self, text):
        self.send(self.Ctrl['E'])
        self.send(text.replace('\n','\r\n'))
        self.send(self.Ctrl['D'])
        
    def read(self):
        if self.any():
            reply = self.uart.read()
            return reply.decode()
        return None
        
    def readln(self):
        if self.any():
            reply = self.uart.readline()
            return reply.decode()
        return None
        
    def abort(self):
        self.send(self.Ctrl['C'])
        
    def any(self):
        return self.uart.any()
