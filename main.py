#!/usr/bin/env python3

import os
import sys
import subprocess
import serial
import serial.tools.list_ports
import logging
import time
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

logging.basicConfig(level=logging.WARNING)

class MyWin(QDialog):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.percorso = os.path.dirname(os.path.realpath(__file__))
        self.initUI()

    def initUI(self):
        logging.info(self.percorso)
        #carico file interfaccia
        uic.loadUi('mainwin.ui', self)
        #carico e linko bottoni suono
        for i in range(1,7):
            self.bottone = getattr(self, 'snd_btn{0:0>2}'.format(i))
            logging.info(self.bottone)
            self.bottone.clicked.connect(self.lancia_suono)
        #carico e linko bottoni pattern, disabilitati
        for i in range(1,7):
            self.bottone = getattr(self, 'pattern_btn{0:0>2}'.format(i))
            self.bottone.clicked.connect(self.lancia_pattern)
            self.bottone.setEnabled(False)
        #popolo comboBox con porte seriali
        for item in serial.tools.list_ports.comports():
            self.comboBox.addItem(item.device)
        self.openSerial_btn.clicked.connect(self.apri_seriale)
        #carico media player per i suoni
        self.player = QMediaPlayer()

    def apri_seriale(self):
        self.ser = serial.Serial(self.comboBox.currentText(), 9600)
        time.sleep(1)
        for i in range(1,7):
            self.bottone = getattr(self, 'pattern_btn{0:0>2}'.format(i))
            self.bottone.setEnabled(True)

    def lancia_pattern(self):
        associazioni_pattern = {'ambulanza': '1',
                        'allarme': '2',
                        'campanello': '3',
                        'fischietto': '4',
                        'elettrodomestico': '5',
                        'clacson': '6'
                        }
        self.tipo_pattern = str.encode(associazioni_pattern[self.sender().text().lower()])
        logging.info(self.tipo_pattern)
        self.ser.write(self.tipo_pattern)
        self.tipo_suono2 = self.comboSuoni.currentText().lower()
        self.lancia_suono2(self.tipo_suono2)

    def lancia_suono(self):
        self.tipo_suono = self.sender().text().lower()
        self.suono = QMediaContent(QUrl.fromLocalFile(os.path.join(self.percorso, 'sounds', '{}{}'.format(self.tipo_suono, '.mp3'))))
        self.player.setMedia(self.suono)
        self.player.play()

    def lancia_suono2(self, nomesuono):
        self.suono = QMediaContent(QUrl.fromLocalFile(os.path.join(self.percorso, 'sounds', '{}{}'.format(nomesuono, '.mp3'))))
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
