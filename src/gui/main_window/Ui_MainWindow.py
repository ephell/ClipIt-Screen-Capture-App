# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.central_layout = QHBoxLayout()
        self.central_layout.setObjectName(u"central_layout")
        self.left_panel = QWidget(self.centralwidget)
        self.left_panel.setObjectName(u"left_panel")
        self.left_panel.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout = QVBoxLayout(self.left_panel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.select_area_button = QPushButton(self.left_panel)
        self.select_area_button.setObjectName(u"select_area_button")

        self.verticalLayout.addWidget(self.select_area_button)

        self.start_recording_button = QPushButton(self.left_panel)
        self.start_recording_button.setObjectName(u"start_recording_button")

        self.verticalLayout.addWidget(self.start_recording_button)

        self.stop_recording_button = QPushButton(self.left_panel)
        self.stop_recording_button.setObjectName(u"stop_recording_button")

        self.verticalLayout.addWidget(self.stop_recording_button)


        self.central_layout.addWidget(self.left_panel)

        self.separator_line = QFrame(self.centralwidget)
        self.separator_line.setObjectName(u"separator_line")
        self.separator_line.setFrameShadow(QFrame.Plain)
        self.separator_line.setLineWidth(1)
        self.separator_line.setFrameShape(QFrame.VLine)

        self.central_layout.addWidget(self.separator_line)

        self.right_panel = QWidget(self.centralwidget)
        self.right_panel.setObjectName(u"right_panel")
        self.right_panel.setMaximumSize(QSize(16777215, 16777215))

        self.central_layout.addWidget(self.right_panel)


        self.horizontalLayout.addLayout(self.central_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.select_area_button.setText(QCoreApplication.translate("MainWindow", u"Select Area", None))
        self.start_recording_button.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.stop_recording_button.setText(QCoreApplication.translate("MainWindow", u"Stop Recording", None))
    # retranslateUi

