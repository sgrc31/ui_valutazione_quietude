#!/usr/bin/env python3

import os
import sys
import subprocess
import serial
import serial.tools.list_ports
import logging
import time
import copy
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

logging.basicConfig(level=logging.WARNING)

class MyWin(QDialog):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.percorso = os.path.dirname(os.path.realpath(__file__))
        self.lista_valori_pwm_originali = [250, 90,
                                           250, 50,
                                           250, 60,
                                           250, 100,
                                           200, 250]
        self.lista_valori_pwm = copy.deepcopy(self.lista_valori_pwm_originali)
        self.initUI()

    def initUI(self):
        logging.info(self.percorso)
        #carico file interfaccia
        uic.loadUi('mainwin.ui', self)
        #carico e linko bottoni suono
        for i in range(1,7):
            self.bottone = getattr(self, 'snd_btn{0:0>2}'.format(i))
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
        self.reset_btn.clicked.connect(self.resetta_valori_pattern)
        self.set_btn.clicked.connect(self.set_valori_pattern)
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
        self.tipo_pattern = associazioni_pattern[self.sender().text().lower()]
        self.scrivi_seriale(self.tipo_pattern, self.lista_valori_pwm)
        if self.checkBox.checkState() == 2:
            self.tipo_suono2 = self.comboSuoni.currentText().lower()
            time.sleep(0.9)
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

    def resetta_valori_pattern(self):
        #self.lista_valori_pwm = self.lista_valori_pwm_originali
        self.slider_alte.setValue(self.lista_valori_pwm_originali[0])
        self.slider_basse.setValue(self.lista_valori_pwm_originali[1])
        self.slider_alte_3.setValue(self.lista_valori_pwm_originali[2])
        self.slider_basse_3.setValue(self.lista_valori_pwm_originali[3])
        self.slider_alte_2.setValue(self.lista_valori_pwm_originali[4])
        self.slider_basse_2.setValue(self.lista_valori_pwm_originali[5])
        self.slider_alte_4.setValue(self.lista_valori_pwm_originali[6])
        self.slider_basse_4.setValue(self.lista_valori_pwm_originali[7])
        self.slider_alte_6.setValue(self.lista_valori_pwm_originali[8])
        self.slider_alte_5.setValue(self.lista_valori_pwm_originali[9])
        self.set_valori_pattern()

    def set_valori_pattern(self):
        self.lista_valori_pwm[0] = self.slider_alte.sliderPosition()
        self.lista_valori_pwm[1] = self.slider_basse.sliderPosition()
        self.lista_valori_pwm[2] = self.slider_alte_3.sliderPosition()
        self.lista_valori_pwm[3] = self.slider_basse_3.sliderPosition()
        self.lista_valori_pwm[4] = self.slider_alte_2.sliderPosition()
        self.lista_valori_pwm[5] = self.slider_basse_2.sliderPosition()
        self.lista_valori_pwm[6] = self.slider_alte_4.sliderPosition()
        self.lista_valori_pwm[7] = self.slider_basse_4.sliderPosition()
        self.lista_valori_pwm[8] = self.slider_alte_6.sliderPosition()
        self.lista_valori_pwm[9] = self.slider_alte_5.sliderPosition()
        logging.info(self.lista_valori_pwm)
        self.scrivi_seriale(0, self.lista_valori_pwm)

    def scrivi_seriale(self, pattern, valori_pwm):
        self.tipo_attuatore = 0 if self.radioBtn_led.isChecked() else 1
        self.payload = str.encode('{} {} {} {} {} {} {} {} {} {} {} {}'.format(self.tipo_attuatore,
                                                                                     pattern,
                                                                                     *valori_pwm))
        self.ser.write(self.payload)
        logging.info(self.payload)


################
##  Start it  ##
################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWin()
    ex.show()
    sys.exit(app.exec_())
