# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'extractorset.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_exwin(QDialog):
    signal = pyqtSignal(int)

    def __init__(self, para):
        super(Ui_exwin, self).__init__()
        self.setupUi(self)

        self.para = 0
        self.comboBox.currentIndexChanged[int].connect(self.change)

    def setupUi(self, exwin):
        exwin.setObjectName("exwin")
        exwin.resize(349, 451)
        exwin.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        exwin.setAutoFillBackground(True)
        self.verticalLayoutWidget = QtWidgets.QWidget(exwin)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 190, 171, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setAutoFillBackground(False)
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout.addWidget(self.checkBox_3)
        self.checkBox_6 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setAutoFillBackground(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_6.setObjectName("checkBox_6")
        self.verticalLayout.addWidget(self.checkBox_6)
        self.checkBox_4 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setAutoFillBackground(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout.addWidget(self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setChecked(False)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout.addWidget(self.checkBox_5)
        self.label_2 = QtWidgets.QLabel(exwin)
        self.label_2.setGeometry(QtCore.QRect(40, 170, 151, 16))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(exwin)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(27, 40, 301, 28))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.entropyset = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        self.entropyset.setFont(font)
        self.entropyset.setObjectName("entropyset")
        self.horizontalLayout.addWidget(self.entropyset)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Adobe Heiti Std")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(exwin)
        self.buttonBox.setGeometry(QtCore.QRect(160, 370, 156, 23))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.scaleedit = QtWidgets.QLineEdit(exwin)
        self.scaleedit.setGeometry(QtCore.QRect(180, 80, 121, 21))
        self.scaleedit.setObjectName("scaleedit")
        self.buttonBox.accepted.connect(self.acceptwin)
        self.buttonBox.rejected.connect(self.rejectwin)

        self.retranslateUi(exwin)
        QtCore.QMetaObject.connectSlotsByName(exwin)

    def retranslateUi(self, exwin):
        _translate = QtCore.QCoreApplication.translate
        exwin.setWindowTitle(_translate("exwin", "提取设置"))
        self.checkBox_3.setText(_translate("exwin", "CPU"))
        self.checkBox_6.setText(_translate("exwin", "FFT"))
        self.checkBox_4.setText(_translate("exwin", "GPU"))
        self.checkBox_5.setText(_translate("exwin", "Pipline"))
        self.label_2.setText(_translate("exwin", "提取方法"))
        self.entropyset.setText(_translate("exwin", "随机数提取规模"))
        self.comboBox.setItemText(0, _translate("exwin", "自定义"))
        self.comboBox.setItemText(1, _translate("exwin", "默认值"))

    def change(self):
        if self.comboBox.currentText() == "自定义":
            self.scaleedit.show()
        elif self.comboBox.currentText() == "默认值":
            self.scaleedit.hide()
            self.para = 0

    def acceptwin(self):
        self.para = self.scaleedit.text()
        self.signal.emit(int(self.para))
        self.accept()

    def rejectwin(self):
        self.reject()
