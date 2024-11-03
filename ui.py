# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designercDFApt.ui'
##
## Created by: Qt User Interface Compiler version 5.15.15
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(985, 779)
        self.GridFrame = QFrame(Dialog)
        self.GridFrame.setObjectName(u"GridFrame")
        self.GridFrame.setGeometry(QRect(0, 10, 981, 721))
        self.GridFrame.setFrameShape(QFrame.StyledPanel)
        self.GridFrame.setFrameShadow(QFrame.Raised)
        self.Start = QPushButton(Dialog)
        self.Start.setObjectName(u"Start")
        self.Start.setGeometry(QRect(10, 740, 101, 31))
        self.Stop = QPushButton(Dialog)
        self.Stop.setObjectName(u"Stop")
        self.Stop.setGeometry(QRect(120, 740, 101, 31))
        self.Clear = QPushButton(Dialog)
        self.Clear.setObjectName(u"Clear")
        self.Clear.setGeometry(QRect(230, 740, 101, 31))
        self.AddPattern = QPushButton(Dialog)
        self.AddPattern.setObjectName(u"AddPattern")
        self.AddPattern.setGeometry(QRect(340, 740, 101, 31))
        self.Evolutionary_Computation = QPushButton(Dialog)
        self.Evolutionary_Computation.setObjectName(u"Evolutionary_Computation")
        self.Evolutionary_Computation.setGeometry(QRect(450, 740, 111, 31))
        self.SpeedSlider = QSlider(Dialog)
        self.SpeedSlider.setObjectName(u"SpeedSlider")
        self.SpeedSlider.setGeometry(QRect(810, 750, 160, 16))
        self.SpeedSlider.setOrientation(Qt.Horizontal)
        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(570, 740, 221, 28))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.Start.setText(QCoreApplication.translate("Dialog", u"Start", None))
        self.Stop.setText(QCoreApplication.translate("Dialog", u"Stop", None))
        self.Clear.setText(QCoreApplication.translate("Dialog", u"Clear", None))
        self.AddPattern.setText(QCoreApplication.translate("Dialog", u"Add Pattern", None))
        self.Evolutionary_Computation.setText(QCoreApplication.translate("Dialog", u"Add Evolution", None))
    # retranslateUi

