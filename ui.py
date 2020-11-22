from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QRadioButton,QLabel,QListWidget,QVBoxLayout,QHBoxLayout
import sys
class arayüz2(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.kullanici=QLabel("Aktif Kullanıcılar")
        self.list=QListWidget()
        self.remote_pc=QRadioButton("Bilgisayar Yönetimi")
        self.file_transfer=QRadioButton("Dosya Paylaşımı")
        self.baglanbtn=QPushButton("Bağlan")
        self.listelebtn=QPushButton("Yenile")


        vbox=QVBoxLayout()
        hbox=QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.kullanici)
        hbox.addStretch()
        vbox.addLayout(hbox)
        vbox.addWidget(self.list)
        vbox.addWidget(self.remote_pc)
        vbox.addWidget(self.file_transfer)
        vbox.addWidget(self.baglanbtn)
        vbox.addWidget(self.listelebtn)

        self.setLayout(vbox)

        self.show()
