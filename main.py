#!/usr/bin/env python3

import sys
import subprocess
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MyWin(QDialog):
    homepath = '/home/sgrc/lab/quietude/code/ui_testuitenti/'
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.initUI()

    def initUI(self):
        uic.loadUi('mainwin.ui', self)
        for i in range(1,7):
            self.bottone = getattr(self, 'snd_btn{0:0>2}'.format(i))
            print(self.bottone)
            self.bottone.clicked.connect(self.lancia_suono)
        for i in range(1,7):
            self.bottone = getattr(self, 'pattern_btn{0:0>2}'.format(i))
            self.bottone.clicked.connect(self.lancia_pattern)
        for item in serial.tools.list_ports.comports():
            self.comboBox.addItem(item.device)
            print(item.device)
        self.player = QMediaPlayer()

    def lancia_pattern(self):
        associazioni_pattern = {'ambulanza': '1',
                        'allarme': '2',
                        'campanello': '3',
                        'fischietto': '4',
                        'elettrodomestico': '5',
                        'clacson': '6'
                        }
        self.tipo_pattern = str.encode(associazioni_pattern[self.sender().text().lower()])
        print(self.tipo_pattern)
        self.ser = serial.Serial(self.comboBox.currentText())
        self.ser.write(self.tipo_pattern)
        self.ser.close()

    def lancia_suono(self):
        self.tipo_suono = self.sender().text().lower()
        self.suono = QMediaContent(QUrl.fromLocalFile('{}{}{}{}'.format(self.homepath, 'sounds/', self.tipo_suono, '.mp3')))
        self.player.setMedia(self.suono)
        self.player.play()

################
##  Start it  ##
################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWin()
    ex.show()
    sys.exit(app.exec_())
