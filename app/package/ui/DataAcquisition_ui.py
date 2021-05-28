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
        self.horizontalLayout_5 = QHBoxLayout(self.top_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.cam_view = QLabel(self.top_frame)
        self.cam_view.setObjectName(u"cam_view")

        self.horizontalLayout_5.addWidget(self.cam_view)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


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
        self.horizontalLayout_8 = QHBoxLayout(self.left_frame)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.capture_bt = QPushButton(self.left_frame)
        self.capture_bt.setObjectName(u"capture_bt")
        self.capture_bt.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_8.addWidget(self.capture_bt)


        self.horizontalLayout.addWidget(self.left_frame)

        self.mid_groupBox = QGroupBox(self.bottom_frame)
        self.mid_groupBox.setObjectName(u"mid_groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.mid_groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_2 = QFrame(self.mid_groupBox)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.rows_sb = QSpinBox(self.frame_2)
        self.rows_sb.setObjectName(u"rows_sb")
        self.rows_sb.setMinimum(1)
        self.rows_sb.setMaximum(20)

        self.horizontalLayout_3.addWidget(self.rows_sb)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.mid_groupBox)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_6.addWidget(self.label_2)

        self.cols_sb = QSpinBox(self.frame_3)
        self.cols_sb.setObjectName(u"cols_sb")
        self.cols_sb.setMinimum(1)
        self.cols_sb.setMaximum(20)

        self.horizontalLayout_6.addWidget(self.cols_sb)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.mid_groupBox)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_7.addWidget(self.label_3)

        self.pad_sb = QSpinBox(self.frame_4)
        self.pad_sb.setObjectName(u"pad_sb")
        self.pad_sb.setMaximum(200)

        self.horizontalLayout_7.addWidget(self.pad_sb)


        self.verticalLayout_3.addWidget(self.frame_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.mid_groupBox)

        self.right_frame = QFrame(self.bottom_frame)
        self.right_frame.setObjectName(u"right_frame")
        self.right_frame.setFrameShape(QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.right_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.start_stop_button = QPushButton(self.right_frame)
        self.start_stop_button.setObjectName(u"start_stop_button")
        self.start_stop_button.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.start_stop_button)


        self.horizontalLayout.addWidget(self.right_frame)


        self.verticalLayout.addWidget(self.bottom_frame)


        self.horizontalLayout_2.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
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
        self.capture_bt.setText(QCoreApplication.translate("MainWindow", u"Take picture!", None))
        self.mid_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Grid Configuration:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"n\u00ba Rows", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"n\u00ba Cols", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Padding", None))
        self.start_stop_button.setText(QCoreApplication.translate("MainWindow", u"START!", None))
    # retranslateUi

