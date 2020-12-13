from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import threading
import redis
import sys


class msgListenerThread(QThread):
    msg_emitter = pyqtSignal(str)

    def __init__(self, r):
        super().__init__()
        self.r = r
        self.p = self.r.pubsub(ignore_subscribe_messages=True)

    def run(self):
        self.p.subscribe("msg")
        while True:
            msg_dict = self.p.get_message()
            if msg_dict:
                msg = msg_dict["data"].decode("utf-8")
                self.msg_emitter.emit(msg)


class AnaEkran(QWidget):
    def __init__(self, r):
        super().__init__()
        # redis instance
        self.r = r
        # create UserInterface(Arayuz)
        self.initUI()
        self.msg_listener_thread = msgListenerThread(self.r)
        self.msg_listener_thread.msg_emitter.connect(self.setMessage)
        self.msg_listener_thread.start()

    def initUI(self):
        h1box = QHBoxLayout()

        self.resize(QSize(200, 200))
        self.setMinimumSize(QSize(200, 200))
        self.setMaximumSize(QSize(200, 200))
        self.labelIp = QLabel("Mesaj buraya gelicek")

        h1box.addWidget(self.labelIp)
        self.setLayout(h1box)
        self.show()

    def setMessage(self, msg):
        self.labelIp.setText(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    r = redis.Redis(
        host="redis-11907.c135.eu-central-1-1.ec2.cloud.redislabs.com",
        password="jPHWcbukgy7r1qmBwa9VxNRHZmfeD9N9",
        port=11907,
        db=0,
    )
    mainScreen = AnaEkran(r)
    sys.exit(app.exec_())