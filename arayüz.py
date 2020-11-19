import sys
from PyQt5 import QtWidgets

class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
    def init_ui(self):
        self.hedef_ip=QtWidgets.QLineEdit()
        self.listele=QtWidgets.QPushButton("Listele")
        self.baglan=QtWidgets.QPushButton("Bağlan")
        self.kapat=QtWidgets.QPushButton("Kapat")

        hbox=QtWidgets.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.listele)
        hbox.addWidget(self.baglan)
        hbox.addWidget(self.kapat)
        hbox.addStretch()

        vbox=QtWidgets.QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.hedef_ip)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        



        self.show()

