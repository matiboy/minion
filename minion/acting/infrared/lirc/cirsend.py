'''
    Credits to https://bitbucket.org/charltones/python-lirc/src/77f4a9c67512d1a00109a536d45b15c580f7e1ce/python-irsend.py?at=default
    Python port of irsend.c - a command line utility to send ir commands through LIRC
'''
import socket
import time

LIRCD = "/var/run/lirc/lircd"

class IRSend(object):

    def __init__(self, device=LIRCD, address=None):
        # connect to unix socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(device)
        self.sfile = self.sock.makefile()

    def send_packet(self, packet):
        self.packet = packet
        self.sfile.write(packet)
        self.sfile.flush()
        # now read the response
        return self.read_response()

    def read_response(self):
        resp = []
        while True:
            line = self.sfile.readline().strip()
            resp.append(line)
            if line=="END":
                if "SUCCESS" in resp:
                    return True
                else:
                    return False

    def send(self, codes):
        ''' send the specified codes
            codes: list of tuples of (directive, remote, code) or
                   (directive, remote, code, count)
        '''
        packet = ""
        for code in codes:
            directive = code[0]
            remote = code[1]
            if directive=="SEND_ONCE":
                acode = code[2]
                if len(code)==4:
                    count = code[3]
                else:
                    count = 1
                packet = "%s %s %s %s\n" % (directive, remote, acode, count)
                if not self.send_packet(packet):
                    print "Error sending packet: %s" % packet
            elif directive=="SLEEP":
                print "Sleep %s" % code[1]
                time.sleep(code[1])
