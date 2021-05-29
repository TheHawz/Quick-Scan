# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DisplayResults.ui'
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
        MainWindow.resize(827, 651)
        self.actionOpen_Project = QAction(MainWindow)
        self.actionOpen_Project.setObjectName(u"actionOpen_Project")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame_5 = QFrame(self.frame_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.bg_img_label = QLabel(self.frame_5)
        self.bg_img_label.setObjectName(u"bg_img_label")

        self.horizontalLayout_4.addWidget(self.bg_img_label)


        self.horizontalLayout_2.addWidget(self.frame_5)

        self.spectrum_groupBox = QGroupBox(self.frame_2)
        self.spectrum_groupBox.setObjectName(u"spectrum_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectrum_groupBox.sizePolicy().hasHeightForWidth())
        self.spectrum_groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.spectrum_groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spectrum = QVBoxLayout()
        self.spectrum.setObjectName(u"spectrum")

        self.horizontalLayout_3.addLayout(self.spectrum)


        self.horizontalLayout_2.addWidget(self.spectrum_groupBox)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.frame_3)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_7 = QFrame(self.groupBox)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(250, 0))
        self.label_2.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_7.addWidget(self.label_2)

        self.pr_name = QLabel(self.frame_7)
        self.pr_name.setObjectName(u"pr_name")

        self.horizontalLayout_7.addWidget(self.pr_name)


        self.verticalLayout_2.addWidget(self.frame_7)

        self.frame_9 = QFrame(self.groupBox)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(self.frame_9)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(250, 0))
        self.label_4.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_8.addWidget(self.label_4)

        self.grid_config = QLabel(self.frame_9)
        self.grid_config.setObjectName(u"grid_config")

        self.horizontalLayout_8.addWidget(self.grid_config)


        self.verticalLayout_2.addWidget(self.frame_9)

        self.frame_8 = QFrame(self.groupBox)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_6 = QLabel(self.frame_8)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(250, 0))
        self.label_6.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_9.addWidget(self.label_6)

        self.audio_info = QLabel(self.frame_8)
        self.audio_info.setObjectName(u"audio_info")

        self.horizontalLayout_9.addWidget(self.audio_info)


        self.verticalLayout_2.addWidget(self.frame_8)


        self.verticalLayout_3.addWidget(self.groupBox)


        self.verticalLayout.addWidget(self.frame_3)


        self.horizontalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 827, 22))
        self.menuArchive = QMenu(self.menubar)
        self.menuArchive.setObjectName(u"menuArchive")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuArchive.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuArchive.addAction(self.actionOpen_Project)
        self.menuArchive.addAction(self.action_Quit)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_Project.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
#if QT_CONFIG(tooltip)
        self.actionOpen_Project.setToolTip(QCoreApplication.translate("MainWindow", u"Create a new project or load an old one", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpen_Project.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
#if QT_CONFIG(tooltip)
        self.action_Quit.setToolTip(QCoreApplication.translate("MainWindow", u"Close the program safely", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_Quit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.bg_img_label.setText("")
        self.spectrum_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"3rd Octave Spectrum", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Project Information", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Project Name:", None))
        self.pr_name.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Grid Config:", None))
        self.grid_config.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Sample Rate and Frequency Range: ", None))
        self.audio_info.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.menuArchive.setTitle(QCoreApplication.translate("MainWindow", u"Archive", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

