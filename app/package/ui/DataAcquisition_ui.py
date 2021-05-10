# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataAcquisition.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_frame = QFrame(self.frame)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setFrameShape(QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.top_frame)

        self.bottom_frame = QFrame(self.frame)
        self.bottom_frame.setObjectName(u"bottom_frame")
        self.bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.bottom_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.left_frame = QFrame(self.bottom_frame)
        self.left_frame.setObjectName(u"left_frame")
        self.left_frame.setFrameShape(QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.left_frame)

        self.mid_frame = QFrame(self.bottom_frame)
        self.mid_frame.setObjectName(u"mid_frame")
        self.mid_frame.setFrameShape(QFrame.StyledPanel)
        self.mid_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.mid_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cam_view = QLabel(self.mid_frame)
        self.cam_view.setObjectName(u"cam_view")

        self.horizontalLayout_3.addWidget(self.cam_view)


        self.horizontalLayout.addWidget(self.mid_frame)

        self.right_frame = QFrame(self.bottom_frame)
        self.right_frame.setObjectName(u"right_frame")
        self.right_frame.setFrameShape(QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.right_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.start_stop_button = QPushButton(self.right_frame)
        self.start_stop_button.setObjectName(u"start_stop_button")

        self.horizontalLayout_4.addWidget(self.start_stop_button)


        self.horizontalLayout.addWidget(self.right_frame)


        self.verticalLayout.addWidget(self.bottom_frame)


        self.horizontalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.cam_view.setText("")
        self.start_stop_button.setText(QCoreApplication.translate("MainWindow", u"START!", None))
    # retranslateUi

