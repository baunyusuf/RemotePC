import sys
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QRadioButton,QPushButton,QTextEdit,QVBoxLayout,QHBoxLayout

class Pencere(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
    def init_ui(self):
        self.Hedef_IP_Label=QLabel("Hedef İP'nin raddrsi(localhost kullanımı için): ")
        self.Hedef_IP_Line=QLineEdit()
        self.dosya_transferi=QRadioButton("Dosya Transferi")
        self.ekran_paylasimi=QRadioButton("Ekran Paylaşımı")
        self.baglanbtn=QPushButton("Bağlan")
        self.listelebtn=QPushButton("Listele")
        self.kapatbtn=QPushButton("Çıkış")
        self.textedit=QTextEdit()
        hbox=QHBoxLayout()
        hbox2=QHBoxLayout()
        vbox=QVBoxLayout()
        hbox3=QHBoxLayout()

        hbox.addWidget(self.Hedef_IP_Label)
        hbox.addWidget(self.Hedef_IP_Line)
        vbox.addLayout(hbox)
        vbox.addWidget(self.dosya_transferi)
        vbox.addWidget(self.ekran_paylasimi)
        vbox.addStretch()
        hbox2.addWidget(self.baglanbtn)
        hbox2.addWidget(self.listelebtn)
        hbox2.addWidget(self.kapatbtn)
        vbox.addLayout(hbox2)

        hbox3.addLayout(vbox)
        hbox3.addWidget(self.textedit)

        self.setLayout(hbox3)

        self.show()

