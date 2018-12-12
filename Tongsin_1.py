# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\JEJ\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\pyqt5_tools\Tongsin.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import serial
import threading
import requests
'''
ser = serial.Serial(
    port='COM14',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    timeout=0)
'''

ser = serial.Serial('/dev/ttyUSB0', 115200)  # 포트 설정 여서 하셈

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Ui_Tongsin(object):
    def setupUi(self, Tongsin):
        Tongsin.setObjectName("Tongsin")
        Tongsin.resize(586, 357)

        self.startbtn = QtWidgets.QPushButton(Tongsin)
        self.startbtn.setGeometry(QtCore.QRect(20, 50, 301, 291))
        self.startbtn.setObjectName("startbtn")
        self.startbtn.clicked.connect(self.startbtn_clicked)

        self.uselabel = QtWidgets.QLabel(Tongsin)
        self.uselabel.setGeometry(QtCore.QRect(350, 50, 200, 50))
        self.uselabel.setObjectName("uselabel")

        self.resultbtn = QtWidgets.QPushButton(Tongsin)
        self.resultbtn.setGeometry(QtCore.QRect(450, 290, 121, 51))
        self.resultbtn.setObjectName("resultbtn")

        self.endbtn = QtWidgets.QPushButton(Tongsin)
        self.endbtn.setGeometry(QtCore.QRect(330, 290, 121, 51))
        self.endbtn.setObjectName("endbtn")
        self.endbtn.clicked.connect(self.endbtn_clicked)

        self.Tongsin_Count = QtWidgets.QTextEdit(Tongsin)
        self.Tongsin_Count.setGeometry(QtCore.QRect(440, 180, 121, 41))
        self.Tongsin_Count.setObjectName("Tongsin_Count")

        self.packet_Length = QtWidgets.QTextEdit(Tongsin)
        self.packet_Length.setGeometry(QtCore.QRect(440, 130, 121, 41))
        self.packet_Length.setObjectName("packet_Length")

        self.countlabel = QtWidgets.QLabel(Tongsin)
        self.countlabel.setGeometry(QtCore.QRect(360, 190, 64, 21))
        self.countlabel.setObjectName("countlabel")

        self.lengthlabel = QtWidgets.QLabel(Tongsin)
        self.lengthlabel.setGeometry(QtCore.QRect(360, 140, 64, 21))
        self.lengthlabel.setObjectName("lengthlabel")

        self.countlabel_2 = QtWidgets.QLabel(Tongsin)
        self.countlabel_2.setGeometry(QtCore.QRect(333, 240, 101, 21))
        self.countlabel_2.setObjectName("countlabel_2")

        self.packet_Interval = QtWidgets.QTextEdit(Tongsin)
        self.packet_Interval.setGeometry(QtCore.QRect(440, 230, 121, 41))
        self.packet_Interval.setObjectName("packet_Interval")

        self.retranslateUi(Tongsin)
        QtCore.QMetaObject.connectSlotsByName(Tongsin)

    def retranslateUi(self, Tongsin):
        _translate = QtCore.QCoreApplication.translate
        Tongsin.setWindowTitle(_translate("Tongsin", "Form"))
        self.startbtn.setText(_translate("Tongsin", "시작"))
        self.uselabel.setText(_translate("Tongsin", "이용가능"))
        self.resultbtn.setText(_translate("Tongsin", "결과보기"))
        self.endbtn.setText(_translate("Tongsin", "이용 중지"))
        self.countlabel.setText(_translate("Tongsin", "통신 횟수"))
        self.lengthlabel.setText(_translate("Tongsin", "패킷 길이"))
        self.countlabel_2.setText(_translate("Tongsin", "패킷 전송 간격"))

    def startbtn_clicked(self):
        self.startbtn.setText("Test가 진행중 입니다.")

        if (self.Tongsin_Count.toPlainText()) == "" or (self.packet_Interval.toPlainText()) == "" or (
        self.packet_Length.toPlainText()) == "":
            self.uselabel.setText("값을 입력하세요")

        elif not (0 < (int(self.Tongsin_Count.toPlainText())) < 65537 and 0 < (
                int(self.packet_Interval.toPlainText())) and 0 < (int(self.packet_Length.toPlainText())) < 33):
            self.uselabel.setText("통신 횟수는 <1~65536>, \n 패킷 전송 값은 0 이상,\n 패킷 길이는 <1~32>로 입력해주세요.")

        elif 0 < (int(self.Tongsin_Count.toPlainText())) < 65537 and 0 < (
                int(self.packet_Interval.toPlainText())) and 0 < (int(self.packet_Length.toPlainText())) < 33:

            # 데이터를 인코딩해서 변수에 짠!
            serial_data = bytes(self.Tongsin_Count.toPlainText(), 'utf-8')

            ser.write(serial_data)

            self.uselabel.setText("이용중..")

    def endbtn_clicked(self):
        self.uselabel.setText("이용가능")
        self.startbtn.setText("시작")

    def showMessageBox(self):
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.question(self, "Error", "값을 입력해 주세요.", QtWidgets.QMessageBox.Ok)


def read_serial_thread():
    while(True):
        tem = ser.readline()
        if not (tem == b''):
            print(tem)
            serial_read_data = tem    
            MachineID=str(int(str(serial_read_data[49:55]).strip('b\''),2))
            PacketLength=(str(int(str(serial_read_data[55:60]).strip('b\''),2)))
            PacketCount=(str(int(str(serial_read_data[60:71]).strip('b\''),2)+1))
            Milis=(str(int(str(serial_read_data[72:96]).strip('b\''),2)))
            total=MachineID+':'+PacketLength+':'+PacketCount+':'+Milis
            params={'a':'gateway','id':'1','f':total}
            r=requests.get(url='http://dev.nrf24test.infoboss.co.kr:82/testsession.php',params=params)
            print(total)
            print(r.url)
            print(r.text)

if __name__ == "__main__":
    import sys

    t = threading.Thread(target=read_serial_thread)
    t.start()  # 아직까지 읽는 거 test를 안해봄 알아서하셈

    app = QtWidgets.QApplication(sys.argv)
    Tongsin = QtWidgets.QWidget()
    ui = Ui_Tongsin()
    ui.setupUi(Tongsin)
    Tongsin.show()
    sys.exit(app.exec_())