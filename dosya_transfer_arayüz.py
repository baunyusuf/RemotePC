from PyQt5.QtWidgets import QWidget,QApplication,QFileDialog,QTextEdit,QPushButton,QHBoxLayout,QVBoxLayout,QListWidget
import sys
import os

class Dosya_Pencere(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
    def init_ui(self):
        self.resize(1280, 500)
        self.ekle=QPushButton("Ekle")
        self.gonder=QPushButton("Gönder")
        self.temizle=QPushButton("Temizle")
        self.list=QListWidget()
        self.i=0
        
        hbox=QHBoxLayout()
        vbox=QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.ekle)
        vbox.addWidget(self.gonder)
        vbox.addWidget(self.temizle)
        vbox.addStretch()
        hbox.addWidget(self.list)
        hbox.addLayout(vbox)


        self.setLayout(hbox)



