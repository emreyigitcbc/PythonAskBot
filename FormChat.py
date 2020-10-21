import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QApplication, QLabel, QScrollArea

from CoreChat import AskBot, resource_path, Settings, data, similarity, wtokenizer, logger


class AskForm(QWidget):
    def __init__(self, parent=None):
        super(AskForm, self).__init__(parent)
        self.setWindowTitle("AskBOT")
        with open(resource_path("Style.css"), "r") as css:
            self.setStyleSheet(css.read())
        self.resizeWindow()
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        frame = QFormLayout()

        self.info = QLabel()
        self.info.setText("AskBOT")
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setProperty("Title", True)

        self.slider = QScrollArea()
        self.slider.setWidgetResizable(True)
        self.slider.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.slider.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.box = QLabel()
        self.box.setText(AskBot(True, ""))
        self.box.setAlignment(Qt.AlignCenter)
        self.box.setProperty("Chat", True)
        self.box.setTextFormat(Qt.RichText)

        self.slider.setWidget(self.box)
        self.slider.setMinimumHeight(500)
        self.slider.setAlignment(Qt.AlignHCenter)

        self.slide = self.slider.verticalScrollBar()
        self.slide.rangeChanged.connect(lambda: self.slide.setValue(self.slide.maximum()))

        self.message = QLineEdit()
        self.message.setFocusPolicy(Qt.StrongFocus)
        self.message.setPlaceholderText("Please, type something...")
        self.message.setAlignment(QtCore.Qt.AlignCenter)


        frame.addWidget(self.info)
        frame.addWidget(self.slider)
        frame.addWidget(self.message)

        self.setLayout(frame)

    def getMessage(self):
        self.message.setFocus()
        entry = self.message.text()
        self.message.setText("")
        cevap = AskBot(False, entry)
        self.box.setText(
            self.box.text() + "<br><span style='color: red'>YOU:</span><br>" + entry + "<br>" + cevap)
        logger("YOU: " + entry + "\n" + cevap)
        self.cleancontrol(entry)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.message.setFocus()
            self.getMessage()
        else:
            self.message.setFocus()
            super().keyPressEvent(qKeyEvent)

    def resizeWindow(self):
        if Settings.getSetting("Fullscreen") == "Yes":
            self.setCursor(Qt.BlankCursor)
            self.showFullScreen()
        else:
            self.setCursor(Qt.ArrowCursor)
            self.resize(800,700)

    def closeEvent(self, event):
        self.message.setFocus()
        event.ignore()

    def cleancontrol(self, entry):
        for mindata in data["Cleaning"]:
            for eleman in wtokenizer.tokenize(entry):
                if entry in mindata["key"] and similarity(entry, mindata["key"]) >= 0.7:
                    time.delay(1)
                    self.box.setText(AskBot(True, ""))
                elif eleman in mindata["key"] and similarity(eleman, mindata["key"]) >= 0.7:
                    time.delay(1)
                    self.box.setText(AskBot(True, ""))
                else:
                    for key in mindata["key"]:
                        if similarity(entry, key) >= 0.67:
                            time.sleep(1)
                            self.box.setText(AskBot(True, ""))
                        elif similarity(eleman, key) >= 0.67:
                            time.sleep(1)
                            self.box.setText(AskBot(True, ""))
                    else:
                        return 1


def starter():
    form = QApplication(sys.argv)
    baslat = AskForm()
    baslat.show()
    baslat.message.setFocus()
    form.exec_()

starter()
