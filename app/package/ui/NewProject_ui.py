# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewProject.ui'
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
        MainWindow.resize(542, 696)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.bottom_frame = QFrame(self.frame)
        self.bottom_frame.setObjectName(u"bottom_frame")
        self.bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.bottom_frame)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.bottom_frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(12, 12, 12, 12)
        self.drivers_frame = QFrame(self.frame_5)
        self.drivers_frame.setObjectName(u"drivers_frame")
        self.drivers_frame.setFrameShape(QFrame.StyledPanel)
        self.drivers_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.drivers_frame)
        self.horizontalLayout_8.setSpacing(16)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.audio_frame = QFrame(self.drivers_frame)
        self.audio_frame.setObjectName(u"audio_frame")
        self.audio_frame.setFrameShape(QFrame.StyledPanel)
        self.audio_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.audio_frame)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame1 = QFrame(self.audio_frame)
        self.frame1.setObjectName(u"frame1")
        self.verticalLayout_4 = QVBoxLayout(self.frame1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame1)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_4.addWidget(self.label_3)

        self.frame_2 = QFrame(self.frame1)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.cb_audio_driver = QComboBox(self.frame_2)
        self.cb_audio_driver.addItem("")
        self.cb_audio_driver.addItem("")
        self.cb_audio_driver.addItem("")
        self.cb_audio_driver.setObjectName(u"cb_audio_driver")
        self.cb_audio_driver.setEnabled(True)
        self.cb_audio_driver.setAcceptDrops(False)
        self.cb_audio_driver.setEditable(False)

        self.verticalLayout_5.addWidget(self.cb_audio_driver)


        self.verticalLayout_4.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame1)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_6.addWidget(self.label_2)

        self.cb_audio_device = QComboBox(self.frame_3)
        self.cb_audio_device.setObjectName(u"cb_audio_device")
        self.cb_audio_device.setEnabled(True)

        self.verticalLayout_6.addWidget(self.cb_audio_device)


        self.verticalLayout_4.addWidget(self.frame_3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)


        self.horizontalLayout_9.addWidget(self.frame1)


        self.horizontalLayout_8.addWidget(self.audio_frame)

        self.video_frame = QFrame(self.drivers_frame)
        self.video_frame.setObjectName(u"video_frame")
        self.video_frame.setFrameShape(QFrame.StyledPanel)
        self.video_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.video_frame)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_21 = QFrame(self.video_frame)
        self.frame_21.setObjectName(u"frame_21")
        self.verticalLayout_7 = QVBoxLayout(self.frame_21)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.frame_21)
        self.label_4.setObjectName(u"label_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.verticalLayout_7.addWidget(self.label_4)

        self.frame_4 = QFrame(self.frame_21)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_4)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)

        self.verticalLayout_8.addWidget(self.label_5)

        self.cb_video_devices = QComboBox(self.frame_4)
        self.cb_video_devices.setObjectName(u"cb_video_devices")

        self.verticalLayout_8.addWidget(self.cb_video_devices)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)


        self.verticalLayout_7.addWidget(self.frame_4)


        self.horizontalLayout_10.addWidget(self.frame_21)


        self.horizontalLayout_8.addWidget(self.video_frame)


        self.verticalLayout_3.addWidget(self.drivers_frame)

        self.project_frame = QFrame(self.frame_5)
        self.project_frame.setObjectName(u"project_frame")
        self.project_frame.setFrameShape(QFrame.StyledPanel)
        self.project_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.project_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.name_location = QFrame(self.project_frame)
        self.name_location.setObjectName(u"name_location")
        self.name_location.setFrameShape(QFrame.StyledPanel)
        self.name_location.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.name_location)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_7 = QFrame(self.name_location)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_13.setSpacing(6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_7)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)
        self.label_6.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_13.addWidget(self.label_6)

        self.line_project_name = QLineEdit(self.frame_7)
        self.line_project_name.setObjectName(u"line_project_name")

        self.horizontalLayout_13.addWidget(self.line_project_name)


        self.verticalLayout_9.addWidget(self.frame_7)

        self.frame_9 = QFrame(self.name_location)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.frame_9)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)
        self.label_7.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_12.addWidget(self.label_7)

        self.line_project_location = QLineEdit(self.frame_9)
        self.line_project_location.setObjectName(u"line_project_location")

        self.horizontalLayout_12.addWidget(self.line_project_location)

        self.open_location = QToolButton(self.frame_9)
        self.open_location.setObjectName(u"open_location")

        self.horizontalLayout_12.addWidget(self.open_location)


        self.verticalLayout_9.addWidget(self.frame_9)


        self.verticalLayout_2.addWidget(self.name_location)

        self.FreqSelectors = QFrame(self.project_frame)
        self.FreqSelectors.setObjectName(u"FreqSelectors")
        self.FreqSelectors.setFrameShape(QFrame.StyledPanel)
        self.FreqSelectors.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.FreqSelectors)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.LowFreq = QFrame(self.FreqSelectors)
        self.LowFreq.setObjectName(u"LowFreq")
        self.LowFreq.setFrameShape(QFrame.StyledPanel)
        self.LowFreq.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.LowFreq)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.low_freq_dial = QDial(self.LowFreq)
        self.low_freq_dial.setObjectName(u"low_freq_dial")
        self.low_freq_dial.setAcceptDrops(False)
        self.low_freq_dial.setMinimum(30)
        self.low_freq_dial.setMaximum(100)
        self.low_freq_dial.setValue(30)
        self.low_freq_dial.setSliderPosition(30)

        self.verticalLayout_10.addWidget(self.low_freq_dial)

        self.low_freq_label = QLabel(self.LowFreq)
        self.low_freq_label.setObjectName(u"low_freq_label")
        font = QFont()
        font.setBold(False)
        self.low_freq_label.setFont(font)
        self.low_freq_label.setLayoutDirection(Qt.LeftToRight)
        self.low_freq_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.low_freq_label)


        self.horizontalLayout_3.addWidget(self.LowFreq)

        self.HighFreq = QFrame(self.FreqSelectors)
        self.HighFreq.setObjectName(u"HighFreq")
        self.HighFreq.setFrameShape(QFrame.StyledPanel)
        self.HighFreq.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.HighFreq)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.high_freq_dial = QDial(self.HighFreq)
        self.high_freq_dial.setObjectName(u"high_freq_dial")
        self.high_freq_dial.setAcceptDrops(False)
        self.high_freq_dial.setMinimum(30)
        self.high_freq_dial.setMaximum(100)
        self.high_freq_dial.setValue(30)

        self.verticalLayout_11.addWidget(self.high_freq_dial)

        self.high_freq_label = QLabel(self.HighFreq)
        self.high_freq_label.setObjectName(u"high_freq_label")
        self.high_freq_label.setFont(font)
        self.high_freq_label.setLayoutDirection(Qt.LeftToRight)
        self.high_freq_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_11.addWidget(self.high_freq_label)


        self.horizontalLayout_3.addWidget(self.HighFreq)

        self.frame_6 = QFrame(self.FreqSelectors)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.minimum_time_label = QLabel(self.frame_6)
        self.minimum_time_label.setObjectName(u"minimum_time_label")

        self.verticalLayout_12.addWidget(self.minimum_time_label)


        self.horizontalLayout_3.addWidget(self.frame_6)


        self.verticalLayout_2.addWidget(self.FreqSelectors)


        self.verticalLayout_3.addWidget(self.project_frame)

        self.verticalSpacer_2 = QSpacerItem(20, 218, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.buttons_frame = QFrame(self.frame_5)
        self.buttons_frame.setObjectName(u"buttons_frame")
        self.buttons_frame.setFrameShape(QFrame.StyledPanel)
        self.buttons_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.buttons_frame)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.buttons_frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.open_project_button = QPushButton(self.frame_8)
        self.open_project_button.setObjectName(u"open_project_button")

        self.horizontalLayout_15.addWidget(self.open_project_button)

        self.horizontalSpacer_2 = QSpacerItem(430, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_2)

        self.but_create = QPushButton(self.frame_8)
        self.but_create.setObjectName(u"but_create")
        self.but_create.setEnabled(True)

        self.horizontalLayout_15.addWidget(self.but_create)


        self.horizontalLayout_14.addWidget(self.frame_8)


        self.verticalLayout_3.addWidget(self.buttons_frame)


        self.horizontalLayout_7.addWidget(self.frame_5)


        self.verticalLayout.addWidget(self.bottom_frame)


        self.horizontalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 542, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.bottom_frame.setStyleSheet("")
        self.frame_5.setStyleSheet("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Audio", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Driver", None))
        self.cb_audio_driver.setItemText(0, QCoreApplication.translate("MainWindow", u"ASIO", None))
        self.cb_audio_driver.setItemText(1, QCoreApplication.translate("MainWindow", u"Blabla", None))
        self.cb_audio_driver.setItemText(2, QCoreApplication.translate("MainWindow", u"Yamaha", None))

        self.cb_audio_driver.setCurrentText(QCoreApplication.translate("MainWindow", u"ASIO", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Device", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Video", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Device", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Localization", None))
        self.open_location.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.low_freq_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.high_freq_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.minimum_time_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.open_project_button.setText(QCoreApplication.translate("MainWindow", u"Open Project", None))
        self.but_create.setText(QCoreApplication.translate("MainWindow", u"Create", None))
    # retranslateUi

