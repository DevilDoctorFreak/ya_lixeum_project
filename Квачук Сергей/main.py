import sys
import cv2
import socket
import time
import multiprocessing

import pyaudio

from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1071, 727)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.screen = QtWidgets.QLabel(self.centralwidget)
        self.screen.setGeometry(QtCore.QRect(30, 50, 631, 471))
        font = QtGui.QFont()
        font.setPointSize(72)
        self.screen.setFont(font)
        self.screen.setFrameShape(QtWidgets.QFrame.Box)
        self.screen.setText("")
        self.screen.setObjectName("screen")
        self.conbtn = QtWidgets.QPushButton(self.centralwidget)
        self.conbtn.setGeometry(QtCore.QRect(10, 620, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.conbtn.setFont(font)
        self.conbtn.setObjectName("conbtn")
        self.disconbtn = QtWidgets.QPushButton(self.centralwidget)
        self.disconbtn.setGeometry(QtCore.QRect(10, 620, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.disconbtn.setFont(font)
        self.disconbtn.setObjectName("disconbtn")
        self.endvid = QtWidgets.QPushButton(self.centralwidget)
        self.endvid.setGeometry(QtCore.QRect(530, 620, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.endvid.setFont(font)
        self.endvid.setObjectName("endvid")
        self.startvid = QtWidgets.QPushButton(self.centralwidget)
        self.startvid.setGeometry(QtCore.QRect(350, 620, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.startvid.setFont(font)
        self.startvid.setObjectName("startvid")
        self.warmes = QtWidgets.QLabel(self.centralwidget)
        self.warmes.setGeometry(QtCore.QRect(150, 620, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.warmes.setFont(font)
        self.warmes.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.warmes.setText("")
        self.warmes.setObjectName("warmes")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(680, 50, 381, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.chat = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.chat.setObjectName("chat")
        self.verticalLayout.addWidget(self.chat)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.line = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line.setFont(font)
        self.line.setText("")
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.sendbtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sendbtn.setFont(font)
        self.sendbtn.setObjectName("sendbtn")
        self.horizontalLayout_2.addWidget(self.sendbtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1071, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.conbtn.setText(_translate("MainWindow", "Подключиться"))
        self.disconbtn.setText(_translate("MainWindow", "Отключиться"))
        self.endvid.setText(_translate("MainWindow", "Выключить камеру"))
        self.startvid.setText(_translate("MainWindow", "Включить камеру"))
        self.sendbtn.setText(_translate("MainWindow", "Отправить"))


class Videolink(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # uic.loadUi('videolink_main.ui', self)
        self.sock = socket.socket()
        self.f = open('1.png', 'wb')

        self.gettingmes = multiprocessing.Process(target=self.getmes)

        # создание экземпляра PyAudio
        self.audio = pyaudio.PyAudio()

        # Создание аргументов для PyAudio
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = 5

        # задание параметра QTimer
        self.timerVideo = QTimer(self)
        self.timerVideo.setSingleShot(False)
        self.timerVideo.timeout.connect(self.Cam)

        # Подключение виджетов и настройка их
        self.startvid.clicked.connect(self.startVideo)
        self.endvid.clicked.connect(self.endVideo)
        self.conbtn.clicked.connect(self.connection)
        self.disconbtn.clicked.connect(self.disconnection)
        self.sendbtn.clicked.connect(self.sendmes)

        self.disconbtn.setEnabled(False)
        self.disconbtn.setVisible(False)
        self.chat.setEnabled(False)
        self.chat.setVisible(False)
        self.line.setEnabled(False)
        self.line.setVisible(False)
        self.sendbtn.setEnabled(False)
        self.sendbtn.setVisible(False)

        # Подключение камеры
        self.cap = cv2.VideoCapture(cv2.CAP_DSHOW, 0)
        self.cap.set(3, 480)
        self.cap.set(4, 640)
        self.cap.set(5, 35)

    def Cam(self):
        # Получение картинки с веб-камеры
        ret, image = self.cap.read()
        image = cv2.flip(image, 1)
        im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = im.shape
        step = channel * width
        qImg = QImage(im.data, width, height, step, QImage.Format_RGB888)
        self.screen.setPixmap(QPixmap.fromImage(qImg))

    def Aud(self):
        # Модуль звука
        stream = self.audio.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.RATE,
                                 input=True,
                                 output=True,
                                 input_device_index=1,
                                 frames_per_buffer=self.CHUNK)

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            stream.write(data, self.CHUNK)

        stream.stop_stream()
        stream.close()

    # Включение видео
    def startVideo(self):
        self.timerVideo.start(50)

    # Выключение видео
    def endVideo(self):

        self.timerVideo.stop()
        self.screen.clear()

    # Модуль подключения к сокетам
    def connection(self):

        who_server, ok_pressed = QInputDialog.getItem(
            self, "Выберите хост", "Что делать?",
            ("Ждать гостей", "Идти в гости"), 1, False)

        if ok_pressed:

            if who_server == "Ждать гостей":
                self.sock.bind((socket.gethostbyname_ex(socket.gethostname())[2][0], 9090))
                self.sock.listen(1)
                self.conn, self.addr = self.sock.accept()

                self.turnOn()

                # self.gettingmes.start()

            else:
                ip, ok_pressed = QInputDialog.getText(self, "Введите в поле",
                                                      "IP адрес вашего друга")
                if ok_pressed:
                    try:
                        self.sock.connect((ip, 9090))
                        self.turnOn()

                    except socket.gaierror:
                        self.warmes.setText('Сервер не найден')
                        time.sleep(3)
                        self.warmes.clear()
                    except ConnectionRefusedError:
                        self.warmes.setText('Подключение не установлено')
                        time.sleep(3)
                        self.warmes.clear()

    def getmes(self):
        while True:
            data = self.conn.recv(63000).decode('UTF-8')
            self.chat.addItem(data + ' (visitor)')

            if not data:
                break
        self.gettingmes.join()

    # Модуль отключения от сокетов
    def disconnection(self):
        # self.gettingmes.join()
        self.conn.close()

        self.disconbtn.setEnabled(False)
        self.disconbtn.setVisible(False)
        self.conbtn.setEnabled(True)
        self.conbtn.setVisible(True)

        self.chat.setEnabled(False)
        self.chat.setVisible(False)
        self.line.setEnabled(False)
        self.line.setVisible(False)
        self.sendbtn.setEnabled(False)
        self.sendbtn.setVisible(False)

    def sendmes(self):
        self.conn.send(self.line.text().encode('UTF-8'))
        self.chat.addItem(self.line.text() + ' (you)')
        self.line.clear()

    def turnOn(self):
        self.disconbtn.setEnabled(True)
        self.disconbtn.setVisible(True)
        self.conbtn.setEnabled(False)
        self.conbtn.setVisible(False)

        self.chat.setEnabled(True)
        self.chat.setVisible(True)
        self.line.setEnabled(True)
        self.line.setVisible(True)
        self.sendbtn.setEnabled(True)
        self.sendbtn.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = Videolink()
    exe.show()
    sys.exit(app.exec())

