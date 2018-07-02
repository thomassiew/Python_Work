#!/usr/bin/env python

# Echo client program
import socket
import time
import threading
import multiprocessing
import thread


# f = open("datass", "w+")

class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # print "Starting " + self.name
        # Get lock to synchronize threads
        # threadLock.acquire()
        spam()
        # Free lock to release next thread
        # threadLock.release()


def spam():
    # HOST = ''
    # PORT = 5011
    HOST = '10.25.39.134'  # The remote host
    PORT = 81
    # The same port as used by the server

    while 1:
        try:
            # s = socket.create_connection((HOST,PORT),socket._GLOBAL_DEFAULT_TIMEOUT,('www.baidu.com', 80))

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((HOST, PORT))
            tm = time.time()
            # time.sleep(5)
            # try:
            s.send('thomas%s=' % (tm + 3) + ('%s' % (tm + 1)))
            # for x in range(100):
            # time.sleep(3)
            # s.send('thomas%s=' % (tm + 3) + ('%s' % (tm + 1)))
            # while 1:
            data = s.recv(1024)
            print "data: ", data
            #     if not data == "":
            #         # print "datafound"
            #
            #         host2 , port2 = data.split(":")
            #         a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #         # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #         a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #         a.connect((host2,int(port2)))
            #         a.send('thomas%s=' % (tm + 3) + ('%s' % (tm + 1)))
            #         data3 = a.recv(1024)
            #         # print data3
            #     s.shutdown(socket.SHUT_RDWR)
            #     s.close()
            #     a.shutdown(socket.SHUT_RDWR)
            #     a.close()
            #     break


            # f.write(data + ",")
            # s.send('thomas=GONGXIFACAI - ANGPAU MARI MARI HOM!!!!')
            # s.send('thomas=GONGXIFACAI - ANGPAU MARI MARI HOM!!!!')
            # s.send('thomas=GONGXIFACAI - ANGPAU MARI MARI HOM!!!!')
            # print s.send('thomas%s=' % (tm + 3) + ('%s' % (tm + 1))*10000)
            # abc = 1
            # aa = 1
            # while abc:

            # s.recv(1024)
            #     if data == "":
            #         print "empty"
            #         pass
            #         aa += 1
            #     elif data != "" or aa == 10:
            #         abc = 2

            # except:
            #     continue
            # #         break

        except:
            print "failed"
            # s.shutdown(socket.SHUT_RDWR)
            # s.close()
            time.sleep(5)
            continue
    # except:
    #     # print "failed"
    #     # f.write("failed"+ ",")
    #     pass
    # finally:
    #     try:
    #     time.sleep(.6)
    #     s.shutdown(socket.SHUT_RDWR)
    #     s.close()  # except:
# pass
def hi():
    #
    # for x in range(65000):
    # while 1:
    # while 1:
    for x in range(500):
        print "thread-", x
        #     t = threading.Thread(name="thread-" + str(x),target=spam(),args=(x,))
        #     t.start()

        thread1 = myThread()
        thread1.start()
        # print "out"
        # f.write("out"+ ",")
    while threading.activeCount():
        time.sleep(2)


if __name__ == '__main__':
    for x in range(1):
        process = multiprocessing.Process(target=hi)
        process.start()
